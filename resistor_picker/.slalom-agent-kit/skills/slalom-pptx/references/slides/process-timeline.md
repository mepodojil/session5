# Process & Timelines

8 layouts in this category. Pick by matching the message and content shape. `idx` is the **0-based** master-slide position — pass it directly to `rearrange.py`. (Slide N as numbered in PowerPoint = `idx` N-1.) Render any layout's thumbnail on demand via the snippet in `references/workflows.md`.

| Name | When to use | idx | Key shapes |
|---|---|--:|---|
| `chevron-4` | Four-step chevron with bullet list under each step. Real CHEVRON auto-shapes; sequential left-to-right flow with multi-line detail per step. | 92 | title, body, 4x "Sample text", 4x "Optional Subheadline", date, footer, slide_number |
| `bullets-4-cols` | Four-column bullets layout with horizontal divider bars at the top. Use for parallel multi-bullet content without implying sequential flow. (Not a chevron despite the master title 'Chevron process'.) | 93 | title, body, 4x "Optional Subheadline", date, footer, slide_number |
| `process-visual` | Pipeline/intake flow with a TARGET endpoint (reactive intake -> pursuit -> engagement). | 95 | title, body, "TARGET", "Reactive Intake", "Pursuit", "Initial engagement", "Portfolio – Key Account", 4x "Bulleted list example", "Prioritize by # of yes answers", "Proactive Account Intake", "Sales Executive", 3x "Team involvement text", 3x "Timeframe text", 2x "Market Focus: Lorem Ipsum", date, footer, slide_number |
| `gantt-chart` | Gantt chart with swim-lanes and go-live milestones. Use for multi-track delivery plans. | 94 | title, body, "Dash 1 Go-Live", "Dash 2 Go-Live", "Dash 3 Go-Live", "Dash 4-5 Go-Live", "Risk Gate 1", "Risk Gate 2", "Risk Gate 3", date, footer, slide_number |
| `timeline-weekly` | Weekly timeline (short horizon). Use for sprint or cadence plans. | 96 | title, date, footer, slide_number |
| `timeline-8week` | Eight-week timeline. Use for pilots or phase-0 engagements. | 97 | title, date, footer, slide_number |
| `timeline-quarterly` | Quarterly roadmap with sprints and releases. Use for quarter+ horizons. | 98 | title, 4x "Development Sprints", 3x "Enhance and Operate", 3x "Release", "Deliverables", date, footer, slide_number |
| `flowchart` | Branching flowchart with decision points. Use for approval trees or conditional logic. | 113 | title, 2x body, date, footer, slide_number |
