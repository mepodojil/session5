# Slalom PPTX Reference Index

Catalog of 95 slide layouts and 80 icons. Read only the section you need; each per-category file lists ~5-15 slides.

## Quick lookup

| Need | Read |
|---|---|
| Brand colors, fonts, footer | `references/colors.md` |
| Icon catalog (PNG/SVG paths) | `references/icons.md` |
| How to assemble a deck (Workflows A/B/C, icon swap, validation) | `references/workflows.md` |
| Choosing a layout (cross-slide decision aid) | `references/selection.md` |
| Programmatic catalog (JSON) | `references/index.json` |

## Slide layouts by category

| Category | Read | Slides |
|---|---|--:|
| Openers / Covers | `references/slides/covers.md` | 13 |
| Navigation / Framing | `references/slides/navigation.md` | 23 |
| Content & Pricing Layouts | `references/slides/content.md` | 10 |
| Process & Timelines | `references/slides/process-timeline.md` | 8 |
| Concept Diagrams | `references/slides/diagrams.md` | 5 |
| Charts | `references/slides/charts.md` | 10 |
| Devices, Storytelling & About | `references/slides/devices-storytelling.md` | 15 |
| Closers & Quotes | `references/slides/closers.md` | 11 |

## Asset paths (relative to skill root)

- Master template (single source of truth): `assets/master/Slalom Template document.pptx`
- Slide extraction: `rearrange.py master.pptx out.pptx <idx>` where `idx` is **0-based** (slide N in PowerPoint = `idx` N-1)
- Text inventories: `assets/inventories/<name>.json`
- Icons: `assets/icons/<name>.png` and `assets/icons/<name>.svg`
- Thumbnails: rendered on demand via LibreOffice (see `references/workflows.md` *On-demand thumbnails*); not pre-baked.
- Reprocess script: `scripts/preprocess.sh`
