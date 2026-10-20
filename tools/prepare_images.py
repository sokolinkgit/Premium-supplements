#!/usr/bin/env python3
"""Prepare the site imagery from the art-directed source shots.

The layout asks for fixed aspect ratios and a single grade, so this script
takes the source stills in `assets/img/_raw/` and `assets/img/florals/_raw/`
and writes the final JPEG/WebP files the pages reference, plus the decorative
florals (crops of the watercolour branch, a painted gold botanical branch and a
soft watercolour wash) and their alpha-matted variants for the burgundy panels.

    .venv-img/bin/python tools/prepare_images.py

Sources are kept out of Git (see .gitignore); the rendered outputs are the
files that ship.
"""
from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
RAW = os.path.join(IMG, "_raw")
FLORAL = os.path.join(IMG, "florals")
FLORAL_RAW = os.path.join(FLORAL, "_raw")

WHITE = (255, 253, 251)
BLUSH = (247, 213, 216)
PEARL = (252, 233, 232)
GOLD = (214, 163, 77)


# --------------------------------------------------------------------------
# grading
# --------------------------------------------------------------------------
def crop_to_aspect(img, aspect, focus=(0.5, 0.5)):
    w, h = img.size
    target = aspect
    if w / h > target:
        nw = int(round(h * target))
        x = int(round((w - nw) * focus[0]))
        box = (x, 0, x + nw, h)
    else:
        nh = int(round(w / target))
        y = int(round((h - nh) * focus[1]))
        box = (0, y, w, y + nh)
    return img.crop(box)


def grade(img, warmth=1.012, lift=2, contrast=1.03, blush=0.030, seed=3, vignette=0.06):
    """A single, consistent grade: warm ivory lift, gentle contrast, blush edges."""
    arr = np.asarray(img.convert("RGB"), dtype=np.float32)

    # contrast about mid-grey, then a per-channel warm scale
    arr = (arr - 128.0) * contrast + 128.0
    arr[..., 0] += lift * 1.2
    arr[..., 1] += lift * 0.9
    arr[..., 2] += lift * 0.7
    arr[..., 0] *= warmth
    arr[..., 1] *= 1.0
    arr[..., 2] *= 1 / warmth

    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = np.clip(np.sqrt(((xx / w - 0.5) / 0.74) ** 2 + ((yy / h - 0.5) / 0.74) ** 2), 0, 1)[..., None] ** 2
    arr = arr * (1 - vignette * v) + np.array((214, 160, 168), dtype=np.float32) * (vignette * v)

    blush_strength = np.clip((yy / h - 0.62) / 0.38, 0, 1)[..., None] ** 1.6
    arr = arr * (1 - blush * blush_strength) + np.array((240, 200, 205), dtype=np.float32) * (blush * blush_strength)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1.1, (h, w, 1)).round()
    arr = arr + noise

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def save_jpg(img, path, quality=88):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    print("  ", os.path.relpath(path, ROOT), img.size)


def load(path):
    return Image.open(path).convert("RGB")


# --------------------------------------------------------------------------
# white-matte removal for the decorative florals
# --------------------------------------------------------------------------
def white_to_alpha(img, floor=0.035, gain=1.15, gamma=0.92):
    """Return RGBA artwork with the white paper knocked out."""
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    lum = arr.min(axis=2)
    alpha = np.clip((1.0 - lum - floor) * gain, 0, 1) ** gamma
    safe = np.maximum(alpha, 1e-4)[..., None]
    rgb = arr - (1.0 - alpha[..., None])
    rgb = np.clip(rgb / safe, 0, 1)
    rgb = np.where(alpha[..., None] < 0.02, 1.0, rgb)
    out = np.concatenate([rgb, alpha[..., None]], axis=2)
    return Image.fromarray((out * 255).round().astype(np.uint8), "RGBA")


def trim_alpha(img, margin=0.02):
    alpha = np.asarray(img.getchannel("A"))
    ys, xs = np.nonzero(alpha > 12)
    if len(xs) == 0:
        return img
    pad = int(max(img.size) * margin)
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
           min(xs.max() + pad, img.width), min(ys.max() + pad, img.height))
    return img.crop(box)


def alpha_to_white(img, pad=0.02):
    """Flatten RGBA art onto warm white for the multiply-blended layers."""
    bbox = img.getbbox()
    img = img.crop(bbox) if bbox else img
    w, h = img.size
    pad_px = int(max(w, h) * pad)
    canvas = Image.new("RGB", (w + pad_px * 2, h + pad_px * 2), (255, 255, 255))
    canvas.paste(img, (pad_px, pad_px), img)
    return canvas


# --------------------------------------------------------------------------
# painted florals
# --------------------------------------------------------------------------
def gild(img):
    """Recolour watercolour art as champagne-gold foil, keeping its detail."""
    rgba = white_to_alpha(img, floor=0.03, gain=1.35, gamma=0.85)
    arr = np.asarray(rgba, dtype=np.float32) / 255.0
    rgb, alpha = arr[..., :3], arr[..., 3]
    lum = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    # map tone onto the foil ramp (deep bronze in the shadows, pale gold in the lights)
    ramp = np.array([
        [150, 101, 34], [196, 143, 62], [214, 163, 77],
        [233, 205, 150], [247, 233, 190], [252, 245, 222],
    ], dtype=np.float32)
    t = np.clip(lum * 1.25, 0, 1) * (len(ramp) - 1)
    lo = np.floor(t).astype(np.int32)
    hi = np.clip(lo + 1, 0, len(ramp) - 1)
    frac = (t - lo)[..., None]
    out = ramp[lo] * (1 - frac) + ramp[hi] * frac
    # a touch of the original hue in the deepest washes keeps it painterly
    out = out * 0.92 + rgb * 255 * 0.08
    boosted = np.clip(alpha * 1.15, 0, 1)[..., None]
    res = np.concatenate([np.clip(out, 0, 255), boosted * 255], axis=2)
    return Image.fromarray(res.round().astype(np.uint8), "RGBA")


def gold_branch(size=(1100, 900)):
    """A fine gilded botanical branch, painted with a foil gradient."""
    ss = 2
    W, H = size[0] * ss, size[1] * ss
    art = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(art)

    # gold foil gradient shared by stem and leaves
    foil = Image.new("RGB", (W, H))
    fa = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((xx / W * 0.7 + yy / H * 0.3), 0, 1)
    stops = [(0.0, (168, 118, 42)), (0.22, (233, 205, 150)), (0.45, (214, 163, 77)),
             (0.62, (247, 233, 190)), (0.82, (206, 154, 72)), (1.0, (150, 101, 34))]
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (t >= p0) & (t <= p1)
        local = ((t[m] - p0) / (p1 - p0))[:, None]
        fa[m] = np.array(c0, dtype=np.float32) * (1 - local) + np.array(c1, dtype=np.float32) * local
    fa[t < stops[0][0]] = stops[0][1]
    fa[t > stops[-1][0]] = stops[-1][1]
    foil = Image.fromarray(np.clip(fa, 0, 255).astype(np.uint8), "RGB")

    # main arc stem
    pts = []
    for i in range(120):
        u = i / 119
        x = W * (0.06 + 0.88 * u)
        y = H * (0.78 - 0.30 * math.sin(u * math.pi * 0.85) - 0.10 * u)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        width = int(W * 0.0055 * (1.0 - 0.5 * i / len(pts)) + 1)
        d.line([pts[i], pts[i + 1]], fill=255, width=width)

    # leaves along the stem, alternating sides
    rng = np.random.default_rng(4)
    for i in range(7, len(pts) - 6, 9):
        x, y = pts[i]
        bx, by = pts[min(i + 1, len(pts) - 1)]
        tangent = math.atan2(by - y, bx - x)
        for side in (-1, 1):
            a = tangent + side * (0.62 + rng.normal(0, 0.06))
            length = W * (0.045 + 0.022 * rng.random())
            width = length * 0.36
            poly = []
            steps = 16
            for k in range(steps + 1):
                tt = k / steps
                half = width * math.sin(math.pi * tt) ** 0.75
                ax = x + math.cos(a) * length * tt
                ay = y + math.sin(a) * length * tt
                nx, ny = -math.sin(a), math.cos(a)
                poly.append((ax + nx * half, ay + ny * half))
            for k in range(steps, -1, -1):
                tt = k / steps
                half = width * math.sin(math.pi * tt) ** 0.75
                ax = x + math.cos(a) * length * tt
                ay = y + math.sin(a) * length * tt
                nx, ny = -math.sin(a), math.cos(a)
                poly.append((ax - nx * half, ay - ny * half))
            d.polygon(poly, fill=255)
            # vein
            d.line([(x, y), (x + math.cos(a) * length * 0.86, y + math.sin(a) * length * 0.86)],
                   fill=255, width=max(1, int(W * 0.0012)))

    # round pods on the tips
    for i in (18, 52, 96):
        x, y = pts[i]
        d.ellipse([x - W * 0.008, y - W * 0.008, x + W * 0.008, y + W * 0.008], fill=255)

    mask = art.filter(ImageFilter.GaussianBlur(W * 0.0012))
    art = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    art.paste(foil.convert("RGBA"), (0, 0), mask)

    bbox = art.getbbox()
    art = art.crop(bbox)
    target_w = size[0] - 120
    return art.resize((target_w, int(target_w * art.height / art.width)), Image.LANCZOS)


def watercolor_wash(size=(1600, 900)):
    """Soft blush washes with paper grain — the texture behind the hero sky."""
    W, H = size
    base = np.zeros((H, W, 3), dtype=np.float32) + np.array(WHITE, dtype=np.float32)
    rng = np.random.default_rng(12)
    layers = []
    for i in range(26):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        rx, ry = rng.uniform(W * 0.10, W * 0.34), rng.uniform(H * 0.12, H * 0.42)
        tint = np.array(rng.choice([(250, 224, 228), (252, 233, 232), (246, 208, 214), (252, 240, 226)]),
                        dtype=np.float32)
        layer = Image.new("L", (W, H), 0)
        ImageDraw.Draw(layer).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
        layer = layer.filter(ImageFilter.GaussianBlur(min(rx, ry) * rng.uniform(0.35, 0.75)))
        a = np.asarray(layer, dtype=np.float32)[..., None] / 255.0 * rng.uniform(0.10, 0.26)
        base = base * (1 - a) + tint * a
        layers.append(layer)

    # faint gold flecks
    gold = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(gold)
    for i in range(240):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(0.6, 1.8)
        gd.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.uniform(30, 90)))
    gold = gold.filter(ImageFilter.GaussianBlur(0.6))
    ga = np.asarray(gold, dtype=np.float32)[..., None] / 255.0
    base = base * (1 - ga * 0.5) + np.array((214, 163, 77), dtype=np.float32) * (ga * 0.5)

    # paper grain
    noise = rng.normal(0, 2.2, (H, W, 1))
    base = base + noise
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    print("editorial stills")
    stills = [
        ("goal-weight.png", "goal-weight.jpg", (1200, 750), (0.50, 0.52), 0.012),
        ("goal-energy.png", "goal-energy.jpg", (1200, 750), (0.50, 0.52), 0.012),
        ("goal-recovery.png", "goal-recovery.jpg", (1200, 750), (0.48, 0.52), 0.010),
        ("goal-glow.png", "goal-glow.jpg", (1200, 750), (0.50, 0.50), 0.012),
        ("goal-focus.png", "goal-focus.jpg", (1200, 750), (0.52, 0.52), 0.010),
        ("goal-supplies.png", "goal-supplies.jpg", (960, 600), (0.50, 0.52), 0.010),
        ("range-lineup.png", "range-lineup.jpg", (1200, 560), (0.50, 0.50), 0.012),
        ("delivery-kenya.png", "delivery-kenya.jpg", (1400, 800), (0.50, 0.52), 0.012),
        ("hero-wellness.png", "hero-wellness.jpg", (1000, 1150), (0.50, 0.56), 0.012),
    ]
    for src, dst, size, focus, warmth in stills:
        path = os.path.join(RAW, src)
        if not os.path.exists(path):
            print("   missing", src)
            continue
        img = load(path)
        aspect = size[0] / size[1]
        img = crop_to_aspect(img, aspect, focus)
        img = img.resize(size, Image.LANCZOS)
        img = grade(img, contrast=1.035, blush=0.018, seed=hash(dst) % 97)
        save_jpg(img, os.path.join(IMG, dst))

    print("florals")
    blossom_path = os.path.join(FLORAL_RAW, "blossom-branch.png")
    if os.path.exists(blossom_path):
        blossom = load(blossom_path)
        w, h = blossom.size

        # 1. the whole branch, trimmed to its art
        art = white_to_alpha(blossom, gain=1.35, gamma=0.85)
        art = trim_alpha(art, 0.015)
        branch = alpha_to_white(art, 0.02)
        branch.thumbnail((1500, 1500), Image.LANCZOS)
        save_jpg(branch, os.path.join(FLORAL, "blossom-branch.jpg"))

        # 2. a dense flower cluster -> the peony / rose layer
        cluster = blossom.crop((int(w * 0.24), int(h * 0.05), int(w * 0.74), int(h * 0.95)))
        ca = trim_alpha(white_to_alpha(cluster, gain=1.3, gamma=0.88), 0.015)
        cl = alpha_to_white(ca, 0.02)
        cl.thumbnail((1200, 1200), Image.LANCZOS)
        save_jpg(cl, os.path.join(FLORAL, "peony-rose.jpg"))

        # 3. the trailing right-hand spray
        spray = blossom.crop((int(w * 0.50), int(h * 0.12), int(w * 0.99), int(h * 0.92)))
        sa = trim_alpha(white_to_alpha(spray, gain=1.3, gamma=0.88), 0.015)
        sp = alpha_to_white(sa, 0.02)
        sp.thumbnail((900, 900), Image.LANCZOS)
        save_jpg(sp, os.path.join(FLORAL, "rose-spray.jpg"))

        # 4. alpha-matted ghost for the burgundy panels
        ghost = trim_alpha(white_to_alpha(blossom, floor=0.02, gain=1.5, gamma=0.80), 0.01)
        ghost.thumbnail((1100, 1100), Image.LANCZOS)
        ghost.save(os.path.join(FLORAL, "blossom-ghost.webp"), "WEBP", quality=90, method=6)
        print("   florals/blossom-ghost.webp", ghost.size)

    # 5. gilded botanical branch: the blossom art, foil-toned. Keeps the fine
    #    watercolour detail while reading as a gold foil print on the page.
    if os.path.exists(blossom_path):
        gilded = gild(load(blossom_path))
        gilded = trim_alpha(gilded, 0.012)
        flat = alpha_to_white(gilded, 0.03)
        flat.thumbnail((1200, 1200), Image.LANCZOS)
        save_jpg(flat, os.path.join(FLORAL, "gold-branch.jpg"))
        alpha = gilded.copy()
        alpha.thumbnail((1000, 1000), Image.LANCZOS)
        alpha.save(os.path.join(FLORAL, "gold-branch-alpha.webp"), "WEBP", quality=90, method=6)
        print("   florals/gold-branch-alpha.webp", alpha.size)

    # 6. watercolour wash
    save_jpg(watercolor_wash((1600, 900)), os.path.join(FLORAL, "watercolor-wash.jpg"), 84)

    # 7. brand seal derivatives already exist (tools/render_brand.py)
    print("done")


if __name__ == "__main__":
    main()
