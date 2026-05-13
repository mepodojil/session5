# Choosing a layout

Cross-slide decision aid. Use this to triage by content shape; once you've picked a candidate, read its row in the per-category file (`references/slides/<category>.md`) for the visual differentiator from siblings, then load its inventory (`assets/inventories/<name>.json`) before writing replacement JSON.

This file is a flat triage list, not a deep tree. Find your content shape, read the recommendations, and follow up to the per-slide `when_to_use` for the final pick. When in doubt between near-twins, render thumbnails on demand (see *On-demand thumbnails* in `workflows.md`) and eyeball the differences.

## Openers (covers)

| Content shape | Pick |
|---|---|
| Text-only, single concept, no logo or partner | `cover-basic` (idx 13) |
| Need a second opener (back cover, mid-deck section title) | `cover-basic-alt` (idx 14) |
| Co-branded with one partner, partner logo prominent | `cover-partner` (idx 15) |
| Co-branded variant with a different layout | `cover-partner-alt` (idx 16) |
| Visual-led; the image sets the tone | `cover-image` (idx 17) or `cover-image-2..6` (idx 18-22) — compare per-slide `when_to_use` for image position / overlay treatment |
| Multi-partner alliance (logos featured prominently) | `partner-logo-lockup-1..3` (idx 170-172) |

## Navigation / framing

| Content shape | Pick |
|---|---|
| Table of contents (chapter list) | `contents` (idx 23) or `contents-alt` (idx 24) |
| Time-boxed meeting agenda | `agenda` (idx 25) |
| Narrative agenda framing (more prose than time-blocks) | `agenda-summary` (idx 26) |
| Presentation overview with subheadlines | `overview` (idx 27) |
| "Our understanding of your situation" framing | `our-understanding` (idx 28) |
| "Together we've created great things" partnership intro | `together-intro` (idx 29) |
| Team intros (people on the call) | `team-intro` / `team-intro-2` / `team-intro-3` (idx 30-32) — compare per-slide |
| Single-person bio card | `bio-card` (idx 121) |
| Neutral section divider (low-key chapter break) | `section-divider` / `section-divider-alt` (idx 33-34) |
| High-contrast colored section break | `section-divider-color` / `-color-2..5` (idx 35-39) |
| Counting off chapters (01, 02, 03, ...) | `section-divider-numbered-1..5` (idx 40-44) — one per chapter |

## Content slides

| Content shape | Pick |
|---|---|
| Pros/cons or two-side compare | `content-2col` (idx 59) |
| Three parallel arguments or feature triad | `content-3col` (idx 61) |
| Standard content with title + rich body (~5 sub-blocks) | `content-body` (idx 69) |
| Dense single-slide summary (~5 panels) | `content-large` (idx 88) |
| Plain rows-and-columns table | `table` (idx 90) |
| Feature/vendor comparison matrix | `comparison-table` (idx 91) |
| Rate card / plan tiers | `pricing` (idx 99) |
| Cost estimate with team-structure breakdown | `cost-estimate` (idx 100) |
| Executive "at a glance" one-pager (~22 stat slots) | `at-a-glance` (idx 138) |
| Terse "state of X" with two-line title | `short-headline` (idx 139) |

## Process & flow

| Content shape | Pick |
|---|---|
| Sequential 4-step flow with detail per step | `chevron-4` (idx 92) — real CHEVRON auto-shapes |
| Parallel content in 4 columns of bullets | `bullets-4-cols` (idx 93) — NOT a chevron despite master title |
| Branching flow with decision points | `flowchart` (idx 113) |
| Pipeline/intake with TARGET endpoint | `process-visual` (idx 95) |
| Multi-track delivery plan with go-live milestones | `gantt-chart` (idx 94) |
| Sprint/cadence plan, weekly horizon | `timeline-weekly` (idx 96) |
| Pilot or phase-0, 8-week horizon | `timeline-8week` (idx 97) |
| Quarterly+ roadmap with sprints and releases | `timeline-quarterly` (idx 98) |

## Concept diagrams

| Content shape | Pick |
|---|---|
| 3-part hub-and-spoke framework | `diagram-3-icons` (idx 101) |
| 4-quadrant or 4-pillar model | `diagram-4-icons` (idx 102) |
| 5-part framework | `diagram-5-icons` (idx 103) |
| 6-item one-pager (3x2 grid around a center label) | `diagram-6-icons` (idx 104) |
| Three-circle Venn (role / capability intersections) | `venn-diagram` (idx 114) |

## Charts

| Content shape | Pick |
|---|---|
| Single-series ranked comparison | `chart-bar` (idx 109) |
| Multi-series grouped bars (multiple labels per row) | `chart-bar-grouped` (idx 110) |
| High-density categorical comparison | `chart-bar-multi` (idx 111) |
| Side-by-side comparison of 2+ groups | `chart-bar-comparison` (idx 112) |
| Share-of-total at a glance (small N segments) | `chart-pie` (idx 115) |
| Modern share-of-total with center text space | `chart-doughnut` (idx 116) |
| Before/after share-of-total | `chart-doughnut-comparison` (idx 117) |
| Time-series trend | `chart-line` (idx 118) |
| Cost build-up / budget walk / running totals | `chart-waterfall` (idx 119) |
| Parts-of-whole over time periods | `chart-stacked-column` (idx 120) |

## Devices & storytelling

| Content shape | Pick |
|---|---|
| Screenshot or mockup in a device shell | `device-frame-1..4` (idx 105-108) — all four have iPhone PICTURE overlap; effective body width ~6.5", not 7.97"/7.0" the inventory reports |
| "Storytelling Templates" section opener | `storytelling-intro` (idx 133) |
| Customer outcome with a stat hero | `customer-outcome-1` (idx 134) |
| Customer outcome with a quote hero | `customer-outcome-2` (idx 135) |
| Customer outcome with a diagram hero | `customer-outcome-3` (idx 136) |
| Customer outcome with a solutions hero | `customer-outcome-4` (idx 137) |
| Single Page Response Overview cover | `spro-cover` (idx 140) |
| SPRO content body | `spro-template` (idx 141) |
| About-Slalom boilerplate | `about-slalom-1..4` (idx 144-147) — compare densities |

## Closers & quotes

| Content shape | Pick |
|---|---|
| Pull quote / testimonial (text-only) | `quote` (idx 129), or `quote-2..4` (idx 130-132) — compare per-slide attribution treatment |
| Closing slide listing 5 team contacts | `closing-connect` (idx 149) |
| Thank-you sign-off | `thank-you-1..5` (idx 150-154) — each ships with different stock imagery; if the photo doesn't fit your context, use Workflow C to swap the image |
| Final copyright / disclaimer page | `copyright` (idx 156) — always last |

## When two layouts look similar

Render thumbnails for both and compare. The on-demand thumbnail flow in `workflows.md` produces side-by-side previews in seconds:

```bash
TMP=$(mktemp -d) && trap 'rm -rf "$TMP"' EXIT
python3 "$PPTX_DIR/legacy/rearrange.py" \
    "assets/master/Slalom Template document.pptx" "$TMP/preview.pptx" 18,19
python3 "$PPTX_DIR/modern/thumbnail.py" "$TMP/preview.pptx" "$TMP/thumb" --cols 2
# -> $TMP/thumb.jpg
```

If the per-slide `when_to_use` doesn't surface the differentiator clearly, that's a doc bug — file it. The catalog should make near-twin choices obvious without forcing a render.
