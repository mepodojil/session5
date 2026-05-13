"""Slide map: the single source of truth for which master slides become extracted templates.

Each entry has:
    name          file stem used for slides/<name>.pptx, inventories/<name>.json, thumbnails/<name>.png
    idx           0-indexed slide number in assets/master/Slalom Template document.pptx
                  (rearrange.py uses 0-based indices)
    category      one of CATEGORIES; drives which references/slides/<category>.md the entry lands in
    when_to_use   short prose describing the trigger for picking this layout

Add new entries here, then run scripts/preprocess.sh to extract them and regenerate references/.
"""

from dataclasses import dataclass


CATEGORIES = (
    "covers",
    "navigation",
    "content",
    "process-timeline",
    "diagrams",
    "charts",
    "devices-storytelling",
    "closers",
)

CATEGORY_LABELS = {
    "covers": "Openers / Covers",
    "navigation": "Navigation / Framing",
    "content": "Content & Pricing Layouts",
    "process-timeline": "Process & Timelines",
    "diagrams": "Concept Diagrams",
    "charts": "Charts",
    "devices-storytelling": "Devices, Storytelling & About",
    "closers": "Closers & Quotes",
}


@dataclass(frozen=True)
class SlideEntry:
    name: str
    idx: int
    category: str
    when_to_use: str


SLIDE_MAP: tuple[SlideEntry, ...] = (
    # --- Covers ---
    SlideEntry("cover-basic", 13, "covers",
               "Clean text-only deck opener with title + subtitle."),
    SlideEntry("cover-basic-alt", 14, "covers",
               "Alternate basic cover. Use when the deck needs a second opener (back cover, section)."),
    SlideEntry("cover-partner", 15, "covers",
               "Opener co-branded with a partner (logo slot included). Use for joint-venture or alliance decks."),
    SlideEntry("cover-partner-alt", 16, "covers",
               "Co-branded cover on white with a yellow accent stripe at left and partner-logo slot. "
               "Use when cover-partner's blue-heavy treatment feels too dense or formal — the white field reads as more open and consultative."),
    SlideEntry("cover-image", 17, "covers",
               "Cover with a full-bleed image area on the right. The default master image is generic; swap via Workflow C if the photo doesn't match your context. "
               "Use when visuals set the tone and you want a custom photo, not stock."),
    SlideEntry("cover-image-2", 18, "covers",
               "Image cover with a warm sunrise / mountain-silhouette photo. "
               "Use for nature, sustainability, journey, or new-beginning themes — the warm tone contrasts with the rest of the cover-image set, which is mostly cool blue."),
    SlideEntry("cover-image-3", 19, "covers",
               "Image cover with a blue blurred-motion transit photo. "
               "Use for momentum, transformation, speed-of-change, or transit/logistics themes."),
    SlideEntry("cover-image-4", 20, "covers",
               "Image cover with a blue circuit-board pattern. "
               "Use for technology, infrastructure, platform, or systems-engineering themes — pattern reads as 'large-scale, designed'."),
    SlideEntry("cover-image-5", 21, "covers",
               "Image cover with a blue microchip / circuitry close-up. "
               "Use for hardware, semiconductors, low-level computing, or precision-engineering themes — closer crop than cover-image-4 reads as 'detail, expertise'."),
    SlideEntry("cover-image-6", 22, "covers",
               "Image cover with a blue solar-panel / clean-energy pattern. "
               "Use for sustainability, clean-energy, ESG, or climate themes — the only cover-image variant with explicit renewable-energy imagery."),
    SlideEntry("partner-logo-lockup-1", 170, "covers",
               "Partner logo lockup on a white field with a single partner column and a blue gradient accent. "
               "Use as a 'deck featuring partner X' opener when one alliance is the headline."),
    SlideEntry("partner-logo-lockup-2", 171, "covers",
               "Partner logo lockup with a multi-partner grid (about a dozen logos) on a white-to-blue gradient. "
               "Use when the deck speaks to a portfolio of alliances rather than one named partner."),
    SlideEntry("partner-logo-lockup-3", 172, "covers",
               "Partner logo lockup with a denser multi-partner grid in a more uniform layout. "
               "Use for industry-coalition or partner-program decks where the count of partners is the story."),

    # --- Navigation / Framing ---
    SlideEntry("contents", 23, "navigation",
               "Table of contents. Lists chapters before diving in."),
    SlideEntry("contents-alt", 24, "navigation",
               "Numbered table-of-contents with right-aligned page numbers, book-style. "
               "Use when the deck has discrete numbered chapters and the audience needs an at-a-glance map; pick `contents` for a more visual TOC."),
    SlideEntry("agenda", 25, "navigation",
               "Meeting agenda with time-boxed items."),
    SlideEntry("agenda-summary", 26, "navigation",
               "'Summarize your agenda' framing slide. Use when agenda is more narrative than time-boxed."),
    SlideEntry("overview", 27, "navigation",
               "Presentation overview with subheadline blocks. Primes the audience on what follows."),
    SlideEntry("our-understanding", 28, "navigation",
               "'Our understanding' framing slide. Use to demonstrate you've heard the client's situation before pitching."),
    SlideEntry("together-intro", 29, "navigation",
               "'Together, we've created great things' partnership intro. Use for established-client check-ins or extension pitches."),
    SlideEntry("team-intro", 30, "navigation",
               "Team introduction slide. Use to present the people on the call."),
    SlideEntry("team-intro-2", 31, "navigation",
               "Team-intro variant on a white field with light-blue accent (less ink than team-intro). "
               "Use when the headshots and bios are the focus and you want minimum visual competition from the slide chrome."),
    SlideEntry("team-intro-3", 32, "navigation",
               "Team-intro variant with a divided light/dark blue background. "
               "Use when the team has two distinct sub-groups (e.g., Slalom team + client team) that benefit from a visual split."),
    SlideEntry("section-divider", 33, "navigation",
               "Neutral section divider with a small intro-text block under the title. "
               "Use when the section break needs a one-line subtitle to set up what follows."),
    SlideEntry("section-divider-alt", 34, "navigation",
               "Full-bleed dark blue section divider with title only (no intro text). "
               "Use when you want maximum visual break and the section title speaks for itself."),
    SlideEntry("section-divider-color", 35, "navigation",
               "Full-bleed color divider in Slalom Blue (accent1). High-contrast visual reset. "
               "Pick this when the section is the headline color of the deck; pick a -color-N variant when the section maps to a different brand accent."),
    SlideEntry("section-divider-color-2", 36, "navigation",
               "Full-bleed color divider in Cyan (accent3). "
               "Use when the section's theme maps to cyan in your color story (often: data, tech, momentum)."),
    SlideEntry("section-divider-color-3", 37, "navigation",
               "Full-bleed color divider in Coral Red (accent4). "
               "Use when the section's theme maps to coral red (often: risk, urgency, customer)."),
    SlideEntry("section-divider-color-4", 38, "navigation",
               "Full-bleed color divider in Purple (accent5). "
               "Use when the section's theme maps to purple (often: people, culture, creative)."),
    SlideEntry("section-divider-color-5", 39, "navigation",
               "Full-bleed color divider in Chartreuse (accent6). "
               "Use when the section's theme maps to chartreuse (often: growth, sustainability, energy)."),
    SlideEntry("section-divider-numbered-1", 40, "navigation",
               "Numbered chapter divider 01 on a solid Slalom Blue background. "
               "Use as the first chapter of a long deck; the numbered series 1-5 is intended to be used in order, but the visual treatment varies (1-3 are solid colors, 4-5 are nature photos)."),
    SlideEntry("section-divider-numbered-2", 41, "navigation",
               "Numbered chapter divider 02 with a cyan diagonal pattern. "
               "Use as chapter 2 in the numbered series — pairs with -1's solid blue."),
    SlideEntry("section-divider-numbered-3", 42, "navigation",
               "Numbered chapter divider 03 on a solid coral red background. "
               "Use as chapter 3 in the numbered series — high-contrast warm tone breaks up the cool-blue feel of -1 and -2."),
    SlideEntry("section-divider-numbered-4", 43, "navigation",
               "Numbered chapter divider 04 with a purple aerial-clouds photograph. "
               "Use as chapter 4 in the numbered series — visual treatment shifts from solid color to nature photography here."),
    SlideEntry("section-divider-numbered-5", 44, "navigation",
               "Numbered chapter divider 05 with a green farmland aerial photograph. "
               "Use as the final chapter (5) in the numbered series — completes the photo-pair with -4 for a closing nature beat."),
    SlideEntry("bio-card", 121, "navigation",
               "Single-person bio card with name, pronouns slot, and headshot area. Use for individual speaker intros."),

    # --- Content & Pricing ---
    SlideEntry("content-2col", 59, "content",
               "Two-column compare/contrast (Pros/Cons labels). Good for trade-off slides."),
    SlideEntry("content-3col", 61, "content",
               "Three-column layout for feature triads or parallel arguments."),
    SlideEntry("content-body", 69, "content",
               "Standard content slide with a title and rich body area (~5 sub-blocks)."),
    SlideEntry("content-large", 88, "content",
               "Dense single-slide summary with 5 body panels. Use when packing a lot onto one page."),
    SlideEntry("table", 90, "content",
               "Plain table layout for tabular data. Use when you need rows-and-columns without the side-by-side comparison framing."),
    SlideEntry("comparison-table", 91, "content",
               "Comparison table layout. Use for feature-by-feature, vendor-by-vendor, or option matrices."),
    SlideEntry("pricing", 99, "content",
               "Pricing table for rate cards or plan tiers."),
    SlideEntry("cost-estimate", 100, "content",
               "Cost estimate with a team-structure breakdown. Use for staffing + cost proposals."),
    SlideEntry("at-a-glance", 138, "content",
               "Dense executive 'At a glance' one-pager with ~22 slots for stats, callouts, and metrics. Use as a high-density summary."),
    SlideEntry("short-headline", 139, "content",
               "Short-headline overview with two-line title + body. Use for terse 'state of X' summaries."),

    # --- Process & Timelines ---
    SlideEntry("chevron-4", 92, "process-timeline",
               "Four-step chevron with bullet list under each step. Real CHEVRON auto-shapes; sequential left-to-right flow with multi-line detail per step."),
    SlideEntry("bullets-4-cols", 93, "process-timeline",
               "Four-column bullets layout with horizontal divider bars at the top. Use for parallel multi-bullet content without implying sequential flow. (Not a chevron despite the master title 'Chevron process'.)"),
    SlideEntry("process-visual", 95, "process-timeline",
               "Pipeline/intake flow with a TARGET endpoint (reactive intake -> pursuit -> engagement)."),
    SlideEntry("gantt-chart", 94, "process-timeline",
               "Gantt chart with swim-lanes and go-live milestones. Use for multi-track delivery plans."),
    SlideEntry("timeline-weekly", 96, "process-timeline",
               "Weekly timeline (short horizon). Use for sprint or cadence plans."),
    SlideEntry("timeline-8week", 97, "process-timeline",
               "Eight-week timeline. Use for pilots or phase-0 engagements."),
    SlideEntry("timeline-quarterly", 98, "process-timeline",
               "Quarterly roadmap with sprints and releases. Use for quarter+ horizons."),
    SlideEntry("flowchart", 113, "process-timeline",
               "Branching flowchart with decision points. Use for approval trees or conditional logic."),

    # --- Concept Diagrams ---
    SlideEntry("diagram-3-icons", 101, "diagrams",
               "Hub-and-spoke with 3 icon-labeled concepts around a center. Use for 3-part frameworks."),
    SlideEntry("diagram-4-icons", 102, "diagrams",
               "Hub-and-spoke with 4 icon-labeled concepts. Use for 4-quadrant or 4-pillar models."),
    SlideEntry("diagram-5-icons", 103, "diagrams",
               "Hub-and-spoke with 5 icon-labeled concepts."),
    SlideEntry("diagram-6-icons", 104, "diagrams",
               "Hub-and-spoke with 6 icons in a 3x2 grid around a central label. Strong choice for single-slide one-pagers with 6 items."),
    SlideEntry("venn-diagram", 114, "diagrams",
               "Three-circle Venn showing overlap between 3 groups. Use for role or capability intersections."),

    # --- Charts ---
    SlideEntry("chart-bar", 109, "charts",
               "Single-series bar graph. Use for ranked comparisons across categories."),
    SlideEntry("chart-bar-grouped", 110, "charts",
               "Grouped bar graph (multiple labels per row). Use for multi-series ranked comparisons."),
    SlideEntry("chart-bar-multi", 111, "charts",
               "Multi-series bar graph with several bars stacked horizontally per category. "
               "Use when you have 3+ series across a few categories (e.g., quarterly KPI trends across 4 metrics) — denser than chart-bar-grouped, less paired-comparison than chart-bar-comparison."),
    SlideEntry("chart-bar-comparison", 112, "charts",
               "Side-by-side comparison bar graph. Use to contrast two or more groups directly."),
    SlideEntry("chart-pie", 115, "charts",
               "Pie chart. Use for share-of-total at a glance (small N segments)."),
    SlideEntry("chart-doughnut", 116, "charts",
               "Doughnut chart. Modern alternative to a pie chart with center text space."),
    SlideEntry("chart-doughnut-comparison", 117, "charts",
               "Three doughnut charts side-by-side with subheadlines under each. "
               "Use for before/middle/after share-of-total comparisons or three-scenario projections; pick chart-doughnut for a single ring with center text."),
    SlideEntry("chart-line", 118, "charts",
               "Line graph. Use for time-series trends."),
    SlideEntry("chart-waterfall", 119, "charts",
               "Waterfall chart. Use for cost build-ups, budget walks, or running totals."),
    SlideEntry("chart-stacked-column", 120, "charts",
               "Stacked column graph. Use for parts-of-whole over multiple time periods or categories."),

    # --- Devices, Storytelling & About ---
    SlideEntry("device-frame-1", 105, "devices-storytelling",
               "Device frame layout 1 (image-to-be-replaced). Use for screenshots/mockups in a device shell. "
               "Body placeholder is 7.97\" wide but the right ~1.5\" sits behind the iPhone PICTURE shape (z-ordered above text); keep body copy under ~6.5\" effective width or it disappears behind the device."),
    SlideEntry("device-frame-2", 106, "devices-storytelling",
               "Device frame layout 2. "
               "Same iPhone-overlay constraint as device-frame-1: keep body copy under ~6.5\" effective width."),
    SlideEntry("device-frame-3", 107, "devices-storytelling",
               "Device frame layout 3. "
               "Same iPhone-overlay constraint as device-frame-1: keep body copy under ~6.5\" effective width."),
    SlideEntry("device-frame-4", 108, "devices-storytelling",
               "Device frame layout 4. "
               "Same iPhone-overlay constraint as device-frame-1: keep body copy under ~6.5\" effective width."),
    SlideEntry("storytelling-intro", 133, "devices-storytelling",
               "'Storytelling Templates' section opener. Use to introduce a customer-outcome chapter."),
    SlideEntry("customer-outcome-1", 134, "devices-storytelling",
               "Customer-outcome storytelling layout 1. Headline highlights the outcome; supporting blocks for context, action, result."),
    SlideEntry("customer-outcome-2", 135, "devices-storytelling",
               "Customer-outcome layout with a customer quote as the hero. "
               "Photo right, headline + body left, large pull quote across the top. "
               "Use when a verbatim customer voice is the most compelling proof point."),
    SlideEntry("customer-outcome-3", 136, "devices-storytelling",
               "Customer-outcome layout with three sub-headline blocks pairing description and supporting detail. "
               "Photo left, structured body right. "
               "Use when the outcome has multiple dimensions (technology, scale, partners) you want to call out individually."),
    SlideEntry("customer-outcome-4", 137, "devices-storytelling",
               "Customer-outcome layout with an explicit Solutions / Cloud Provider stamp and supporting body. "
               "Photo left (people working), body right with stats and labeled solution callouts. "
               "Use when the cloud platform / technology vendor partnership is part of the outcome story."),
    SlideEntry("spro-cover", 140, "devices-storytelling",
               "Single Page Response Overview (SPRO) cover. Use as the opener for a one-page proposal response."),
    SlideEntry("spro-template", 141, "devices-storytelling",
               "SPRO content template. Use for the body of a one-page proposal."),
    SlideEntry("about-slalom-1", 144, "devices-storytelling",
               "About Slalom boilerplate slide 1. Use to introduce the firm to a new client."),
    SlideEntry("about-slalom-2", 145, "devices-storytelling",
               "About-Slalom boilerplate with one named partner column alongside the firm description. "
               "Use when introducing a deck co-authored or co-delivered with a single named partner."),
    SlideEntry("about-slalom-3", 146, "devices-storytelling",
               "About-Slalom boilerplate with two named partner columns alongside the firm description. "
               "Use for joint pitches involving two partners (e.g., Slalom + cloud provider + ISV)."),
    SlideEntry("about-slalom-4", 147, "devices-storytelling",
               "About-Slalom boilerplate with three named partner columns. "
               "Use when the alliance / coalition itself is the narrative and three partners need equal billing alongside Slalom."),

    # --- Closers & Quotes ---
    SlideEntry("quote", 129, "closers",
               "Pull quote / testimonial slide. Use to spotlight a customer voice or strategic quote."),
    SlideEntry("quote-2", 130, "closers",
               "Pull-quote on white with attribution above and a large blue headline-style quote below. "
               "Use for a short, high-impact quote (3-5 lines) where the words should dominate the slide."),
    SlideEntry("quote-3", 131, "closers",
               "Pull-quote on white in body text size (smaller than quote-2) with attribution. "
               "Use when the quote is longer (multi-paragraph or 6+ lines) and won't fit at headline scale."),
    SlideEntry("quote-4", 132, "closers",
               "Pull-quote on a Slalom Blue background with white text. "
               "Use for the closing quote of a section or deck — high-contrast color reset signals 'this is the takeaway'."),
    SlideEntry("closing-connect", 149, "closers",
               "Closing slide listing 5 team contacts. Use as the last content page before copyright."),
    SlideEntry("thank-you-1", 150, "closers",
               "Thank-you closer with a winding-road-through-forest stock photo. "
               "Use for journey or partnership-continuation themes; swap the photo via Workflow C if a road metaphor doesn't fit your context."),
    SlideEntry("thank-you-2", 151, "closers",
               "Thank-you closer with a person looking out a car window through a landscape. "
               "Use for contemplation, perspective, or 'what's next' framings — more reflective tone than thank-you-1's road."),
    SlideEntry("thank-you-3", 152, "closers",
               "Thank-you closer with a green winding road through hills (different angle from thank-you-1). "
               "Use when the road metaphor fits but you want a fresher, less corporate-stock feel."),
    SlideEntry("thank-you-4", 153, "closers",
               "Thank-you closer with a person looking up / daydreaming portrait. "
               "Use for aspirational or future-looking closes — human-focused contrast to the landscape variants 1-3."),
    SlideEntry("thank-you-5", 154, "closers",
               "Thank-you closer on a plain Slalom Blue background, text-only (no photo). "
               "Use when no stock imagery fits the deck context — fastest to brand-correct close, no Workflow C swap needed."),
    SlideEntry("copyright", 156, "closers",
               "Copyright / disclaimer final slide. Use as the deck's last page."),
)


def by_category() -> dict[str, list[SlideEntry]]:
    """Return SLIDE_MAP grouped by category, preserving insertion order within each group."""
    out: dict[str, list[SlideEntry]] = {c: [] for c in CATEGORIES}
    for entry in SLIDE_MAP:
        if entry.category not in out:
            raise ValueError(f"Unknown category {entry.category!r} on entry {entry.name!r}")
        out[entry.category].append(entry)
    return out


def names() -> list[str]:
    return [e.name for e in SLIDE_MAP]


def assert_unique() -> None:
    """Sanity check: names and idx must be unique."""
    seen_names: set[str] = set()
    seen_idx: set[int] = set()
    for e in SLIDE_MAP:
        if e.name in seen_names:
            raise ValueError(f"Duplicate slide name {e.name!r}")
        if e.idx in seen_idx:
            raise ValueError(f"Duplicate slide idx {e.idx}")
        seen_names.add(e.name)
        seen_idx.add(e.idx)


if __name__ == "__main__":
    assert_unique()
    grouped = by_category()
    for cat, entries in grouped.items():
        print(f"{cat} ({len(entries)})")
        for e in entries:
            print(f"  {e.idx:>3}  {e.name}")
