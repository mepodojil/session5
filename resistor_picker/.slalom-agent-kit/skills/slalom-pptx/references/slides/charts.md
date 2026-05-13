# Charts

10 layouts in this category. Pick by matching the message and content shape. `idx` is the **0-based** master-slide position — pass it directly to `rearrange.py`. (Slide N as numbered in PowerPoint = `idx` N-1.) Render any layout's thumbnail on demand via the snippet in `references/workflows.md`.

| Name | When to use | idx | Key shapes |
|---|---|--:|---|
| `chart-bar` | Single-series bar graph. Use for ranked comparisons across categories. | 109 | title, 2x body, date, footer, slide_number |
| `chart-bar-grouped` | Grouped bar graph (multiple labels per row). Use for multi-series ranked comparisons. | 110 | title, 5x body, date, footer, slide_number |
| `chart-bar-multi` | Multi-series bar graph with several bars stacked horizontally per category. Use when you have 3+ series across a few categories (e.g., quarterly KPI trends across 4 metrics) — denser than chart-bar-grouped, less paired-comparison than chart-bar-comparison. | 111 | title, 4x body, date, footer, slide_number |
| `chart-bar-comparison` | Side-by-side comparison bar graph. Use to contrast two or more groups directly. | 112 | title, 5x body, date, footer, slide_number |
| `chart-pie` | Pie chart. Use for share-of-total at a glance (small N segments). | 115 | title, "Subtitle necupta ius consequ o...", "Optional subheadline", "Beremod maximusaesto dunt labo...", date, footer, slide_number |
| `chart-doughnut` | Doughnut chart. Modern alternative to a pie chart with center text space. | 116 | title, "Subtitle necupta ius consequ o...", "Optional subheadline", "Item one", date, footer, slide_number |
| `chart-doughnut-comparison` | Three doughnut charts side-by-side with subheadlines under each. Use for before/middle/after share-of-total comparisons or three-scenario projections; pick chart-doughnut for a single ring with center text. | 117 | title, 4x "Subheadline", date, footer, slide_number |
| `chart-line` | Line graph. Use for time-series trends. | 118 | title, 2x body, date, footer, slide_number |
| `chart-waterfall` | Waterfall chart. Use for cost build-ups, budget walks, or running totals. | 119 | title, 5x body, date, footer, slide_number |
| `chart-stacked-column` | Stacked column graph. Use for parts-of-whole over multiple time periods or categories. | 120 | title, 2x body, date, footer, slide_number |
