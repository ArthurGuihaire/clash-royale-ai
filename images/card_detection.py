import os, glob, argparse, time
import numpy as np
from PIL import Image, ImageDraw

# ---------- utility ----------
def to_vec(im, size=(150,165)):
    imr = im.resize(size, Image.Resampling.LANCZOS)
    arr = np.asarray(imr).astype(np.float32) / 255.0
    arr = arr - arr.mean()
    v = arr.reshape(-1)
    n = np.linalg.norm(v) + 1e-8
    return v / n

def cosine(u, v):
    return float(np.dot(u, v))

def load_templates(tmpl_dir: str):
    tmpls = []
    for ext in ("*.png","*.jpg","*.jpeg","*.webp","*.bmp"):
        for p in sorted(glob.glob(os.path.join(tmpl_dir, ext))):
            name = os.path.splitext(os.path.basename(p))[0]
            tmpls.append((name, Image.open(p).convert("RGB")))
    if not tmpls:
        raise RuntimeError(f"No templates found in {tmpl_dir}")
    vecs = {name: to_vec(im) for name, im in tmpls}
    return tmpls, vecs

# ---------- Fixed inner-art coordinates ----------
INNER_ART_COORDS = [
    (144, 46, 211, 119),  # Slot 1 inner art
    (251, 46, 318, 119),  # Slot 2 inner art
    (358, 46, 425, 119),  # Slot 3 inner art
    (465, 46, 532, 119),  # Slot 4 inner art
]

# Tiny slot (width=34, height=35)
TINY_SLOT_COORDS = (37, 139, 71, 174)

# ---------- core classifier ----------
def classify_slot(img: Image.Image,
                  tmpl_vecs: dict,
                  coords: tuple[int, int, int, int],
                  drawer: ImageDraw.ImageDraw | None = None,
                  label: str | None = None):
    """
    Classify a single crop defined by `coords` against `tmpl_vecs`.
    Returns (best_name, best_score).
    If `drawer` is provided, draws the box + label onto that canvas.
    """
    x0, y0, x1, y1 = coords
    crop = img.crop((x0, y0, x1, y1))
    v = to_vec(crop)
    best_name, best_score = max(((name, cosine(v, tv)) for name, tv in tmpl_vecs.items()),
                                key=lambda x: x[1])

    if drawer is not None:
        drawer.rectangle([x0, y0, x1, y1], outline=(255,255,0), width=2)
        lab = label or "slot"
        drawer.text((x0 + 4, max(0, y0 - 14)), f"{lab}: {best_name} ({best_score:.2f})", fill=(255,255,255))

    return best_name, float(best_score)

def classify_four_main(img_path: str, tmpl_vecs_main: dict, out_overlay: str | None = None):
    """
    Classify the 4 main inner-art slots.
    Returns a list of (name, score) for each slot.
    """
    img = Image.open(img_path).convert("RGB")
    draw = None
    if out_overlay:
        canvas = img.copy()
        draw = ImageDraw.Draw(canvas)

    results = []
    for i, coords in enumerate(INNER_ART_COORDS, start=1):
        name, score = classify_slot(img, tmpl_vecs_main, coords, drawer=draw, label=f"S{i}")
        results.append((name, score))

    if out_overlay:
        canvas.save(out_overlay)

    return results

def classify_tiny(img_path: str, tmpl_vecs_tiny: dict, out_overlay: str | None = None):
    """
    Classify ONLY the tiny slot at TINY_SLOT_COORDS.
    Returns (name, score).
    """
    img = Image.open(img_path).convert("RGB")
    draw = None
    if out_overlay:
        canvas = img.copy()
        draw = ImageDraw.Draw(canvas)

    name, score = classify_slot(img, tmpl_vecs_tiny, TINY_SLOT_COORDS, drawer=draw, label="Tiny")

    if out_overlay:
        canvas.save(out_overlay)

    return name, score

def main():
    # Fixed locations relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    templates_main_dir = os.path.join(base_dir, "templates_borderless")
    templates_tiny_dir = os.path.join(base_dir, "templates_tiny")
    out_dir = os.path.join(base_dir, "output")

    ap = argparse.ArgumentParser()
    ap.add_argument("--save_overlays", action="store_true")
    ap.add_argument("--only_tiny", action="store_true", help="Only classify the tiny slot.")
    ap.add_argument("--only_main", action="store_true", help="Only classify the four main slots.")
    ap.add_argument("--print_scores", action="store_true", help="Print the score of the best match for each slot.")
    ap.add_argument("--profile", action="store_true", help="Print classification time for each image.")
    args = ap.parse_args()

    # sanity: if both flags are on, prefer tiny-only
    mode_only_tiny = args.only_tiny
    mode_only_main = args.only_main and not args.only_tiny

    os.makedirs(out_dir, exist_ok=True)

    # Load only what we need
    tmpl_vecs_main = None
    tmpl_vecs_tiny = None
    if not mode_only_tiny:
        _, tmpl_vecs_main = load_templates(templates_main_dir)
    if not mode_only_main:
        _, tmpl_vecs_tiny = load_templates(templates_tiny_dir)

    # gather images from data/
    img_paths = []
    for ext in ("*.png","*.jpg","*.jpeg","*.webp","*.bmp"):
        img_paths += sorted(glob.glob(os.path.join(data_dir, ext)))
    if not img_paths:
        raise RuntimeError(f"No screenshots found in {data_dir}")

    for p in img_paths:
        base = os.path.splitext(os.path.basename(p))[0]
        start_time = time.perf_counter() if args.profile else None

        if mode_only_tiny:
            overlay = os.path.join(out_dir, f"{base}_overlay_tiny.png") if args.save_overlays else None
            name, score = classify_tiny(p, tmpl_vecs_tiny, out_overlay=overlay)
            if args.print_scores:
                output_str = f"{os.path.basename(p)} -> tiny={name} ({score:.3f})"
            else:
                output_str = f"{os.path.basename(p)} -> tiny={name}"

        elif mode_only_main:
            overlay = os.path.join(out_dir, f"{base}_overlay_main.png") if args.save_overlays else None
            results = classify_four_main(p, tmpl_vecs_main, out_overlay=overlay)
            if args.print_scores:
                slots_str = ", ".join(f"S{i+1}: {n} ({s:.3f})" for i, (n, s) in enumerate(results))
            else:
                slots_str = ", ".join(n for n, _ in results)
            output_str = f"{os.path.basename(p)} -> {slots_str}"

        else:
            overlay = os.path.join(out_dir, f"{base}_overlay.png") if args.save_overlays else None
            main_results = classify_four_main(p, tmpl_vecs_main, out_overlay=None)
            tiny_name, tiny_score = classify_tiny(p, tmpl_vecs_tiny, out_overlay=None)
            if args.save_overlays:
                # Draw both sets to one overlay
                img = Image.open(p).convert("RGB")
                canvas = img.copy()
                d = ImageDraw.Draw(canvas)
                for i, coords in enumerate(INNER_ART_COORDS, start=1):
                    classify_slot(img, tmpl_vecs_main, coords, drawer=d, label=f"S{i}")
                classify_slot(img, tmpl_vecs_tiny, TINY_SLOT_COORDS, drawer=d, label="Tiny")
                canvas.save(overlay)

            if args.print_scores:
                main_str = ", ".join(f"S{i+1}: {n} ({s:.3f})" for i, (n, s) in enumerate(main_results))
                tiny_str = f"Tiny: {tiny_name} ({tiny_score:.3f})"
                output_str = f"{os.path.basename(p)} -> {main_str}, {tiny_str}"
            else:
                main_str = ", ".join(n for n, _ in main_results)
                output_str = f"{os.path.basename(p)} -> {main_str}, tiny={tiny_name}"

        if args.profile:
            elapsed = time.perf_counter() - start_time
            output_str += f"  [Time: {elapsed:.4f} s]"

        print(output_str)

if __name__ == "__main__":
    main()
