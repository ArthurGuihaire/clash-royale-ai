import os, glob, csv, argparse
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

# ---------- Fixed-slot cropping (user-provided pixel coords) ----------
FIXED_SLOT_COORDS = [
    (131, 25, 228, 145),  # Slot 1
    (238, 25, 335, 145),  # Slot 2
    (345, 25, 442, 145),  # Slot 3
    (452, 25, 549, 145),  # Slot 4
]

def crop_slots(img, roi_override=None, use_auto_roi=True):
    """Return roi image and list of (slot_full, inner_art) for 4 slots.
       This version uses fixed pixel coordinates for slots (as provided by the user).
    """
    slots = []
    for (sx0, sy0, sx1, sy1) in FIXED_SLOT_COORDS:
        slot = img.crop((sx0, sy0, sx1, sy1))
        # Trim margins to isolate inner art
        margin_x = int(0.14*slot.size[0])
        margin_y_top = int(0.10*slot.size[1])
        margin_y_bot = int(0.22*slot.size[1])
        inner = slot.crop((margin_x, margin_y_top,
                           slot.size[0]-margin_x, slot.size[1]-margin_y_bot))
        slots.append((slot, inner, (sx0, sy0, sx1, sy1)))

    # ROI here is just the bounding box covering all slots
    x0 = min(coords[0] for _, _, coords in slots)
    y0 = min(coords[1] for _, _, coords in slots)
    x1 = max(coords[2] for _, _, coords in slots)
    y1 = max(coords[3] for _, _, coords in slots)
    roi = img.crop((x0, y0, x1, y1))
    return roi, slots

def process_image(path, tmpl_vecs, out_overlay=None, accept_threshold=None):
    img = Image.open(path).convert("RGB")
    roi, slots = crop_slots(img)
    results = []
    if out_overlay:
        draw = img.copy()
        d = ImageDraw.Draw(draw)

    for i, (slot, inner, box) in enumerate(slots):
        v = to_vec(inner)
        scores = [(name, cosine(v, tv)) for name, tv in tmpl_vecs.items()]
        scores.sort(key=lambda x: x[1], reverse=True)
        best_name, best_score = scores[0]
        accepted = True
        if accept_threshold is not None and best_score < accept_threshold:
            accepted = False
        results.append({
            "slot": i+1,
            "best": best_name if accepted else "UNKNOWN",
            "score": round(float(best_score), 4),
            "top3": "; ".join([f"{n}:{s:.3f}" for n,s in scores[:3]])
        })

        if out_overlay:
            (sx0, sy0, sx1, sy1) = box
            d.rectangle([sx0, sy0, sx1, sy1], outline=(255,255,0), width=2)
            label = f"S{i+1}: {results[-1]['best']} ({best_score:.2f})"
            d.text((sx0+4, sy0-14), label, fill=(255,255,255))

    if out_overlay:
        draw.save(out_overlay)
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--templates_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--threshold", type=float, default=None,
                    help="Min cosine score to accept a match; else UNKNOWN.")
    ap.add_argument("--save_overlays", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    tmpls, tmpl_vecs = load_templates(args.templates_dir)

    rows = []
    img_paths = []
    for ext in ("*.png","*.jpg","*.jpeg","*.webp","*.bmp"):
        img_paths += sorted(glob.glob(os.path.join(args.data_dir, ext)))
    if not img_paths:
        raise RuntimeError(f"No screenshots found in {args.data_dir}")

    for p in img_paths:
        base = os.path.splitext(os.path.basename(p))[0]
        out_overlay = None
        if args.save_overlays:
            out_overlay = os.path.join(args.out_dir, f"{base}_overlay.png")
        res = process_image(p, tmpl_vecs,
                            out_overlay=out_overlay,
                            accept_threshold=args.threshold)
        for r in res:
            rows.append({
                "image": os.path.basename(p),
                "slot": r["slot"],
                "best": r["best"],
                "score": r["score"],
                "top3": r["top3"],
            })

    csv_path = os.path.join(args.out_dir, "matches.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["image","slot","best","score","top3"])
        w.writeheader()
        w.writerows(rows)

    print(csv_path)

if __name__ == "__main__":
    main()
