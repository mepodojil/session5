---
name: slalom-pptx
description: >
  Create Slalom-branded PowerPoint presentations using the official Slalom
  template. Use for any deck, slides, one-pager, or PowerPoint output that
  should follow Slalom branding, colors, layouts, or visual style. Trigger on:
  "Slalom presentation", "Slalom deck", "Slalom slides", "branded pptx",
  "Slalom template" - and on adjacent phrasings even when "Slalom" is not
  spoken: "client kickoff deck", "QBR slides", "QBR deck", "proposal one-pager",
  "RFP response deck", "internal pitch deck", "client status deck",
  "executive summary slides". Triggers on icon swaps, text replacement, layout
  selection, and faithful template-based slide construction.
---

# Slalom PPTX Skill

95 catalogued slide layouts in the master template (extract on demand via `rearrange.py master <idx>`, where `idx` is **0-based**), 80 brand icons, and a per-category reference index. Load only the category file your task needs.

> Shared assets live in `.slalom-agent-kit/skills/slalom-pptx/` at the project root.
> All asset paths below are relative to that directory.

## Step 0: Preflight

Check only the dependencies the user's task actually needs. Don't pre-install everything. If a needed dependency is missing, ask the user before installing — phrase as "X is needed for [specific task]; install with `<command>`?"

| Dependency | When required | Detect with |
|---|---|---|
| Vendored `pptx` primitives (in this skill) | Always — bundled at `${CLAUDE_PLUGIN_ROOT}/skills/slalom-pptx/scripts/vendor/` | `[ -f ${CLAUDE_PLUGIN_ROOT}/skills/slalom-pptx/scripts/vendor/legacy/rearrange.py ]` |
| `python-pptx`, `Pillow`, `defusedxml`, `six` | Always | `python3 -c "import pptx, defusedxml, six; from PIL import Image"` |
| `markitdown[pptx]` | Always (Step 3 verify) | `python3 -m markitdown --help` |
| LibreOffice (`soffice`) | On-demand thumbnails (pre/post-synthesis) and Step 3 visual verify | `command -v soffice` (or `command -v libreoffice`) |

Install commands (use the one that matches the user's platform):

| Dependency | Command |
|---|---|
| Python deps | `pip install python-pptx Pillow defusedxml six 'markitdown[pptx]'` |
| LibreOffice — macOS | `brew install --cask libreoffice` |
| LibreOffice — Debian/Ubuntu | `sudo apt-get install -y libreoffice` |
| LibreOffice — Fedora/RHEL | `sudo dnf install -y libreoffice` |
| LibreOffice — Windows | `winget install --silent TheDocumentFoundation.LibreOffice` |

For batch / CI / `preprocess.sh` re-runs, the bundled platform-aware script handles detection and install in one shot:

```bash
bash .slalom-agent-kit/skills/slalom-pptx/scripts/preflight.sh           # detect only
bash .slalom-agent-kit/skills/slalom-pptx/scripts/preflight.sh --install # detect + auto-install
```

Export the vendor path for the rest of the session:

```bash
export PPTX_DIR=${CLAUDE_PLUGIN_ROOT}/skills/slalom-pptx/scripts/vendor
```

The vendored tree is hybrid:

- **`$PPTX_DIR/legacy/`** — `rearrange.py`, `replace.py`, `inventory.py` from upstream commit `69c0b1a06741` (with in-house patches for read-only-master `chmod`, layout-aware overflow detection, and omit-vs-blank semantics). Used by Workflow A (Template Replace).
- **`$PPTX_DIR/modern/`** — `clean.py`, `unpack.py`, `pack.py`, `validate.py`, `thumbnail.py`, plus `helpers/`, `validators/`, and `schemas/` from current upstream HEAD. Used by Workflow C (Faithful OOXML) and on-demand thumbnails. Smart quotes are auto-escaped on unpack and unescaped on pack. (We flattened upstream's `office/` segment for archive-depth reasons; functionally equivalent.)

Call vendored scripts for every file mutation. They are the canonical OOXML surface; reimplementing them risks subtle bytes-differ-from-PowerPoint bugs. See `${CLAUDE_PLUGIN_ROOT}/skills/slalom-pptx/scripts/vendor/VENDOR.md` for provenance and patch details.

## Step 1: Read the index router

Read `.slalom-agent-kit/skills/slalom-pptx/references/index.md` first. It's a ~30-line router. Load only what your task needs:

- Picking a slide layout → `references/slides/<category>.md` (one of 8: covers, navigation, content, process-timeline, diagrams, charts, devices-storytelling, closers).
- Brand colors / fonts / footer → `references/colors.md`.
- Icon catalog → `references/icons.md`.
- Step-by-step build / verify procedures → `references/workflows.md`.
- Programmatic catalog → `references/index.json`.

The router lists every asset path. Router + one category file is typically enough.

## Step 2: Choose a build workflow

| Scenario | Workflow |
|---|---|
| Slide layout exists in catalog | **A: Template Replace** |
| Close match but need to add/remove shapes | **C: Faithful OOXML** |
| Combine elements from multiple slides | **C: Faithful OOXML** |
| New layout, must match Slalom style | **C: Faithful OOXML** |
| Internal / throwaway content; user explicitly waived Slalom branding fidelity | **B: PptxGenJS** |

Step-by-step procedures live in `references/workflows.md`.

## Step 3: Verify (Workflow D)

After every generated `.pptx`, run the checks from `references/workflows.md`. Each catches a different failure mode; if LibreOffice isn't installed, run D1 + D2 only.

1. **D1 Text** (always) — `python3 -m markitdown output.pptx` confirms expected text appears.
2. **D2 Structure** (always) — `python-pptx` shape-type dump confirms the right shape *types* are present (e.g., a real `CHEVRON` auto-shape vs. a plain rectangle). Inventory JSON only captures text shapes; this is the structural ground truth.
3. **D3 Visual** (requires LibreOffice) — `python3 "$PPTX_DIR/scripts/thumbnail.py" output.pptx /tmp/qa --cols 3` renders to JPG so you can eyeball overflow, cutoff, and alignment.

When all three pass, the file at `output.pptx` is ready to deliver to the user.
