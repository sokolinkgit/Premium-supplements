# Blossom Wellness

A responsive one-page wellness website built with HTML, CSS and vanilla JavaScript.
The visual language follows the Blossom Wellness TIRZZY KPV poster: a luxurious,
feminine atelier of blush pink `#F7D5D8`, pearl pink `#FCE9E8`, warm ivory `#FFF7F0`
and soft white `#FFFDFB`, lacquered ruby `#A80F2D` and burgundy `#650D21` headlines,
champagne gold `#D6A34D` foil details, rose pink `#E99BAA` petals — watercolor cherry
blossom, peonies, roses and gilded botanical branches layered over soft CSS gradient
skies, with delicate gold hairlines, pearl-white panels, elegant serif typography and
tasteful script accents.

## Run locally

Open `index.html` in a browser, or serve the repository root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Website features

- Responsive navigation and mobile menu.
- Shop by goal: six goal tiles — weight management, energy & endurance, recovery & repair, glow & immunity, focus & performance and reconstitution supplies.
- Full In-Stock catalogue (28 products mirroring the Blossom Wellness In-Stock flyer: Tirzzy 5–60 mg, RETA, 5 AMINO, MOTS-C, NAD+, SS-31, BPC-157, KPV, EPITALON, TESA, GHK-CU, Glutathione, Lipo-C, SEMAX, SELANK, P141, BAC Water and Acetic Acid) with guide prices from KSh 2,000 – KSh 40,000, search and category filters.
- Studio product photography: every card shows its own labelled vial — gold cap, crimson serif name and magenta strength pill, like the flyer — on a blush-pink sweep.
- Trust strip — lab tested, premium quality, research grade, discreet shipping to all 47 counties.
- 52 verified customer reviews from all 47 counties, with search, product filter and pagination.
- Product orders and the contact form open WhatsApp with a pre-filled message.
- Country selector covering all 47 counties in Kenya.
- Tap-to-call and WhatsApp links for `0720 580 031`.

## Theme

The palette lives in the `:root` block of `css/style.css`: `--blush`, `--pearl`,
`--ivory`, `--gold`, `--ruby`, `--burgundy`, `--rose` and `--white` are the eight
brand-locked colours, with derived tones (`--gold-deep`, `--gold-soft`, `--ruby-deep`,
`--ink`, `--muted`, `--on-dark*`) tuned for WCAG AA contrast. Surfaces are layered CSS
gradients (`--sky`, `--surface-pearl`, `--gold-foil`, `--ruby-gloss`, `--btn-ruby`) and
elevation uses rose-and-champagne tinted shadows (`--sh-1…3`) — never black.

Typography is self-hosted from `assets/fonts/` (SIL Open Font License): Cormorant
Garamond 600 for display serif headings, Parisienne for script accents (`.script-accent`,
the hero lead line) and DM Sans for body and UI. Headlines take the poster's lacquered
ruby finish via `.grad` (gradient-clipped text); gold foil text is available as `.foil`.

Floral decoration is composited, not stretched: optimised watercolor assets in
`assets/img/florals/` (cherry-blossom branch, peony & rose cluster, gold botanical
branch, rose spray on white grounds) sit in `aria-hidden` `.floral-layer` wrappers and
vanish into the pearl canvas with `mix-blend-mode: multiply`; alpha-matted WebP
variants (`blossom-ghost.webp`, `gold-branch-alpha.webp`) decorate the burgundy banners
and footer; `watercolor-wash.jpg` washes the hero sky under a mask. Every placement is
responsive (scaled with `clamp()`, pruned below 700 px) and `prefers-reduced-motion`
disables all animation. Headline words keep refreshing via `.swap-word`
(`setupWordSwaps()` in `js/main.js`), and the hero seal turns inside a double gold ring
with a slowly rotating dashed halo (`.hero-art-frame::before`, `seal-sway`).

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Page structure, content and contact links |
| `css/style.css` | Responsive layout, components and brand theme |
| `js/main.js` | Product catalogue, category filtering, navigation and WhatsApp form |
| `assets/fonts/` | Self-hosted Cormorant Garamond, Parisienne and DM Sans (SIL OFL) |
| `assets/img/florals/` | Watercolor blossom, peony/rose, gold-branch and wash assets (multiply-blended; WebP alpha variants for dark panels) |
| `assets/img/blossom-wellness-logo.webp` / `.png` | The Blossom Wellness seal (page logo / favicon) |
| `assets/img/products/` | 28 studio vial shots, one per catalogue item |
| `assets/img/range-lineup.jpg`, `assets/img/goal-supplies.jpg` | Vial line-ups for the range banner and the supplies goal tile |
| `tools/render_vials.py` | Renders all of the vial photography |
| `tools/fonts/` | Label typefaces for the renderer: Oswald, Parisienne, Cormorant Garamond (SIL OFL) |

## Regenerating the vial photography

The product shots are rendered, not photographed. `tools/render_vials.py` models a
glass vial with a polished gold flip-off cap and crimp and rose solution showing in
the heel and shoulder, prints the flyer's label on it (gold lotus, the gold
"Blossom / WELLNESS" wordmark, the product name in crimson serif caps, the strength
in a magenta pill, a gold spec line, the research disclaimer and a blush band with a
gold foil hem) and lights it as a studio shot on a blush-pink sweep, like the
Blossom Wellness flyer. Only the blush band hue follows the product's category.
`pillow` and `numpy` are needed — on a managed Python (PEP 668) use a venv:

```bash
python3 -m venv .venv-img && .venv-img/bin/pip install pillow numpy
.venv-img/bin/python tools/render_vials.py               # every product + line-ups (~90 s)
.venv-img/bin/python tools/render_vials.py bpc-157       # one product slug
.venv-img/bin/python tools/render_vials.py --composites  # line-up shots only
.venv-img/bin/python tools/render_vials.py --list        # show the catalogue
```

To add a product, append it to `PRODUCTS` in the script (the slug becomes the file
name), point the matching entry in `js/main.js` at `assets/img/products/<slug>.jpg`
and run the script for that slug.

Product names and guide prices mirror the current In-Stock price list shared by the merchant. Availability changes quickly ("available while stocks last") — confirm current pricing, product details and stock on WhatsApp before publishing or ordering. Peptide products are listed for research purposes only; they are not a substitute for professional medical advice, and customers should consult a qualified health professional about suitability.
