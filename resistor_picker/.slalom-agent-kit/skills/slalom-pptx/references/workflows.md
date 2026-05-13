# Workflows

| Need | Workflow |
|---|---|
| Layout already in catalog | A: Template Replace |
| Close match, need to add/remove shapes | C: Faithful OOXML |
| Combine elements from multiple slides | C: Faithful OOXML |
| New layout that must match Slalom style | C: Faithful OOXML |
| Internal / throwaway content; user explicitly waived Slalom branding fidelity | B: PptxGenJS |
| Confirm the output (run after every build) | D: Verify |

## Workflow A: Template Replace

```bash
# 1. Extract the slide(s) from the master by 0-based master idx
#    (look up idx in references/slides/<category>.md)
python3 "$PPTX_DIR/legacy/rearrange.py" \
    "assets/master/Slalom Template document.pptx" working.pptx <idx>
# Multi-slide deck: pass a comma-separated list, e.g. 13,32,45,118,167

# 2. Read the inventory
cat assets/inventories/<slide-name>.json

# 3. Write replacement-text.json matching the inventory structure
#    (preserve font_size, bold, line_spacing from the original)
#    REQUIRED on every body slide - see "Required system-placeholder fills" below.

# 4. Apply replacements
python3 "$PPTX_DIR/legacy/replace.py" working.pptx replacement-text.json output.pptx

# 5. (Optional) Swap icons - see Icon Swap below.
```

`replacement-text.json` mirrors the inventory's `slide-N` / `shape-M` / `paragraphs[i].text` keys. Replace only what you want changed; **omitted entries keep the original master text — empty string `""` BLANKS the placeholder and is destructive.** When in doubt, omit.

### Required system-placeholder fills (body slides)

Every body / content / section-divider / closer slide carries three system placeholders that the master ships with stale or hardcoded defaults. Override `DATE` and `FOOTER` on every such slide; `SLIDE_NUMBER` is auto-filled by `replace.py` when omitted (see below). Cover slides typically don't carry these; check the inventory to confirm.

| Inventory `placeholder_type` | Master ships with | What to put |
|---|---|---|
| `DATE` | "2025" (stale) | Deck year, default format `yyyy` (e.g. "2026"). Master placeholder is only ~0.28" wide; longer formats wrap or clip. |
| `FOOTER` | brand string (often blanked accidentally) | `Slalom. All Rights Reserved. Proprietary and Confidential.` (from `references/colors.md`) |
| `SLIDE_NUMBER` | hardcoded master position (e.g. "29", "94") - NOT a dynamic field | Auto-filled with the slide's deck position (1-based) when omitted from your replacement JSON. Pass an explicit override only when you need a different number (e.g. `"iv"` for front-matter Roman numerals). |

After `replace.py`, run Workflow D1 (`markitdown`) and visually scan that the date, footer, and page numbers appear correctly on every body slide.

```json
{
  "slide-0": {
    "shape-2": {
      "paragraphs": [
        {"text": "Acme Q4 Strategy Review"}
      ]
    },
    "shape-3": {
      "paragraphs": [
        {"text": "Prepared for the executive team, January 2026."}
      ]
    }
  }
}
```

## On-demand thumbnails

Thumbnails are not pre-baked - render them when you actually need a visual.

```bash
# Pre-synthesis: preview a master layout before committing
TMP=$(mktemp -d) && trap 'rm -rf "$TMP"' EXIT
python3 "$PPTX_DIR/legacy/rearrange.py" \
    "assets/master/Slalom Template document.pptx" "$TMP/preview.pptx" <idx>
python3 "$PPTX_DIR/modern/thumbnail.py" "$TMP/preview.pptx" "$TMP/thumb" --cols 1
# -> $TMP/thumb.jpg

# Post-synthesis: visual QA on the deck you just built (also Workflow D3)
python3 "$PPTX_DIR/modern/thumbnail.py" output.pptx /tmp/qa --cols 3
# -> /tmp/qa.jpg (grid)
```

Both paths use the vendored `modern/thumbnail.py` (driven by LibreOffice). Requires `soffice` on PATH; if missing, fall back to the markitdown text check (D1) and shape-type dump (D2).

## Workflow B: Hybrid Build (PptxGenJS)

1. Build slides programmatically with PptxGenJS.
2. Pull brand colors from `references/colors.md` (NO `#` prefix in PptxGenJS hex values).
3. Use Arial font (Avenir Next LT Pro is not web-safe).
4. Use pre-extracted icons via `addImage({ path: 'assets/icons/<name>.png' })`.
5. Add the standard footer text from `references/colors.md`.

## Workflow C: Faithful New Creation (OOXML)

Workflow C uses the modern `office/` toolchain: smart-quote auto-escape on unpack, schema-validating pack with `--original` comparison, and `clean.py` for orphan removal. Pack auto-validates — no separate validate step.

```bash
# 1. Extract closest template slide as base (legacy: deterministic by 0-based idx)
python3 "$PPTX_DIR/legacy/rearrange.py" \
    "assets/master/Slalom Template document.pptx" base.pptx <idx>

# 2. Unpack (modern: auto-escapes smart quotes -> XML entities)
python3 "$PPTX_DIR/modern/unpack.py" base.pptx unpacked/

# 3. Edit ppt/slides/slide1.xml:
#    - Add/remove/reposition <p:sp> shape elements
#    - Use scheme color refs: <a:schemeClr val="accent1"/> (NOT hardcoded hex)
#    - Use theme fonts: <a:latin typeface="+mn-lt"/> (NOT explicit font names)
#    - Copy shapes from other unpacked template slides as building blocks
#    - Smart quotes are already escaped — write literal " ' in your edits and pack will round-trip them

# 4. (Optional) Drop orphans if you removed slides or relationships
python3 "$PPTX_DIR/modern/clean.py" unpacked/

# 5. Repack with validation against the original
python3 "$PPTX_DIR/modern/pack.py" unpacked/ output.pptx --original base.pptx
```

Starting from a template slide inherits master styles, theme colors, fonts, shadows, and gradients automatically. `pack.py --original` auto-repairs minor schema issues and reports whether the result validates.

## Icon Swap

```bash
# 1. Unpack the slide
python3 "$PPTX_DIR/modern/unpack.py" output.pptx unpacked/

# 2. Find which media files the slide's icons reference
cat unpacked/ppt/slides/_rels/slide1.xml.rels | grep media

# 3. Copy replacement icons (both PNG and SVG)
cp assets/icons/<new-icon>.png unpacked/ppt/media/<original-image>.png
cp assets/icons/<new-icon>.svg unpacked/ppt/media/<original-image>.svg

# 4. Repack
python3 "$PPTX_DIR/modern/pack.py" unpacked/ output.pptx --original output.pptx
```

## Workflow D: Verify

After every build, run all three checks. Each catches a different failure mode.

### D1. Text content (deterministic, fast)

```bash
python3 -m markitdown output.pptx
```

Confirms expected text appears. Fastest check.

### D2. Shape structure (deterministic, no rendering)

```bash
python3 - <<'PY'
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
prs = Presentation("output.pptx")
for i, slide in enumerate(prs.slides):
    print(f"slide {i+1}:")
    for sh in slide.shapes:
        tag = sh.shape_type.name if sh.shape_type else "?"
        if sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            tag += f"({sh.auto_shape_type.name})"
        text = sh.text_frame.text[:40].replace("\n", " / ") if sh.has_text_frame else ""
        print(f"  {tag:<28} {text!r}")
PY
```

Confirms the right shape *types* are present (e.g., a real `CHEVRON` auto-shape vs. just a rectangle). Inventory JSON only captures text shapes, so this is the structural ground truth.

### D3. Visual rendering (catches overflow, cutoff, alignment)

```bash
python3 "$PPTX_DIR/modern/thumbnail.py" output.pptx /tmp/qa --cols 3
```

Renders the deck to JPG via LibreOffice. Open the result to eyeball overflow, cutoff, font fallback, alignment.

### Other checks
- Slide count matches expectations.
- If `replace.py` errors on overflow, shorten the text and retry.
- After icon swap, verify replacement files are > 0 bytes.

## Verification gate

The deck is NOT ready until D1, D2, AND D3 have all been run AND inspected, and the agent has cited what each step found. Implicit success ("looks good", "tests passed") is not acceptable; the agent must report concrete evidence per check. Examples of acceptable evidence:

- **D1 (markitdown):** "title text 'Why we built X' is present on slide 2; no `_x000B_` or other escape leakage anywhere; FOOTER reads exactly 'Slalom. All Rights Reserved. Proprietary and Confidential.' on every body slide."
- **D2 (shape-type dump):** "slide 4 contains 4× CHEVRON auto-shapes (not rectangles); SLIDE_NUMBER placeholders show '1' through '6' across body slides 1-6."
- **D3 (thumbnail render):** "thumb.jpg shows no overflow in any title; chevron arrows point right; device-frame body copy stays clear of the iPhone overlay; closer slide imagery matches the deck context."

If `soffice` is unavailable and D3 cannot run, say so explicitly and flag the deck as **unverified** rather than skipping silently. D1 + D2 alone do not constitute a passed gate.

Iterate as needed. Common signals to revise: D3 reveals overflow that the deterministic overflow-checks missed (LibreOffice rendering differs from PIL estimation), the wrong placeholder type was filled (D2 caught it via shape-type dump), or text disagrees between D1 and D3 (escape leakage, encoding issue). The loop is designed: edit JSON → `replace.py` → D1+D2+D3 → adjust → repeat. Don't stop after one pass; trust the triad to reveal what each individual check misses.

## Pitfalls

- **Empty string is destructive.** Passing `{"text": ""}` for a shape in your replacement JSON BLANKS it. To inherit master text, OMIT the shape entirely; to override, supply real text. Omission ≠ empty string.
- **DATE / FOOTER on body slides ship with stale or hardcoded defaults from the master** (year "2025", brand footer string sometimes blanked). Always override them — see *Required system-placeholder fills* in Workflow A. Default DATE format is `yyyy` (4 chars; the master's DATE placeholder is only ~0.28" wide). SLIDE_NUMBER is auto-filled with the slide's deck position when omitted; pass an explicit override only for non-numeric formats.
- **Soft line breaks in master text use `\x0b` (vertical tab).** Inventory JSON shows them as `\u000b` between words where the master had a `<a:br/>`. `replace.py` (Patch #8) splits on `\x0b` and emits real OOXML `<a:br/>` elements automatically — write the literal VT in your replacement text where you want a soft break. Older versions of the toolchain wrote the VT into `<a:t>` directly; PowerPoint serialized it as the literal escape `_x000B_` and rendered that string visibly. If you see `_x000B_` in a D1 markitdown output, the build is using a stale `replace.py` predating the patch.
- **Closer-slide stock imagery.** Layouts like `thank-you-1` and several `quote-N` variants ship with master-provided stock photos (winding road, generic forest, etc.). The inventory exposes only the text placeholders; the picture is a master-owned shape. To swap the image for context-appropriate photography, drop into Workflow C: unpack → replace `ppt/media/imageN.{jpg,png}` → pack. Same procedure as the Icon Swap above, just on a different media file.
- Delete `INSTRUCTIONS` and `Click to add ...` placeholder text in extracted slides; it's master designer-help, not editable content. The auto-derived `Key shapes` columns already hide it, but the actual `.pptx` files retain it.
- `bullets-4-cols.pptx` is a four-column-bullets layout, not a chevron, despite the master title saying "Chevron process". The real chevron is `chevron-4.pptx`.
- Inventory captures only text shapes. Icons are picture shapes; swap them via the Icon Swap procedure above.
- Cover slides use `CENTER_TITLE` / `BODY` placeholders (no `TITLE`); section dividers may have only `BODY`. Read the inventory's `placeholder_type` field; don't assume `TITLE` exists.

## Tips

- Always start from a template slide when visual fidelity matters.
- Prefer `<a:schemeClr val="accent1"/>` over `<a:srgbClr val="0C62FB"/>` in OOXML.
- Use `<a:latin typeface="+mn-lt"/>` for body, `+mj-lt` for headings.
- PptxGenJS builds outside the template theme - use only for drafts.
- Text must fit shape dimensions - check width/height in inventory JSON.
- Icons are PNG+SVG pairs - replace both when swapping.
- The slide master provides consistent footer, page numbers, and background.
- Combine slides via `rearrange.py` with multiple indices: `rearrange.py master.pptx out.pptx 13,104,92`.
