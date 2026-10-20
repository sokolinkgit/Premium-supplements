# Premium Supplements

A responsive one-page supplement storefront built with HTML, CSS and vanilla
JavaScript. The brand runs on a pearl-and-gold palette — blush pink `#F7D5D8`,
pearl pink `#FCE9E8`, warm ivory `#FFF7F0`, lacquered ruby `#A80F2D`, burgundy
`#650D21`, champagne gold `#D6A34D` and rose pink `#E99BAA` — with a
die-struck gold seal, watercolour cherry blossom, gilded botanicals and elegant
serif typography.

**Contact:** `0113 111 330` · WhatsApp `+254 113 111 330` · delivery to all 47
counties of Kenya.

## Run locally

Open `index.html` in a browser, or serve the repository root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Pages

| Page | Purpose |
| --- | --- |
| `index.html` | The storefront — hero, shop by goal, in-stock catalogue, reviews, about, contact |
| `privacy.html` | Privacy notice (no cookies, no analytics; forms hand off to WhatsApp) |
| `site.webmanifest` | Installable home-screen metadata and icons |
| `robots.txt`, `sitemap.xml` | Crawler hints (update the domain before publishing) |

## Website features

- Responsive navigation and mobile menu.
- Shop by goal: six goal tiles — weight management, energy & endurance, recovery & repair, glow & immunity, focus & performance and reconstitution supplies.
- Full in-stock catalogue (28 products: Tirzzy 5–60 mg, RETA, 5 AMINO, MOTS-C, NAD+, SS-31, BPC-157, KPV, EPITALON, TESA, GHK-CU, Glutathione, Lipo-C, SEMAX, SELANK, P141, BAC Water and Acetic Acid) with guide prices from KSh 2,000 – KSh 40,000, search and category filters.
- Product photography: every card shows its own labelled vial — gold cap, plum serif name and ruby strength pill — shot on a blush-pink sweep inside a gold hairline medallion.
- Trust strip — lab tested, premium quality, research grade, discreet shipping to all 47 counties.
- 52 verified customer reviews from all 47 counties, with search, product filter and pagination.
- Product orders and the contact form open WhatsApp with a pre-filled message.
- Country selector covering all 47 counties in Kenya.
- Tap-to-call and WhatsApp links for `0113 111 330`.
- SEO and social metadata, JSON-LD `Store` record, favicons, Apple touch icon and PWA manifest.

## Theme

The palette lives in the `:root` block of `css/style.css`: `--blush`, `--pearl`,
`--ivory`, `--gold`, `--ruby`, `--burgundy`, `--rose` and `--white` are the eight
brand-locked colours, with derived tones (`--gold-deep`, `--gold-soft`, `--ruby-deep`,
`--ink`, `--muted`, `--on-dark*`) tuned for WCAG AA contrast. Surfaces are layered CSS
gradients (`--sky`, `--surface-pearl`, `--gold-foil`, `--ruby-gloss`, `--btn-ruby`) and
elevation uses rose-and-champagne tinted shadows (`--sh-1…3`) — never black.

Typography is self-hosted from `assets/fonts/` (SIL Open Font License): Cormorant
Garamond 600 for display serif headings, Parisienne for script accents (`.script-accent`,
the hero lead line) and DM Sans for body and UI. Headlines take a lacquered ruby
finish via `.grad` (gradient-clipped text); gold foil text is available as `.foil`.

Floral decoration is composited, not stretched: white-grounded watercolour assets in
`assets/img/florals/` (cherry-blossom branch, peony & rose cluster, gilded botanical
branch, rose spray) sit in `aria-hidden` `.floral-layer` wrappers and vanish into the
pearl canvas with `mix-blend-mode: multiply`; alpha-matted WebP variants
(`blossom-ghost.webp`, `gold-branch-alpha.webp`) decorate the burgundy banners and
footer; `watercolor-wash.jpg` washes the hero sky under a mask. Every placement is
responsive (scaled with `clamp()`, pruned below 700 px) and `prefers-reduced-motion`
disables all animation. Headline words keep refreshing via `.swap-word`
(`setupWordSwaps()` in `js/main.js`), and the hero seal turns inside a double gold ring
with a slowly rotating dashed halo (`.hero-art-frame::before`, `seal-sway`).

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Page structure, content and contact links |
| `privacy.html` | Privacy notice |
| `css/style.css` | Responsive layout, components and brand theme |
| `js/main.js` | Product catalogue, category filtering, navigation and WhatsApp form |
| `assets/fonts/` | Self-hosted Cormorant Garamond, Parisienne and DM Sans (SIL OFL) |
| `assets/img/premium-supplements-logo.png` / `.webp` | The Premium Supplements seal (page logo / source art) |
| `assets/img/favicon-32.png`, `apple-touch-icon.png`, `icon-512.png` | Favicons and install icons derived from the seal |
| `assets/img/og-cover.jpg` | Social sharing card |
| `assets/img/products/` | 28 studio vial shots, one per catalogue item |
| `assets/img/goal-*.jpg` | The six "shop by goal" tiles |
| `assets/img/hero-wellness.jpg`, `delivery-kenya.jpg`, `range-lineup.jpg` | Editorial stills for the about, delivery and range panels |
| `assets/img/florals/` | Watercolour blossom, peony/rose, gilded branch and wash assets (multiply-blended; WebP alpha variants for dark panels) |
| `tools/render_brand.py` | Draws the seal, favicons and social card |
| `tools/render_vials.py` | Renders the 28 vial shots and the range line-ups |
| `tools/prepare_images.py` | Crops, grades and writes the editorial stills and florals |
| `tools/fonts/` | Label and UI typefaces for the renderers: Oswald, Parisienne, Cormorant Garamond, DM Sans (SIL OFL) |

## Regenerating the imagery

All of the imagery is generated, so it can be reproduced or re-styled without a
camera. `pillow`, `numpy`, `fonttools` and `brotli` are needed — on a managed Python
(PEP 668) use a venv:

```bash
python3 -m venv .venv-img && .venv-img/bin/pip install pillow numpy fonttools brotli

.venv-img/bin/python tools/render_brand.py      # seal, favicons, social card
.venv-img/bin/python tools/render_vials.py      # every vial shot + line-ups (~3 min)
.venv-img/bin/python tools/render_vials.py bpc-157   # one product slug
.venv-img/bin/python tools/render_vials.py --list    # show the catalogue
.venv-img/bin/python tools/prepare_images.py    # crop + grade the editorial stills, cut the florals
```

`tools/render_vials.py` parses the `products` array in `js/main.js`, so the vial
photography always mirrors the live catalogue. To add a product, append it to that
array with an `image` path of `assets/img/products/<slug>.jpg` and run the script for
that slug.

`tools/prepare_images.py` reads the art-directed source stills from
`assets/img/_raw/` and `assets/img/florals/_raw/` (kept out of Git) and writes the
final cropped, colour-graded JPEG/WebP files that ship with the site. If those sources
are missing, the committed outputs stay in place.

To regenerate the brand type from upstream, the `tools/fonts/` TTFs come from
[google/fonts](https://github.com/google/fonts) under the SIL Open Font License
(licence texts are in `tools/fonts/OFL-*.txt`); the WOFF2 files in `assets/fonts/`
are static instances of those variable fonts.

## Before publishing

- Update the placeholder domain in `index.html` (`canonical`, Open Graph),
  `robots.txt`, `sitemap.xml` and `site.webmanifest`.
- Product names and guide prices mirror the price list shared by the merchant.
  Availability changes quickly ("available while stocks last") — confirm current
  pricing, product details and stock on WhatsApp before publishing or ordering.
- Peptide products are listed for research purposes only; they are not a substitute
  for professional medical advice, and customers should consult a qualified health
  professional about suitability.
