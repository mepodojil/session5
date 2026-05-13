# Navigation / Framing

23 layouts in this category. Pick by matching the message and content shape. `idx` is the **0-based** master-slide position — pass it directly to `rearrange.py`. (Slide N as numbered in PowerPoint = `idx` N-1.) Render any layout's thumbnail on demand via the snippet in `references/workflows.md`.

| Name | When to use | idx | Key shapes |
|---|---|--:|---|
| `contents` | Table of contents. Lists chapters before diving in. | 23 | title, date, footer, slide_number |
| `contents-alt` | Numbered table-of-contents with right-aligned page numbers, book-style. Use when the deck has discrete numbered chapters and the audience needs an at-a-glance map; pick `contents` for a more visual TOC. | 24 | title, date, footer, slide_number |
| `agenda` | Meeting agenda with time-boxed items. | 25 | title, body, date, footer, slide_number |
| `agenda-summary` | 'Summarize your agenda' framing slide. Use when agenda is more narrative than time-boxed. | 26 | title, "Not all agendas are bullet lis...", date, footer, slide_number |
| `overview` | Presentation overview with subheadline blocks. Primes the audience on what follows. | 27 | title, body, "Presentation contents", 4x "Optional subheadline", "©", date, footer, slide_number |
| `our-understanding` | 'Our understanding' framing slide. Use to demonstrate you've heard the client's situation before pitching. | 28 | title, body, 3x "One line subheadline", date, footer, slide_number |
| `together-intro` | 'Together, we've created great things' partnership intro. Use for established-client check-ins or extension pitches. | 29 | title, body, "2019", "2020", "2021", "2022 and beyond", 10x "Header / DateLorem ipsum dolo...", date, footer, slide_number |
| `team-intro` | Team introduction slide. Use to present the people on the call. | 30 | title, date, footer, slide_number |
| `team-intro-2` | Team-intro variant on a white field with light-blue accent (less ink than team-intro). Use when the headshots and bios are the focus and you want minimum visual competition from the slide chrome. | 31 | title, date, footer, slide_number |
| `team-intro-3` | Team-intro variant with a divided light/dark blue background. Use when the team has two distinct sub-groups (e.g., Slalom team + client team) that benefit from a visual split. | 32 | title, date, footer, slide_number |
| `section-divider` | Neutral section divider with a small intro-text block under the title. Use when the section break needs a one-line subtitle to set up what follows. | 33 | center_title, 5x body |
| `section-divider-alt` | Full-bleed dark blue section divider with title only (no intro text). Use when you want maximum visual break and the section title speaks for itself. | 34 | center_title, 5x body |
| `section-divider-color` | Full-bleed color divider in Slalom Blue (accent1). High-contrast visual reset. Pick this when the section is the headline color of the deck; pick a -color-N variant when the section maps to a different brand accent. | 35 | body, title |
| `section-divider-color-2` | Full-bleed color divider in Cyan (accent3). Use when the section's theme maps to cyan in your color story (often: data, tech, momentum). | 36 | body, title |
| `section-divider-color-3` | Full-bleed color divider in Coral Red (accent4). Use when the section's theme maps to coral red (often: risk, urgency, customer). | 37 | body, title |
| `section-divider-color-4` | Full-bleed color divider in Purple (accent5). Use when the section's theme maps to purple (often: people, culture, creative). | 38 | body, title |
| `section-divider-color-5` | Full-bleed color divider in Chartreuse (accent6). Use when the section's theme maps to chartreuse (often: growth, sustainability, energy). | 39 | body, title |
| `section-divider-numbered-1` | Numbered chapter divider 01 on a solid Slalom Blue background. Use as the first chapter of a long deck; the numbered series 1-5 is intended to be used in order, but the visual treatment varies (1-3 are solid colors, 4-5 are nature photos). | 40 | 2x body |
| `section-divider-numbered-2` | Numbered chapter divider 02 with a cyan diagonal pattern. Use as chapter 2 in the numbered series — pairs with -1's solid blue. | 41 | 2x body |
| `section-divider-numbered-3` | Numbered chapter divider 03 on a solid coral red background. Use as chapter 3 in the numbered series — high-contrast warm tone breaks up the cool-blue feel of -1 and -2. | 42 | 2x body |
| `section-divider-numbered-4` | Numbered chapter divider 04 with a purple aerial-clouds photograph. Use as chapter 4 in the numbered series — visual treatment shifts from solid color to nature photography here. | 43 | 2x body |
| `section-divider-numbered-5` | Numbered chapter divider 05 with a green farmland aerial photograph. Use as the final chapter (5) in the numbered series — completes the photo-pair with -4 for a closing nature beat. | 44 | 2x body |
| `bio-card` | Single-person bio card with name, pronouns slot, and headshot area. Use for individual speaker intros. | 121 | "READ ME THEN DELETE ME", "Example consultant profile", 5x body, title, date, footer, slide_number |
