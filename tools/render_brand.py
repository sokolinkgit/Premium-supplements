#!/usr/bin/env python3
"""Render the Premium Supplements brand seal, favicons and social card.

Everything is drawn procedurally at 2x and downsampled, so the wordmark,
laurel and gold rings stay crisp at any size. Run from the repository root:

    .venv-img/bin/python tools/render_brand.py

Outputs
    assets/img/premium-supplements-logo.png    1200 x 1200 seal (page logo)
    assets/img/premium-supplements-logo.webp    800 x 800 seal (header / hero)
    assets/img/favicon-32.png                     32 x 32 favicon
    assets/img/apple-touch-icon.png              180 x 180 iOS icon
    assets/img/icon-512.png                      512 x 512 PWA icon
    assets/img/og-cover.jpg                     1200 x 630 social card
"""
from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
FONTS = os.path.join(ROOT, "tools", "fonts")

SERIF = os.path.join(FONTS, "CormorantGaramond.ttf")
SANS = os.path.join(FONTS, "DMSans.ttf")
SCRIPT = os.path.join(FONTS, "Parisienne-Regular.ttf")

# brand palette (mirrors css/style.css)
PEARL = (252, 233, 232)
IVORY = (255, 247, 240)
BLUSH = (247, 213, 216)
WHITE = (255, 253, 251)
GOLD = (214, 163, 77)
GOLD_LIGHT = (243, 227, 180)
GOLD_DEEP = (143, 98, 32)
RUBY = (168, 15, 45)
BURGUNDY = (101, 13, 33)
MUTED = (124, 85, 96)


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
def vertical_gradient(size, top, bottom):
    w, h = size
    ramp = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    top = np.array(top, dtype=np.float32)
    bottom = np.array(bottom, dtype=np.float32)
    arr = top[None, None, :] * (1 - ramp[:, :, None]) + bottom[None, None, :] * ramp[:, :, None]
    arr = np.repeat(arr, w, axis=1)
    return Image.fromarray(arr.round().astype(np.uint8), "RGB")


def diagonal_gradient(size, stops):
    """stops: [(x0,y0,color), ...] interpolated along the top-left -> bottom-right diagonal."""
    w, h = size
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    t = np.clip((xs + ys) / 2, 0, 1)
    positions = [s[0] for s in stops]
    colors = [np.array(s[1], dtype=np.float32) for s in stops]
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        lo, hi = positions[i], positions[i + 1]
        local = np.clip((t - lo) / max(hi - lo, 1e-6), 0, 1)[..., None]
        seg = colors[i] * (1 - local) + colors[i + 1] * local
        arr = np.where((t >= lo)[..., None] & (t <= hi)[..., None], seg, arr)
    arr[t <= positions[0]] = colors[0]
    arr[t >= positions[-1]] = colors[-1]
    return Image.fromarray(arr.round().astype(np.uint8), "RGB")


def gradient_masked(size, gradient, mask):
    return Image.composite(gradient, Image.new("RGB", size, WHITE), mask)


def add_paper_grain(img, strength=2.4, seed=7):
    rng = np.random.default_rng(seed)
    arr = np.asarray(img).astype(np.int16)
    noise = rng.normal(0, strength, (arr.shape[0], arr.shape[1], 1)).round().astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def font(path, size, weight=None, opsz=None):
    f = ImageFont.truetype(path, size)
    try:
        axes = {}
        if weight is not None:
            axes["wght"] = weight
        if opsz is not None:
            axes["opsz"] = opsz
        if axes:
            f.set_variation_by_axes(list(axes.values()))
    except Exception:
        pass
    return f


def tracked_text(draw, xy, text, fnt, fill, tracking=0, anchor="mm"):
    """Draw text with letter tracking; tracking is a fraction of the font size."""
    space = tracking * fnt.size
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + space * (len(text) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="l" + anchor[1])
        x += w + space
    return total


def tracked_mask(size, xy, text, fnt, tracking=0.12, anchor="mm"):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    tracked_text(d, xy, text, fnt, 255, tracking, anchor)
    return mask


def leaf_polygon(cx, cy, angle, length, width):
    """A pointed laurel leaf growing from (cx, cy) toward `angle` radians."""
    pts_a, pts_b = [], []
    steps = 18
    for i in range(steps + 1):
        t = i / steps
        taper = math.sin(math.pi * t) ** 0.78
        half = width * taper
        along = length * t
        x = cx + math.cos(angle) * along
        y = cy + math.sin(angle) * along
        nx, ny = -math.sin(angle), math.cos(angle)
        pts_a.append((x + nx * half, y + ny * half))
        pts_b.append((x - nx * half, y - ny * half))
    return pts_a + pts_b[::-1]


def draw_laurel(mask, center, radius, start_deg, end_deg, leaves, length, width, direction=1):
    """A branch of laurel leaves. direction=+1 walks counter-clockwise (left
    branch, growing upward), -1 walks clockwise (right branch)."""
    cx, cy = center
    d = ImageDraw.Draw(mask)
    angles = np.linspace(math.radians(start_deg), math.radians(end_deg), leaves)
    for i, a in enumerate(angles):
        x = cx + math.cos(a) * radius
        y = cy + math.sin(a) * radius
        tangent = a + direction * math.pi / 2
        scale = 0.74 + 0.26 * math.sin(math.pi * (i + 0.35) / max(leaves + 0.7, 1))
        d.polygon(leaf_polygon(x, y, tangent, length * scale, width * scale), fill=255)


def diamond(draw, xy, r, fill):
    x, y = xy
    draw.polygon([(x, y - r), (x + r * 0.62, y), (x, y + r), (x - r * 0.62, y)], fill=fill)


def gold_foil(size):
    return diagonal_gradient(
        size,
        [
            (0.0, (180, 130, 58)),
            (0.18, (233, 205, 150)),
            (0.38, (214, 163, 77)),
            (0.55, (247, 233, 190)),
            (0.72, (214, 163, 77)),
            (1.0, (168, 118, 42)),
        ],
    )


def gold_ink(size):
    """Slightly deeper foil for fine line-work so leaves stay visible on pearl."""
    return diagonal_gradient(
        size,
        [(0.0, (150, 101, 34)), (0.35, (196, 143, 62)), (0.7, (214, 163, 77)), (1.0, (160, 108, 38))],
    )


def ruby_gloss(size):
    return vertical_gradient(size, (209, 64, 94), BURGUNDY)


# --------------------------------------------------------------------------
# the seal
# --------------------------------------------------------------------------
def render_seal(size=1200):
    ss = 2  # supersample
    S = size * ss
    canvas = Image.new("RGB", (S, S), WHITE)

    # ---- pearl ground with a warm blush heart ----
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    cx = cy = S / 2
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (S * 0.72)
    glow = np.clip(1 - dist, 0, 1) ** 1.5
    top = np.array(WHITE, dtype=np.float32)
    edge = np.array([250, 219, 222], dtype=np.float32)
    arr = edge[None, None, :] + (top - edge)[None, None, :] * glow[:, :, None]
    # a soft blush crescent in the lower right
    crescent = np.clip(1 - np.sqrt((xx - S * 0.78) ** 2 + (yy - S * 0.82) ** 2) / (S * 0.55), 0, 1) ** 2
    arr = arr * (1 - 0.28 * crescent[:, :, None]) + np.array(BLUSH, dtype=np.float32) * (0.28 * crescent[:, :, None])
    ground = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    canvas.paste(ground, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # ---- rings ----
    ring = Image.new("L", (S, S), 0)
    rd = ImageDraw.Draw(ring)
    rd.ellipse([S * 0.035, S * 0.035, S * 0.965, S * 0.965], outline=255, width=int(3.2 * ss))
    rd.ellipse([S * 0.052, S * 0.052, S * 0.948, S * 0.948], outline=255, width=int(1.1 * ss))
    canvas.paste(gold_foil((S, S)), (0, 0), ring)

    # dashed inner halo
    halo = Image.new("L", (S, S), 0)
    hd = ImageDraw.Draw(halo)
    hr = S * 0.452
    for deg in range(0, 360, 6):
        a0 = math.radians(deg)
        a1 = math.radians(deg + 2.6)
        hd.arc([cx - hr, cy - hr, cx + hr, cy + hr], deg, deg + 2.6, fill=255, width=int(1.4 * ss))
    canvas.paste(gold_foil((S, S)), (0, 0), halo)

    # tiny gold beads between the rings
    bead = Image.new("L", (S, S), 0)
    bd = ImageDraw.Draw(bead)
    br = S * 0.485
    for deg in range(0, 360, 15):
        a = math.radians(deg)
        bx, by = cx + math.cos(a) * br, cy + math.sin(a) * br
        bd.ellipse([bx - 2.2 * ss, by - 2.2 * ss, bx + 2.2 * ss, by + 2.2 * ss], fill=255)
    canvas.paste(gold_foil((S, S)), (0, 0), bead)

    # ---- laurel wreath around the monogram ----
    wreath_cy = S * 0.432
    wreath_r = S * 0.181
    laurel = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(laurel)
    # a fine stem under the leaves
    for start, end in ((104, 256), (76, -76)):
        bbox = [cx - wreath_r, wreath_cy - wreath_r, cx + wreath_r, wreath_cy + wreath_r]
        d.arc(bbox, start, end, fill=255, width=int(1.3 * ss))
    draw_laurel(laurel, (cx, wreath_cy), wreath_r, 104, 256, 9, S * 0.058, S * 0.0185, direction=1)
    draw_laurel(laurel, (cx, wreath_cy), wreath_r, 76, -76, 9, S * 0.058, S * 0.0185, direction=-1)
    canvas.paste(gold_ink((S, S)), (0, 0), laurel)

    # veins in the leaves
    vein = Image.new("L", (S, S), 0)
    vd = ImageDraw.Draw(vein)
    for start, end, direction in ((104, 256, 1), (76, -76, -1)):
        n = 9
        for i, a_deg in enumerate(np.linspace(start, end, n)):
            a = math.radians(a_deg)
            x = cx + math.cos(a) * wreath_r
            y = wreath_cy + math.sin(a) * wreath_r
            tangent = a + direction * math.pi / 2
            scale = 0.74 + 0.26 * math.sin(math.pi * (i + 0.35) / (n + 0.7))
            ex = x + math.cos(tangent) * S * 0.056 * scale
            ey = y + math.sin(tangent) * S * 0.056 * scale
            vd.line([(x, y), (ex, ey)], fill=150, width=int(0.9 * ss))
    canvas.paste(gold_ink((S, S)), (0, 0), vein)

    # monogram disc: a pearl plate inside the wreath
    plate = Image.new("L", (S, S), 0)
    pd = ImageDraw.Draw(plate)
    pr = S * 0.152
    pd.ellipse([cx - pr, wreath_cy - pr, cx + pr, wreath_cy + pr], fill=255)
    plate_grad = vertical_gradient((S, S), WHITE, (250, 224, 223))
    canvas = Image.composite(plate_grad, canvas, plate)
    draw = ImageDraw.Draw(canvas)
    pd2 = ImageDraw.Draw(canvas)
    pd2.ellipse(
        [cx - pr, wreath_cy - pr, cx + pr, wreath_cy + pr],
        outline=(206, 160, 96),
        width=int(1.5 * ss),
    )

    # monogram "PS" in lacquered burgundy
    mono_font = font(SERIF, int(S * 0.185), weight=600)
    mono_mask = tracked_mask((S, S), (cx, wreath_cy + S * 0.006), "PS", mono_font, tracking=0.01, anchor="mm")
    # shrink tracking measurement: tracked_mask centers by glyph widths, good enough
    mono_mask = mono_mask.filter(ImageFilter.GaussianBlur(0.4 * ss))
    mono_grad = vertical_gradient((S, S), (206, 61, 92), (96, 11, 31))
    # gold offset halo behind the monogram
    halo_mask = mono_mask.filter(ImageFilter.MaxFilter(int(5 * ss) // 2 * 2 + 1))
    canvas.paste((236, 207, 149), (0, 0), halo_mask)
    canvas.paste(mono_grad, (0, 0), mono_mask)

    # ---- wordmark ----
    word_font = font(SERIF, int(S * 0.094), weight=600)
    word_mask = tracked_mask((S, S), (cx, S * 0.715), "PREMIUM", word_font, tracking=0.135)
    word_grad = vertical_gradient((S, S), (188, 40, 68), BURGUNDY)
    canvas.paste(word_grad, (0, 0), word_mask)

    sub_font = font(SANS, int(S * 0.036), weight=700)
    sub_mask = tracked_mask((S, S), (cx, S * 0.788), "SUPPLEMENTS", sub_font, tracking=0.3)
    sub_grad = vertical_gradient((S, S), (168, 118, 42), (128, 84, 24))
    canvas.paste(sub_grad, (0, 0), sub_mask)

    # flanking diamonds + hairlines either side of SUPPLEMENTS
    line = Image.new("L", (S, S), 0)
    ld = ImageDraw.Draw(line)
    sub_w = S * 0.362
    for sign in (-1, 1):
        x0 = cx + sign * (sub_w / 2 + S * 0.018)
        x1 = cx + sign * (sub_w / 2 + S * 0.072)
        ld.line([(x0, S * 0.788), (x1, S * 0.788)], fill=255, width=int(1.1 * ss))
        diamond(ld, (cx + sign * (sub_w / 2 + S * 0.09), S * 0.788), 4.2 * ss, 255)
    canvas.paste(gold_foil((S, S)), (0, 0), line)

    # gold rule with center diamond
    rule = Image.new("L", (S, S), 0)
    rg = ImageDraw.Draw(rule)
    ry = S * 0.838
    rg.line([(cx - S * 0.20, ry), (cx + S * 0.20, ry)], fill=255, width=int(1.0 * ss))
    diamond(rg, (cx, ry), 5.4 * ss, 255)
    canvas.paste(gold_foil((S, S)), (0, 0), rule)

    tag_font = font(SANS, int(S * 0.0235), weight=600)
    tag_mask = tracked_mask((S, S), (cx, S * 0.882), "RESEARCH · QUALITY · RESULTS", tag_font, tracking=0.26)
    tag_tint = Image.new("RGB", (S, S), MUTED)
    canvas.paste(tag_tint, (0, 0), tag_mask)

    # ---- finishing: grain, vignette, edge light ----
    canvas = add_paper_grain(canvas, strength=2.0)

    vig = Image.new("L", (S, S), 0)
    vg = ImageDraw.Draw(vig)
    vg.ellipse([-S * 0.15, -S * 0.15, S * 1.15, S * 1.15], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(S * 0.06))
    shadow = Image.new("RGB", (S, S), (196, 160, 162))
    canvas = Image.composite(canvas, shadow, vig)

    # circular crop with a champagne hairline
    crop = Image.new("L", (S, S), 0)
    ImageDraw.Draw(crop).ellipse([0, 0, S - 1, S - 1], fill=255)
    out = Image.new("RGB", (S, S), (255, 253, 251))
    out.paste(canvas, (0, 0), crop)

    out = out.resize((size, size), Image.LANCZOS)
    # add a crisp outer gold ring after downsampling
    d = ImageDraw.Draw(out)
    d.ellipse([1, 1, size - 2, size - 2], outline=(214, 163, 77), width=max(1, size // 400))
    return out


def circular(seal, size, ring=(214, 163, 77)):
    """The square seal cropped to its disc, with a transparent surround."""
    s = seal.resize((size, size), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([1, 1, size - 2, size - 2], fill=255)
    s.putalpha(mask)
    d = ImageDraw.Draw(s)
    d.ellipse([1, 1, size - 2, size - 2], outline=ring, width=max(2, size // 300))
    return s


def render_social_card(seal):
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), IVORY)
    # blush gradient
    grad = diagonal_gradient(
        (W, H),
        [(0.0, (255, 247, 240)), (0.45, (252, 233, 232)), (1.0, (247, 213, 216))],
    )
    card.paste(grad, (0, 0))

    # soft radial pearl light behind the seal
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    light = np.clip(1 - np.sqrt((xx - 930) ** 2 + (yy - 315) ** 2) / 420, 0, 1) ** 1.4
    arr = np.asarray(card).astype(np.float32)
    arr = arr * (1 - 0.55 * light[:, :, None]) + np.array(WHITE, dtype=np.float32) * 0.55 * light[:, :, None]
    card = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    d = ImageDraw.Draw(card)
    # gold hairline frame first, art sits inside it
    d.rectangle([26, 26, W - 27, H - 27], outline=(214, 163, 77), width=2)
    d.rectangle([36, 36, W - 37, H - 37], outline=(233, 205, 150), width=1)

    disc = circular(seal, 420)
    # a soft drop shadow under the seal
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).ellipse([948 - 210, 315 - 190, 948 + 210, 315 + 220], fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    card.paste(Image.new("RGB", (W, H), (196, 150, 158)), (0, 0), sh)
    card.paste(disc, (948 - 210, 315 - 210), disc)

    script = font(SCRIPT, 74)
    d.text((92, 158), "Premium quality,", font=script, fill=RUBY, anchor="ls")
    title = font(SERIF, 96, weight=600)
    d.text((88, 262), "Premium", font=title, fill=BURGUNDY, anchor="ls")
    d.text((88, 356), "Supplements", font=title, fill=BURGUNDY, anchor="ls")

    tracked_text(d, (92, 415), "RESEARCH · QUALITY · RESULTS", font(SANS, 22, weight=700), GOLD_DEEP, 0.24, "lm")
    d.line([(92, 452), (452, 452)], fill=(214, 163, 77), width=1)
    tracked_text(d, (92, 492), "IN-STOCK RANGE · DELIVERED ACROSS KENYA", font(SANS, 20, weight=500), MUTED, 0.12, "lm")
    tracked_text(d, (92, 530), "CALL OR WHATSAPP  0113 111 330", font(SANS, 24, weight=700), RUBY, 0.08, "lm")

    return add_paper_grain(card, strength=1.6)


def main():
    os.makedirs(IMG, exist_ok=True)
    seal = render_seal(1200)
    seal.save(os.path.join(IMG, "premium-supplements-logo.png"), optimize=True)
    seal.resize((800, 800), Image.LANCZOS).save(
        os.path.join(IMG, "premium-supplements-logo.webp"), "WEBP", quality=92, method=6
    )
    seal.resize((512, 512), Image.LANCZOS).save(os.path.join(IMG, "icon-512.png"), optimize=True)
    seal.resize((180, 180), Image.LANCZOS).save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)
    seal.resize((32, 32), Image.LANCZOS).save(os.path.join(IMG, "favicon-32.png"), optimize=True)
    render_social_card(seal).save(os.path.join(IMG, "og-cover.jpg"), quality=88, optimize=True)
    print("brand seal, icons and social card written to assets/img/")


if __name__ == "__main__":
    main()
