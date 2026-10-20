#!/usr/bin/env python3
"""Render the studio vial photography for the Premium Supplements catalogue.

Every product in `js/main.js` gets its own sealed-vial studio shot: a glass
vial with a polished gold flip-off cap and crimp, a blush paper label carrying
the Premium Supplements crest, the product name in crimson serif caps, the
strength in a ruby pill, a gold spec line and the research disclaimer — shot on
a soft blush-pink sweep inside a gold hairline circle.

Usage (from the repository root):

    .venv-img/bin/python tools/render_vials.py               # everything
    .venv-img/bin/python tools/render_vials.py bpc-157       # one product slug
    .venv-img/bin/python tools/render_vials.py --composites  # line-ups only
    .venv-img/bin/python tools/render_vials.py --list        # show the catalogue

The catalogue is parsed from `js/main.js`, so the imagery always mirrors the
live product list. Requires pillow + numpy (see README).
"""
from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "products")
IMG = os.path.join(ROOT, "assets", "img")
FONTS = os.path.join(ROOT, "tools", "fonts")

SERIF = os.path.join(FONTS, "CormorantGaramond.ttf")
SANS = os.path.join(FONTS, "DMSans.ttf")
CONDENSED = os.path.join(FONTS, "Oswald.ttf")

SIZE = 900          # final image edge
SS = 2              # supersampling factor
W = SIZE * SS

# brand palette (mirrors css/style.css)
WHITE = (255, 253, 251)
IVORY = (255, 247, 240)
PEARL = (252, 233, 232)
BLUSH = (247, 213, 216)
GOLD = (214, 163, 77)
GOLD_LIGHT = (243, 227, 180)
GOLD_DEEP = (143, 98, 32)
RUBY = (168, 15, 45)
BURGUNDY = (101, 13, 33)
INK = (78, 42, 54)
MUTED = (124, 85, 96)

CATEGORY_TINT = {
    "Weight Management":      {"band": (246, 200, 211), "liquid": (231, 152, 170), "edge": (206, 120, 142)},
    "Energy & Endurance":     {"band": (248, 219, 194), "liquid": (240, 180, 122), "edge": (214, 148, 92)},
    "Recovery & Repair":      {"band": (231, 214, 226), "liquid": (198, 163, 199), "edge": (170, 132, 172)},
    "Glow & Immunity":        {"band": (248, 212, 204), "liquid": (236, 148, 134), "edge": (208, 118, 104)},
    "Focus & Performance":    {"band": (222, 219, 236), "liquid": (166, 161, 205), "edge": (136, 130, 176)},
    "Reconstitution Supplies": {"band": (218, 231, 223), "liquid": (152, 192, 174), "edge": (118, 160, 142)},
}

# strengths whose flyer name differs from the catalogue name
DISPLAY = {
    "5 AMINO": "5-AMINO",
    "P141 (PT-141)": "P141",
    "BAC Water": "BAC WATER",
}

SPEC_LINE = {
    "Weight Management": "LYOPHILISED · SINGLE VIAL",
    "Energy & Endurance": "LYOPHILISED · SINGLE VIAL",
    "Recovery & Repair": "LYOPHILISED · SINGLE VIAL",
    "Glow & Immunity": "SEALED · SINGLE VIAL",
    "Focus & Performance": "LYOPHILISED · SINGLE VIAL",
    "Reconstitution Supplies": "STERILE · SINGLE VIAL",
}


# --------------------------------------------------------------------------
# catalogue
# --------------------------------------------------------------------------
def load_catalogue():
    """Parse the `products` array out of js/main.js so imagery mirrors the site."""
    src = open(os.path.join(ROOT, "js", "main.js"), encoding="utf-8").read()
    start = src.index("const products = [")
    end = src.index("\n  ];", start)
    block = src[start:end]

    products = []
    for chunk in block.split("{\n")[1:]:
        def grab(field):
            m = re.search(rf"{field}:\s*'([^']*)'", chunk)
            return m.group(1) if m else ""

        name = grab("name")
        if not name:
            continue
        category = grab("category")
        image = grab("image")
        slug = os.path.splitext(os.path.basename(image))[0]
        products.append({"name": name, "category": category, "image": image, "slug": slug})
    return products


def split_name(name):
    """'Tirzzy 10 mg' -> ('TIRZZY', '10 mg');  'GHK-CU 50 mg' -> ('GHK-CU', '50 mg')."""
    m = re.match(r"^(.*?)\s+(\d+(?:\.\d+)?\s*(?:mg|mL|mcg|g))$", name.strip())
    if m:
        base, strength = m.group(1).strip(), m.group(2).strip()
    else:
        base, strength = name.strip(), ""
    base = DISPLAY.get(base.upper(), base)
    return base.upper(), strength


# --------------------------------------------------------------------------
# drawing helpers
# --------------------------------------------------------------------------
def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def vertical_gradient(size, top, bottom):
    w, h = size
    ramp = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    top = np.array(top, dtype=np.float32)
    bottom = np.array(bottom, dtype=np.float32)
    arr = top[None, None, :] * (1 - ramp[:, :, None]) + bottom[None, None, :] * ramp[:, :, None]
    return Image.fromarray(np.repeat(arr, w, axis=1).round().astype(np.uint8), "RGB")


def horizontal_gradient(size, stops):
    """stops: [(position 0-1, (r,g,b)), ...] left to right."""
    w, h = size
    xs = np.linspace(0, 1, w, dtype=np.float32)
    colors = np.zeros((w, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (xs >= p0) & (xs <= p1)
        t = np.clip((xs[m] - p0) / max(p1 - p0, 1e-6), 0, 1)[:, None]
        colors[m] = np.array(c0, dtype=np.float32) * (1 - t) + np.array(c1, dtype=np.float32) * t
    colors[xs < stops[0][0]] = stops[0][1]
    colors[xs > stops[-1][0]] = stops[-1][1]
    arr = np.repeat(colors[None, :, :], h, axis=0)
    return Image.fromarray(arr.round().astype(np.uint8), "RGB")


def tracked_text(draw, xy, text, fnt, fill, tracking=0.0, anchor="mm"):
    space = tracking * fnt.size
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + space * max(len(text) - 1, 0)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="l" + anchor[1])
        x += w + space
    return total


def fit_text(draw, text, path, max_w, max_size, min_size=18, weight=600, tracking=0.02):
    """Largest font size at which `text` fits `max_w`; returns (font, width)."""
    size = max_size
    while size > min_size:
        f = font(path, size, weight)
        total = sum(draw.textlength(ch, font=f) for ch in text) + tracking * size * max(len(text) - 1, 0)
        if total <= max_w:
            return f, total
        size -= 2
    f = font(path, min_size, weight)
    total = sum(draw.textlength(ch, font=f) for ch in text) + tracking * min_size * max(len(text) - 1, 0)
    return f, total


def wrap_two_lines(draw, text, path, max_w, max_size, weight=600, tracking=0.02):
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        fa, wa = fit_text(draw, a, path, max_w, max_size, weight=weight, tracking=tracking)
        fb, wb = fit_text(draw, b, path, max_w, max_size, weight=weight, tracking=tracking)
        size = min(fa.size, fb.size)
        if best is None or size > best[0]:
            best = (size, a, b)
    if not best:
        return None
    size, a, b = best
    return font(path, size, weight), a, b


def paper_grain(img, strength=2.0, seed=7):
    rng = np.random.default_rng(seed)
    arr = np.asarray(img).astype(np.int16)
    noise = rng.normal(0, strength, (arr.shape[0], arr.shape[1], 1)).round().astype(np.int16)
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8), "RGB")


def gold_gradient(size):
    return horizontal_gradient(
        size,
        [(0.0, (150, 101, 34)), (0.10, (206, 158, 84)), (0.22, (247, 229, 178)),
         (0.38, (214, 163, 77)), (0.52, (243, 227, 180)), (0.66, (198, 146, 66)),
         (0.84, (222, 178, 104)), (1.0, (150, 101, 34))],
    )


def clip_poly(mask_img, points):
    d = ImageDraw.Draw(mask_img)
    d.polygon(points, fill=255)


def bezier(p0, p1, p2, p3, steps=60):
    out = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out


# --------------------------------------------------------------------------
# the vial
# --------------------------------------------------------------------------
# geometry, expressed as fractions of W so the render rescales cleanly
G = {
    "body_half":     0.112,
    "body_top":      0.372,
    "base":          0.892,
    "neck_half":     0.0425,
    "neck_top":      0.256,
    "shoulder_top":  0.312,
    "cap_half":      0.0500,
    "cap_top":       0.112,
    "cap_shoulder":  0.202,
    "cap_bottom":    0.262,
    "label_half":    0.106,
    "label_top":     0.436,
    "label_bottom":  0.812,
    "band_h":        0.0295,
    "liquid_top":    0.806,
}

LIQUIDS = ("Reconstitution Supplies",)
LIQUID_SLUGS = ("lipo-c", "lipo-c-b12")
POWDER_TINT = {
    "ghk-cu":      (146, 176, 220),
    "glutathione": (252, 250, 244),
}


def build_sweep():
    """Blush studio sweep: pearl sky, soft horizon, warm pool of light."""
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)
    xn, yn = xx / W, yy / W

    top = np.array((255, 253, 251), dtype=np.float32)
    mid = np.array((252, 233, 232), dtype=np.float32)
    low = np.array((242, 201, 207), dtype=np.float32)
    floor = np.array((233, 185, 194), dtype=np.float32)

    v = np.clip(yn / 0.80, 0, 1)[..., None]
    arr = top + (mid - top) * np.clip(v / 0.62, 0, 1)
    arr = np.where(v > 0.62, mid + (low - mid) * np.clip((v - 0.62) / 0.38, 0, 1), arr)

    horizon = 0.895
    floor_f = np.clip((yn - horizon) / 0.11, 0, 1)[..., None] ** 0.6
    arr = arr * (1 - floor_f * 0.28) + floor * (floor_f * 0.28)

    light = np.clip(1 - np.sqrt(((xn - 0.47) / 0.46) ** 2 + ((yn - 0.40) / 0.44) ** 2), 0, 1) ** 1.6
    arr = arr * (1 - 0.60 * light[..., None]) + np.array(WHITE, dtype=np.float32) * 0.60 * light[..., None]

    # deeper blush towards the bottom edge gives the shot depth
    depth = np.clip((yn - 0.52) / 0.48, 0, 1)[..., None] ** 1.5
    arr = arr * (1 - 0.22 * depth) + np.array((228, 172, 182), dtype=np.float32) * (0.22 * depth)

    vig = np.clip(np.sqrt(((xn - 0.5) / 0.76) ** 2 + ((yn - 0.50) / 0.76) ** 2), 0, 1)[..., None] ** 2
    arr = arr * (1 - 0.07 * vig) + np.array((212, 158, 168), dtype=np.float32) * 0.07 * vig

    return paper_grain(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB"), 1.4, 3)


def glass_silhouette():
    """Mask of the vial: body, shoulder, neck."""
    m = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(m)
    cx = W // 2
    bh, nh = G["body_half"] * W, G["neck_half"] * W
    bt, st = G["body_top"] * W, G["shoulder_top"] * W
    nt, base = G["neck_top"] * W, G["base"] * W

    d.rounded_rectangle([cx - bh, bt, cx + bh, base], radius=0.024 * W, fill=255)
    # rounded shoulder: body wall -> dome -> neck
    left = bezier((cx - bh, bt + 0.004 * W), (cx - bh, st + 0.018 * W),
                  (cx - nh - 0.010 * W, st + 0.002 * W), (cx - nh, nt + 0.006 * W))
    right = bezier((cx + bh, bt + 0.004 * W), (cx + bh, st + 0.018 * W),
                   (cx + nh + 0.010 * W, st + 0.002 * W), (cx + nh, nt + 0.006 * W))
    d.polygon(left + list(reversed(right)), fill=255)
    d.rectangle([cx - nh, nt, cx + nh, st + 0.014 * W], fill=255)
    return m


def cylinder_table(r_px):
    """Per-pixel-across shading rows for a glass cylinder (left -> right)."""
    width = int(round(r_px * 2)) + 1
    x = np.clip((np.arange(width, dtype=np.float32) - (width - 1) / 2) / r_px, -1, 1)
    nz = np.sqrt(np.clip(1 - x ** 2, 0, 1))
    # broad key highlight left of centre, narrow fill and kicker on the right
    key = np.exp(-((x + 0.34) / 0.26) ** 2) * 0.85
    kicker = np.exp(-((x - 0.80) / 0.09) ** 2) * 0.55
    fill = np.exp(-((x + 0.88) / 0.07) ** 2) * 0.40
    spec = np.clip(key + kicker + fill, 0, 1)
    rim = np.clip((np.abs(x) - 0.62) / 0.38, 0, 1) ** 1.6
    return (0.68 + 0.32 * nz), spec, rim


def draw_shadow(canvas):
    cx = W // 2
    shadow = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(shadow)
    d.ellipse([cx - 0.245 * W, 0.856 * W, cx + 0.245 * W, 0.918 * W], fill=210)
    shadow = shadow.filter(ImageFilter.GaussianBlur(0.026 * W))
    canvas.paste(Image.new("RGB", (W, W), (178, 122, 132)), (0, 0), shadow.point(lambda v: int(v * 0.62)))

    cast = Image.new("L", (W, W), 0)
    cd = ImageDraw.Draw(cast)
    cd.polygon([(cx + 0.06 * W, 0.876 * W), (cx + 0.38 * W, 0.892 * W),
                (cx + 0.38 * W, 0.906 * W), (cx + 0.02 * W, 0.892 * W)], fill=75)
    cast = cast.filter(ImageFilter.GaussianBlur(0.024 * W))
    canvas.paste(Image.new("RGB", (W, W), (176, 118, 130)), (0, 0), cast.point(lambda v: int(v * 0.75)))
    return canvas


def vial_layer(category, style_color):
    """Glass, contents and highlights painted inside the silhouette only."""
    cx = W // 2
    bh = G["body_half"] * W
    bt, base = G["body_top"] * W, G["base"] * W
    nt = G["neck_top"] * W

    mask = glass_silhouette()
    m = np.asarray(mask, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)

    shade, spec, rim = cylinder_table(bh)
    def row(values):
        row = np.zeros(W, dtype=np.float32)
        lo = int(round(cx - (len(values) - 1) / 2))
        for i, val in enumerate(values):
            x = lo + i
            if 0 <= x < W:
                row[x] = val
        return row

    shade_row, spec_row, rim_row = row(shade), row(spec), row(rim)

    # ---- glass base: a cool translucent tint, darker at the silhouette ----
    arr = np.zeros((W, W, 3), dtype=np.float32)
    glass = np.array((232, 224, 228), dtype=np.float32)
    arr[:] = glass[None, None, :] * shade_row[None, :, None]

    # ---- contents ----
    if style_color is None:
        # lyophilised cake: a soft cream plug settled in the heel
        cake_top = base - 0.098 * W
        dome = np.clip(1 - ((xx - cx) / (bh * 0.90)) ** 2, 0, 1) ** 0.30
        plug = np.clip((yy - (cake_top + 0.012 * W * (1 - dome))) / (0.004 * W), 0, 1) * dome
        cake = np.array((252, 249, 240), dtype=np.float32)[None, None, :]
        arr = arr * (1 - plug[..., None] * 0.95) + cake * (plug[..., None] * 0.95)
        # a soft shadow line under the puck and crumb texture across its top
        rng = np.random.default_rng(11)
        grains = rng.normal(0, 4, (W, W, 1)).astype(np.float32)
        arr = arr + grains * np.clip((yy - cake_top) / (0.06 * W), 0, 1)[..., None] * 0.9
        arr = arr * (1 - 0.10 * plug[..., None] * np.clip((yy - (cake_top + 0.006 * W)) / (0.02 * W), 0, 1)[..., None])
    else:
        liq_top = G["liquid_top"] * W if category in LIQUIDS else base - 0.055 * W
        liquid = np.clip((yy - liq_top) / (0.010 * W), 0, 1)
        depth = np.clip((yy - liq_top) / (0.06 * W), 0, 1)
        lcol = np.array(style_color, dtype=np.float32)[None, None, :] * (0.82 + 0.18 * shade_row[None, :, None])
        lcol = lcol * (0.94 + 0.06 * (1 - depth[..., None]))
        arr = arr * (1 - liquid[..., None] * 0.85) + lcol * (liquid[..., None] * 0.85)
        meniscus = np.exp(-((yy - liq_top) / (0.005 * W)) ** 2) * liquid
        arr = arr + meniscus[..., None] * np.array((255, 252, 246), dtype=np.float32) * 0.55

    # ---- table sheen + inner rim light ----
    arr = arr + spec_row[None, :, None] * 82
    arr = arr * (1 - rim_row[None, :, None] * 0.30) + np.array((186, 152, 160), dtype=np.float32) * (rim_row[None, :, None] * 0.30)

    arr = arr * m[..., None]
    layer = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    return layer, mask


def stroke_mask(mask, width_px):
    """A thin outline hugging the mask edge."""
    grown = mask.filter(ImageFilter.MaxFilter(width_px * 2 + 1))
    inner = mask.filter(ImageFilter.MinFilter(width_px * 2 + 1))
    edge = Image.fromarray(np.clip(np.asarray(grown, dtype=np.int16) - np.asarray(inner, dtype=np.int16), 0, 255).astype(np.uint8))
    return edge


def draw_label(canvas, base, strength, category):
    """Blush pearl label laid out top-down, with a gold frame and blush band."""
    tint = CATEGORY_TINT.get(category, CATEGORY_TINT["Weight Management"])
    cx = W // 2
    half = G["label_half"] * W
    top = G["label_top"] * W
    bottom = G["label_bottom"] * W
    band_h = G["band_h"] * W

    x0, x1 = int(cx - half), int(cx + half)
    y0, y1 = int(top), int(bottom)
    pw, ph = x1 - x0, y1 - y0

    # ---- paper with a cylindrical fall-off to both edges ----
    paper = vertical_gradient((pw, ph), (255, 255, 253), (253, 245, 241))
    prof = np.clip((np.arange(pw, dtype=np.float32) - (pw - 1) / 2) / (pw / 2), -1, 1)
    nz = np.sqrt(np.clip(1 - prof ** 2, 0, 1))
    parr = np.asarray(paper, dtype=np.float32) * (0.80 + 0.20 * nz)[None, :, None]
    parr = np.clip(parr, 0, 255)
    # bevel: bright top edge, soft shadow along the bottom of the paper
    parr[: max(1, int(0.0020 * W))] = np.minimum(parr[: max(1, int(0.0020 * W))] + 14, 255)
    parr[-max(1, int(0.0035 * W)):] *= 0.965
    paper = paper_grain(Image.fromarray(parr.astype(np.uint8), "RGB"), 1.2, abs(hash(base)) % 9973)
    canvas.paste(paper, (x0, y0))

    # a hairline of shadow where the paper meets the glass
    d0 = ImageDraw.Draw(canvas)
    d0.line([(x0, y0), (x0, y1)], fill=(226, 194, 196), width=max(1, int(0.0010 * W)))
    d0.line([(x1, y0), (x1, y1)], fill=(222, 190, 194), width=max(1, int(0.0010 * W)))

    d = ImageDraw.Draw(canvas)
    hair = max(1, int(0.0014 * W))
    inset = 0.009 * W
    frame_bottom = bottom - band_h - inset * 0.55
    d.rectangle([cx - half + inset, top + inset, cx + half - inset, frame_bottom],
                outline=(212, 160, 76), width=hair)

    # ---- vertical layout: measured from the top of the paper ----
    content_w = (half - inset - 0.010 * W) * 2
    crest_r = 0.0255 * W
    name_size = int(0.049 * W)
    name_font, _ = fit_text(d, base, SERIF, content_w, name_size, 22, weight=600, tracking=0.02)
    word_f = font(SANS, int(0.0125 * W), 700)
    spec_f = font(SANS, int(0.0098 * W), 700)
    fine_f = font(SANS, int(0.0078 * W), 500)
    pill_f = font(SANS, int(0.0155 * W), 700)
    pill_h = 0.0285 * W

    spec_h = 0.0105 * W
    fine_h = 0.0105 * W
    gaps = dict(crest=0.012 * W, word=0.016 * W, name=0.020 * W, pill=0.014 * W, spec=0.012 * W)
    block_h = (
        crest_r * 2 + gaps["crest"]
        + 0.016 * W + gaps["word"]
        + 0.010 * W + gaps["name"]
        + (pill_h + gaps["pill"] if strength else 0)
        + spec_h + gaps["spec"]
        + fine_h * 2
    )
    area_top, area_bottom = top + inset + 0.012 * W, frame_bottom - 0.012 * W
    y = area_top + max((area_bottom - area_top - block_h) / 2, 0)

    # crest roundel
    cy = y + crest_r
    d.ellipse([cx - crest_r, cy - crest_r, cx + crest_r, cy + crest_r], fill=(252, 233, 232),
              outline=(198, 148, 72), width=hair)
    d.ellipse([cx - crest_r + 0.0042 * W, cy - crest_r + 0.0042 * W,
               cx + crest_r - 0.0042 * W, cy + crest_r - 0.0042 * W], outline=(228, 194, 138), width=max(1, hair // 2))
    d.text((cx, cy + 0.001 * W), "PS", font=font(SERIF, int(0.0305 * W), 600), fill=BURGUNDY, anchor="mm")
    y += crest_r * 2 + gaps["crest"]

    # wordmark
    tracked_text(d, (cx, y + 0.008 * W), "PREMIUM SUPPLEMENTS", word_f, GOLD_DEEP, 0.19, "mm")
    y += 0.016 * W + gaps["word"]

    # gold rule with diamond
    ry = y + 0.005 * W
    for sign in (-1, 1):
        d.line([(cx + sign * 0.014 * W, ry), (cx + sign * 0.056 * W, ry)], fill=(212, 160, 76), width=hair)
    dr = 0.0052 * W
    d.polygon([(cx, ry - dr), (cx + dr * 0.70, ry), (cx, ry + dr), (cx - dr * 0.70, ry)], fill=(206, 158, 78))
    y += 0.010 * W + gaps["name"]

    # product name
    tracked_text(d, (cx, y + name_font.size * 0.42), base, name_font, BURGUNDY, 0.02, "mm")
    y += name_font.size * 0.84

    # strength pill
    if strength:
        pw_pill = sum(d.textlength(ch, font=pill_f) for ch in strength) + 0.030 * W
        py = y + pill_h * 0.5
        d.rounded_rectangle([cx - pw_pill / 2, py - pill_h / 2, cx + pw_pill / 2, py + pill_h / 2],
                            radius=pill_h / 2, fill=(174, 17, 62), outline=(224, 186, 122), width=max(1, hair // 2))
        d.text((cx, py + 0.0007 * W), strength, font=pill_f, fill=(255, 247, 240), anchor="mm")
        y += pill_h + gaps["pill"]

    # spec line
    tracked_text(d, (cx, y + spec_h * 0.45), SPEC_LINE.get(category, "SINGLE VIAL"),
                 spec_f, MUTED, 0.10, "mm")
    y += spec_h + gaps["spec"]

    # fine print, shrunk to sit comfortably inside the frame
    for i, (line, track) in enumerate((
        ("PREMIUM SUPPLEMENTS · NAIROBI, KENYA", 0.07),
        ("RESEARCH USE ONLY · NOT FOR HUMAN CONSUMPTION", 0.05),
    )):
        f, _ = fit_text(d, line, SANS, content_w - 0.006 * W, int(0.0078 * W),
                        5, weight=500, tracking=track)
        tracked_text(d, (cx, y + fine_h * (0.45 + i * 1.0)), line, f, (152, 112, 120), track, "mm")

    # ---- blush band with gold hem ----
    band_top = bottom - band_h
    canvas.paste(Image.new("RGB", (pw, int(band_h)), tint["band"]), (x0, int(band_top)))
    d = ImageDraw.Draw(canvas)
    d.line([(x0, band_top), (x1, band_top)], fill=(212, 160, 76), width=max(1, int(0.0016 * W)))
    tracked_text(d, (cx, band_top + band_h / 2 + 0.0008 * W), "PREMIUM SUPPLEMENTS",
                 font(SANS, int(0.0086 * W), 700), (106, 62, 26), 0.22, "mm")

    # ---- subtle glass sheen across the paper ----
    sheen = Image.new("L", (W, W), 0)
    sd = ImageDraw.Draw(sheen)
    sd.polygon([(cx - 0.066 * W, top), (cx - 0.044 * W, top),
                (cx - 0.056 * W, bottom), (cx - 0.080 * W, bottom)], fill=34)
    sd.polygon([(cx + 0.074 * W, top), (cx + 0.082 * W, top),
                (cx + 0.092 * W, bottom), (cx + 0.082 * W, bottom)], fill=22)
    sheen = sheen.filter(ImageFilter.GaussianBlur(0.014 * W))
    canvas.paste(Image.new("RGB", (W, W), (255, 255, 255)), (0, 0), sheen)
    return canvas


def draw_cap(canvas):
    """Polished gold flip-off cap: shell, crimp collar, top disc."""
    cx = W // 2
    half = G["cap_half"] * W
    top = G["cap_top"] * W
    shoulder = G["cap_shoulder"] * W
    bottom = G["cap_bottom"] * W

    cap = Image.new("L", (W, W), 0)
    cd = ImageDraw.Draw(cap)
    cd.rounded_rectangle([cx - half * 0.94, top, cx + half * 0.94, shoulder], radius=0.008 * W, fill=255)
    cd.rounded_rectangle([cx - half, shoulder - 0.005 * W, cx + half, bottom], radius=0.005 * W, fill=255)
    cm = np.asarray(cap, dtype=np.float32)[..., None] / 255.0

    prof = np.clip((np.arange(W, dtype=np.float32) - cx) / half, -1, 1)
    nz = np.sqrt(np.clip(1 - prof ** 2, 0, 1))
    gold = np.array((204, 156, 76), dtype=np.float32)[None, :] * (0.60 + 0.40 * nz[:, None])
    gold = gold + np.array((58, 42, 16), dtype=np.float32)[None, :] * (nz[:, None] ** 7)
    key = np.exp(-((prof + 0.36) / 0.22) ** 2) * 170
    kicker = np.exp(-((prof - 0.82) / 0.07) ** 2) * 105
    gold = gold + (key + kicker)[:, None] * np.array((1.0, 0.92, 0.72), dtype=np.float32)[None, :]

    arr = np.asarray(canvas, dtype=np.float32).copy()
    arr = arr * (1 - cm * 0.98) + gold[None, :, :] * (cm * 0.98)

    yy = np.arange(W, dtype=np.float32)[:, None]
    crimp = np.exp(-((yy - (shoulder - 0.003 * W)) / (0.005 * W)) ** 2) * cm
    arr = arr * (1 - crimp * 0.30)
    floor_shadow = np.exp(-((yy - (bottom - 0.004 * W)) / (0.006 * W)) ** 2) * cm
    arr = arr * (1 - floor_shadow * 0.30)
    canvas = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    # crimp serrations clipped to the collar
    serr = Image.new("L", (W, W), 0)
    sd = ImageDraw.Draw(serr)
    n = 13
    for i in range(-n // 2, n // 2 + 1):
        x = cx + i * (half * 2 / n)
        sd.line([(x, shoulder + 0.001 * W), (x, bottom - 0.002 * W)], fill=255, width=max(1, int(0.0013 * W)))
    serr = Image.composite(serr, Image.new("L", (W, W), 0), cap)
    canvas.paste(Image.new("RGB", (W, W), (118, 76, 22)), (0, 0), serr.point(lambda v: int(v * 0.30)))

    # top disc, flush with the shell
    d = ImageDraw.Draw(canvas)
    disc = [cx - half * 0.94, top - 0.007 * W, cx + half * 0.94, top + 0.029 * W]
    d.ellipse(disc, fill=(231, 194, 122))
    d.ellipse([disc[0] + 0.005 * W, disc[1] + 0.006 * W, disc[2] - 0.005 * W, disc[3] - 0.008 * W], fill=(246, 222, 168))
    d.arc([disc[0] + 0.009 * W, disc[1] + 0.007 * W, disc[2] - 0.009 * W, disc[3] - 0.003 * W],
          205, 335, fill=(255, 250, 226), width=max(1, int(0.0032 * W)))
    d.ellipse(disc, outline=(146, 98, 32), width=max(1, int(0.0020 * W)))

    # cap shadow on the neck
    sh = Image.new("L", (W, W), 0)
    ImageDraw.Draw(sh).ellipse([cx - half, bottom - 0.006 * W, cx + half, bottom + 0.014 * W], fill=175)
    sh = sh.filter(ImageFilter.GaussianBlur(0.005 * W))
    canvas.paste(Image.new("RGB", (W, W), (142, 100, 90)), (0, 0), sh.point(lambda v: int(v * 0.5)))
    return canvas


def render_vial(product, framed=True):
    canvas = build_sweep()
    canvas = draw_shadow(canvas)
    mask = glass_silhouette()

    category = product["category"]
    slug = product["slug"]
    if category in LIQUIDS or slug in LIQUID_SLUGS:
        style = {"lipo-c": (238, 196, 108), "lipo-c-b12": (236, 176, 92)}.get(slug, (246, 244, 238))
    else:
        style = None

    layer, mask = vial_layer(category, style)
    # glass thickness: a fine outline and an inner highlight just inside the edge
    edge = stroke_mask(mask, max(1, int(0.0016 * W)))
    canvas.paste(layer, (0, 0), mask)
    canvas.paste(Image.new("RGB", (W, W), (196, 158, 158)), (0, 0), edge.point(lambda v: int(v * 0.55)))
    inner_light = Image.fromarray(np.clip(np.asarray(mask, dtype=np.int16) - np.asarray(stroke_mask(mask, max(1, int(0.006 * W))), dtype=np.int16), 0, 255).astype(np.uint8))
    canvas.paste(Image.new("RGB", (W, W), (255, 252, 246)), (0, 0), inner_light.point(lambda v: int(v * 0.55)))

    # powder colour for the lyophilised cake is painted over the glass layer
    if style is None and slug in POWDER_TINT:
        cake = Image.new("L", (W, W), 0)
        top = G["base"] * W - 0.070 * W
        ImageDraw.Draw(cake).ellipse([W // 2 - 0.112 * W, top, W // 2 + 0.112 * W, G["base"] * W - 0.006 * W], fill=255)
        cake = Image.composite(cake, Image.new("L", (W, W), 0), mask)
        cake = cake.filter(ImageFilter.GaussianBlur(0.004 * W))
        canvas.paste(Image.new("RGB", (W, W), POWDER_TINT[slug]), (0, 0), cake.point(lambda v: int(v * 0.75)))

    base, strength = split_name(product["name"])
    canvas = draw_label(canvas, base, strength, category)
    canvas = draw_cap(canvas)

    canvas = paper_grain(canvas, 1.0, abs(hash(slug)) % 9973)
    if framed:
        # medallion treatment: white surround with a gold hairline circle
        ring = Image.new("RGB", (W, W), WHITE)
        disc = Image.new("L", (W, W), 0)
        ImageDraw.Draw(disc).ellipse([0, 0, W - 1, W - 1], fill=255)
        canvas.paste(ring, (0, 0), Image.eval(disc, lambda v: 255 - v))
        d = ImageDraw.Draw(canvas)
        d.ellipse([1, 1, W - 2, W - 2], outline=(214, 163, 77), width=max(1, int(0.0030 * W)))
    return canvas.resize((SIZE, SIZE), Image.LANCZOS)


# --------------------------------------------------------------------------
# composites
# --------------------------------------------------------------------------
def load_vial(slug):
    path = os.path.join(OUT, f"{slug}.jpg")
    return Image.open(path).convert("RGB") if os.path.exists(path) else None


def make_lineup(slugs, size, catalogue):
    """A row of vials standing on one continuous blush sweep."""
    Wc, Hc = size
    bg = build_sweep().resize((Wc, Hc), Image.LANCZOS)

    by_slug = {p["slug"]: p for p in catalogue}
    crops = []
    for slug in slugs:
        if slug not in by_slug:
            continue
        v = render_vial(by_slug[slug], framed=False)
        # a full-height crop keeps every vial on the same horizon
        crops.append(v.crop((int(v.width * 0.24), int(v.height * 0.03),
                             int(v.width * 0.76), v.height)))
    if not crops:
        return bg

    n = len(crops)
    aspect = crops[0].width / crops[0].height
    overlap = 0.34 if n > 3 else 0.20
    vh = int(Hc * 0.97)
    vw = int(vh * aspect)
    step = int(vw * (1 - overlap))
    total = step * (n - 1) + vw
    if total > Wc:
        scale = Wc / total
        vh, vw, step = int(vh * scale), int(vw * scale), int(step * scale)
        total = step * (n - 1) + vw
    x = (Wc - total) // 2
    y = Hc - vh

    for crop in crops:
        im = crop.resize((vw, vh), Image.LANCZOS).convert("RGBA")
        ramp = np.ones(vw, dtype=np.float32)
        f = max(int(vw * 0.12), 1)
        ramp[:f] = np.linspace(0, 1, f) ** 1.3
        ramp[-f:] = np.linspace(1, 0, f) ** 1.3
        alpha = np.repeat(ramp[None, :], vh, axis=0)
        im.putalpha(Image.fromarray((alpha * 255).astype(np.uint8), "L"))
        bg.paste(im, (x, y), im)
        x += step

    return paper_grain(bg, 1.1, 5)


def main(argv):
    catalogue = load_catalogue()
    if "--list" in argv:
        for p in catalogue:
            print(f"{p['slug']:18s} {p['category']:26s} {p['name']}")
        return

    os.makedirs(OUT, exist_ok=True)
    composite_only = "--composites" in argv
    wanted = [a for a in argv if not a.startswith("--")]
    slugs = [p["slug"] for p in catalogue]

    if not composite_only:
        for p in catalogue:
            if wanted and p["slug"] not in wanted:
                continue
            print("rendering", p["slug"], flush=True)
            render_vial(p).save(os.path.join(OUT, f"{p['slug']}.jpg"), quality=88, optimize=True)

    if wanted:
        return

    print("rendering composites", flush=True)
    make_lineup([s for s in ["tirzzy-10", "reta-10", "bpc-157", "mots-10", "ghk-cu"] if s in slugs],
                (1200, 540), catalogue).save(os.path.join(IMG, "range-lineup.jpg"), quality=88, optimize=True)
    make_lineup([s for s in ["bac-water-5", "bac-water-10", "acetic-acid"] if s in slugs],
                (900, 620), catalogue).save(os.path.join(IMG, "goal-supplies.jpg"), quality=88, optimize=True)


if __name__ == "__main__":
    main(sys.argv[1:])
