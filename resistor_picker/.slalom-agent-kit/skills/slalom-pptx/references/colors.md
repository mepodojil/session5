# Brand Colors, Fonts, Footer

Use `<a:schemeClr val="accentN"/>` references in OOXML so colors track theme overrides.
Use Arial as a web-safe fallback when PptxGenJS can't load Avenir Next LT Pro.

## Color Scheme

| Scheme | Hex | Slalom Name | Role |
|---|---|---|---|
| dk1 | #000000 | Black | Text/foreground |
| dk2 | #666666 | Dark Gray | Secondary text |
| lt2 | #E6E6E6 | Light Gray | Secondary background |
| accent1 | #0C62FB | Slalom Blue | Primary accent |
| accent2 | #002FAF | Dark Blue | Secondary accent |
| accent3 | #1BE1F2 | Cyan | Accent 3 |
| accent4 | #FF4D5F | Coral Red | Accent 4 |
| accent5 | #C7B9FF | Purple | Accent 5 |
| accent6 | #DEFF4D | Chartreuse | Accent 6 |
| hlink | #0C62FB | Slalom Blue | Hyperlink |
| folHlink | #0C62FB | Slalom Blue | Followed hyperlink |

## Fonts

- Body: theme font `+mn-lt` (Avenir Next LT Pro, Arial fallback)
- Headings: theme font `+mj-lt` (Avenir Next LT Pro, Arial fallback)

## Footer

Standard footer text on all body slides:

> Slalom. All Rights Reserved. Proprietary and Confidential.

## Date format

Default format for the system `DATE` placeholder on body slides: **`yyyy`** (4 chars; e.g. `2026`). The master's `DATE` placeholder is only ~0.28" wide — wider formats (`dd/mm/yyyy`, `mm/yy`, etc.) wrap onto two lines or overflow into the footer. The master ships `2025` as the stale default; replace with the actual deck-delivery year.

Cover slides use a different placeholder (a regular `BODY`) for any month/year eyebrow line — the `yyyy` rule applies only to the system `DATE` placeholder on body slides.

## DATE / FOOTER as a composite footer line

`DATE` (`x≈1.51"`) and `FOOTER` (`x=1.80"`) are two independent placeholders abutted at a fixed 0.01" gap. There's no shape grouping anchoring them, so they look like one continuous footer line *only* when the DATE content stays at ≤4 characters. Anything longer breaks the visual continuity. Treat them as a composite: keep DATE short (default `yyyy`) and let FOOTER carry the brand string.
