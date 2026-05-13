# Content & Pricing Layouts

10 layouts in this category. Pick by matching the message and content shape. `idx` is the **0-based** master-slide position — pass it directly to `rearrange.py`. (Slide N as numbered in PowerPoint = `idx` N-1.) Render any layout's thumbnail on demand via the snippet in `references/workflows.md`.

| Name | When to use | idx | Key shapes |
|---|---|--:|---|
| `content-2col` | Two-column compare/contrast (Pros/Cons labels). Good for trade-off slides. | 59 | title, body, "Pros", "Cons", 2x "A paragraph or bullet goes her...", date, footer, slide_number |
| `content-3col` | Three-column layout for feature triads or parallel arguments. | 61 | title, 2x body, date, footer, slide_number |
| `content-body` | Standard content slide with a title and rich body area (~5 sub-blocks). | 69 | title, 7x body, date, footer, slide_number |
| `content-large` | Dense single-slide summary with 5 body panels. Use when packing a lot onto one page. | 88 | title, 7x body, date, footer, slide_number |
| `table` | Plain table layout for tabular data. Use when you need rows-and-columns without the side-by-side comparison framing. | 90 | "READ ME THEN DELETE ME", "Optional chart icons", title, body, date, footer, slide_number |
| `comparison-table` | Comparison table layout. Use for feature-by-feature, vendor-by-vendor, or option matrices. | 91 | title, body, date, footer, slide_number |
| `pricing` | Pricing table for rate cards or plan tiers. | 99 | title, body, date, footer, slide_number |
| `cost-estimate` | Cost estimate with a team-structure breakdown. Use for staffing + cost proposals. | 100 | title, body, "Team Structure", date, footer, slide_number |
| `at-a-glance` | Dense executive 'At a glance' one-pager with ~22 slots for stats, callouts, and metrics. Use as a high-density summary. | 138 | title, 15x body, date, footer, slide_number |
| `short-headline` | Short-headline overview with two-line title + body. Use for terse 'state of X' summaries. | 139 | title, 8x body, date, footer, slide_number |
