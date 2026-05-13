# slalom-pptx

A Cowork plugin that creates Slalom-branded PowerPoint presentations using the official Slalom template. Specialization layer over Anthropic's upstream `pptx` skill.

## What it gives you

- **95 pre-split slide layouts** in 8 categories (covers, navigation, content, process & timelines, diagrams, charts, devices & storytelling, closers)
- **80 brand icons** (PNG + SVG pairs, 160 files total)
- **Pre-extracted text inventories** for fast template replacement
- **95 thumbnail previews** for visual layout selection
- Token-efficient progressive-disclosure index (`references/index.md` router + 8 per-category catalogs); agent loads only the slice it needs
- Machine-readable catalog (`references/index.json`) for programmatic lookup
- Platform-aware preflight script (`scripts/preflight.sh`) with detection + auto-install for upstream pptx skill, Python deps, and LibreOffice across macOS / Linux / WSL / Windows
- The full Slalom master template as a fallback

## How it works

The skill activates when you ask Claude to build a Slalom deck, slides, or branded pptx. It reads the small index router, narrows to one category file based on what you need, picks the matching layout from the catalog, swaps in your text and icons, and verifies the output via three complementary checks (text, structure, visual).

Four workflows are supported:

- **A. Template Replace**: copy a slide, edit its inventory, replace text. Best fidelity to the template visuals.
- **B. PptxGenJS**: build programmatically with brand colors. Fastest for drafts; outputs sit outside the template theme.
- **C. Faithful OOXML**: edit the slide XML directly when you need to add or remove shapes. Preserves theme inheritance.
- **D. Verify**: combines `markitdown` (text), `python-pptx` (shape structure), and `thumbnail.py` (visual rendering) for end-to-end QA after any build.

## Prerequisites

This skill **extends** the upstream `pptx` skill rather than replacing it; install both:

| Dependency | What for | Install |
|---|---|---|
| Anthropic `pptx` skill | rearrange.py, inventory.py, replace.py, thumbnail.py, unpack.py, pack.py, validate.py | Via `anthropic-agent-skills` marketplace |
| `python-pptx`, `Pillow`, `defusedxml` | Inventory + structural shape inspection (Workflow D2) | `pip install python-pptx Pillow defusedxml` |
| `markitdown[pptx]` | Text-content verification (Workflow D1) | `pip install 'markitdown[pptx]'` |
| LibreOffice (`soffice`) | Thumbnail rendering / visual QA (Workflow D3); also used by `preprocess.sh` to populate `assets/thumbnails/` | brew (macOS) / apt-get / dnf / yum / pacman / zypper / apk (Linux) / winget / choco (Windows) |

Run `bash scripts/preflight.sh` to detect all four; pass `--install` to attempt auto-install. The script picks the right package manager for the current platform.

## Where this skill runs

Works in any environment that can shell out: **Claude Code** (CLI), **Claude Desktop** (built on Claude Code), and **claude.ai** (Cowork / code-interpreter sandbox). The same SKILL.md and preflight apply everywhere — only platform-specific install commands differ, and the preflight handles that automatically.

## Layout

```
slalom-pptx/
├── .claude-plugin/plugin.json
└── skills/slalom-pptx/
    ├── SKILL.md
    ├── references/
    │   ├── index.md            (router; read first)
    │   ├── index.json          (machine-readable catalog)
    │   ├── colors.md           (brand colors + fonts + footer)
    │   ├── workflows.md        (A/B/C build, D verify, icon swap)
    │   ├── icons.md            (icon library catalog)
    │   └── slides/             (one file per category; agent loads ONE)
    │       ├── covers.md
    │       ├── navigation.md
    │       ├── content.md
    │       ├── process-timeline.md
    │       ├── diagrams.md
    │       ├── charts.md
    │       ├── devices-storytelling.md
    │       └── closers.md
    ├── assets/
    │   ├── slides/             (95 pre-split layouts)
    │   ├── inventories/        (text-slot JSON for each slide)
    │   ├── thumbnails/         (PNG visual previews of each slide)
    │   ├── icons/              (80 unique icons, PNG + SVG)
    │   └── master/             (Slalom Template document.pptx)
    └── scripts/
        ├── preprocess.sh       (thin orchestrator)
        └── lib/                (Python helpers - data + extract + render)
```

## Reprocessing

To regenerate everything (after a Slalom master update or after editing `scripts/lib/slide_map.py` to add a layout):

```bash
cd .slalom-agent-kit/skills/slalom-pptx
./scripts/preprocess.sh
```

Thumbnails require LibreOffice; they're skipped with a clear warning if `soffice` is missing.
