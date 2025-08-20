import os, glob, argparse
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

# ---------- Fixed inner-art coordinates (absolute pixel boxes) ----------
# Derived from your earlier slot boxes & margins.
INNER_ART_COORDS = [
    (144, 46, 211, 119),  # Slot 1 inner art
    (251, 46, 318, 119),  # Slot 2 inner art
    (358, 46, 425, 119),  # Slot 3 inner art
    (465, 46, 532, 119),  # Slot 4 inner art
]

def classify_slots(img_path: str, tmpl_vecs: dict, out_overlay: str | None = None):
    """
    Returns a 4-tuple of best-match names for slots 1..4.
    If out_overlay is given, saves an overlay image with boxes + labels.
    """
    img = Image.open(img_path).convert("RGB")

    draw = None
    if out_overlay:
        draw = img.copy()
        d = ImageDraw.Draw(draw)

    best_names = []

    for i, (ix0, iy0, ix1, iy1) in enumerate(INNER_ART_COORDS, start=1):
        inner = img.crop((ix0, iy0, ix1, iy1))
        v = to_vec(inner)
        # pick best cosine score
        best_name, best_score = max(((name, cosine(v, tv)) for name, tv in tmpl_vecs.items()),
                                    key=lambda x: x[1])
        best_names.append(best_name)

        if out_overlay:
            d.rectangle([ix0, iy0, ix1, iy1], outline=(255,255,0), width=2)
            d.text((ix0 + 4, max(0, iy0 - 14)), f"S{i}: {best_name} ({best_score:.2f})", fill=(255,255,255))

    if out_overlay:
        draw.save(out_overlay)

    # Return four values (tuple of length 4)
    return tuple(best_names)

def main():
    # Fixed locations relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    templates_dir = os.path.join(base_dir, "templates_borderless")
    out_dir = os.path.join(base_dir, "output")

    ap = argparse.ArgumentParser()
    ap.add_argument("--save_overlays", action="store_true")
    args = ap.parse_args()

    os.makedirs(out_dir, exist_ok=True)
    _, tmpl_vecs = load_templates(templates_dir)

    # gather images from data/
    img_paths = []
    for ext in ("*.png","*.jpg","*.jpeg","*.webp","*.bmp"):
        img_paths += sorted(glob.glob(os.path.join(data_dir, ext)))
    if not img_paths:
        raise RuntimeError(f"No screenshots found in {data_dir}")

    for p in img_paths:
        base = os.path.splitext(os.path.basename(p))[0]
        out_overlay = os.path.join(out_dir, f"{base}_overlay.png") if args.save_overlays else None
        s1, s2, s3, s4 = classify_slots(p, tmpl_vecs, out_overlay=out_overlay)
        print(f"{os.path.basename(p)} -> {s1}, {s2}, {s3}, {s4}")

if __name__ == "__main__":
    main()
