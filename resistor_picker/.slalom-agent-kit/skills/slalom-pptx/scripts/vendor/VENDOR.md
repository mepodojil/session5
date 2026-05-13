# Vendored upstream `pptx` skill primitives

The slalom-pptx skill vendors a hybrid of the upstream `anthropic/skills` `pptx` skill so the catalog-driven Workflow A and the faithful-OOXML Workflow C both work without an external marketplace install.

## Why hybrid

Between commit `69c0b1a06741` and the current upstream `origin/main`, the upstream pptx skill **deleted** the high-level programmatic primitives (`rearrange.py`, `replace.py`, `inventory.py`, `ooxml/scripts/{unpack,pack,validate}.py`) and replaced them with a manual-OOXML-editing model (`add_slide.py`, `clean.py`, `office/{unpack,pack}.py`). The new primitives are excellent for hand-editing OOXML but don't replace what slalom-pptx's `idx`-driven catalog needs.

We split:

- **`legacy/`** — the deterministic catalog flow (Workflow A: extract by idx → bulk replace text against an inventory schema). Vendored at `69c0b1a06741` because the upstream HEAD no longer has these scripts at all.
- **`modern/`** — the faithful-OOXML escape hatch (Workflow C: unpack → hand-edit → clean → pack). Vendored at `d230a6dd6eb1a0dbee9fec55e2f00a96e28dff81` because the new tree adds smart-quote auto-escape, schema-validating pack-with-`--original`, and orphan cleanup.

`thumbnail.py` is vendored from the modern commit (the LibreOffice rendering surface didn't paradigm-shift).

## Source provenance

| Vendored path | Upstream source | Upstream commit |
|---|---|---|
| `legacy/rearrange.py` | `skills/pptx/scripts/rearrange.py` | `69c0b1a06741` |
| `legacy/replace.py` | `skills/pptx/scripts/replace.py` | `69c0b1a06741` |
| `legacy/inventory.py` | `skills/pptx/scripts/inventory.py` | `69c0b1a06741` |
| `modern/__init__.py` | `skills/pptx/scripts/__init__.py` | `d230a6dd6eb1` |
| `modern/clean.py` | `skills/pptx/scripts/clean.py` | `d230a6dd6eb1` |
| `modern/thumbnail.py` | `skills/pptx/scripts/thumbnail.py` | `d230a6dd6eb1` |
| `modern/unpack.py` | `skills/pptx/scripts/office/unpack.py` | `d230a6dd6eb1` |
| `modern/pack.py` | `skills/pptx/scripts/office/pack.py` | `d230a6dd6eb1` |
| `modern/validate.py` | `skills/pptx/scripts/office/validate.py` | `d230a6dd6eb1` |
| `modern/soffice.py` | `skills/pptx/scripts/office/soffice.py` | `d230a6dd6eb1` |
| `modern/helpers/*` | `skills/pptx/scripts/office/helpers/*` | `d230a6dd6eb1` |
| `modern/validators/*` | `skills/pptx/scripts/office/validators/*` | `d230a6dd6eb1` |
| `modern/schemas/**` | `skills/pptx/scripts/office/schemas/**` | `d230a6dd6eb1` |

Upstream license text is in `LICENSE.vendored` (copied from `skills/pptx/LICENSE.txt` at the legacy commit; the file is identical at the modern commit).

### Flat-layout note

We deliberately collapsed upstream's `scripts/office/...` segment so vendored modern files live directly under `modern/` instead of `modern/office/`. Reason: Claude Desktop refuses to install plugins where any path inside the `.plugin` archive nests deeper than 10 segments, and the upstream `office/schemas/ecma/fouth-edition/...` subtree pushed us to 11 segments. Functionally equivalent — `validators/base.py:99` self-locates schemas via `Path(__file__).parent.parent / "schemas"`, which still resolves correctly under the new layout (`modern/validators/base.py` → `parent.parent` is `modern/`, and `modern/schemas/` exists). The one source-level adjustment we needed: `modern/thumbnail.py` line 26 was `from office.soffice import get_soffice_env` (upstream) and is now `from soffice import get_soffice_env`, since `soffice.py` is now a sibling of `thumbnail.py` instead of being under `office/`.

## In-house patches to `legacy/`

The vendored copies in `legacy/` deliberately diverge from upstream to fix bugs surfaced during slalom-pptx testing. Patches #5/#6/#7 came out of 0.2.0 testing; #8/#9/#10/#11 came out of the second Claude Desktop pass that drove 0.2.2. Each modified file carries a `VENDORED COPY — slalom-pptx skill` header listing its patches.

### Patch #5 — chmod after copy (in `legacy/rearrange.py`)

**Symptom**: when the master template ships read-only on disk (e.g. mode `0o400`, which can happen after some plugin extractors), `shutil.copy2(template, output)` preserves the source mode. The subsequent `prs.save(output)` then raises `PermissionError`.

**Fix**: immediately after `shutil.copy2(...)` we `os.chmod(output, 0o644)` so the save can succeed regardless of source mode. Net effect: `rearrange.py master.pptx out.pptx 13` works even if the master is read-only.

### Patch #6 — overflow detector uses layout `defRPr` (in `legacy/inventory.py`)

**Symptom**: `_get_default_font_size` (instance method, used by `_estimate_frame_overflow`) walks the slide *master*'s `<p:txStyles><p:bodyStyle>` to find a default font size. This ignores layout-level overrides via `<p:defRPr sz="...">`, which many Slalom layouts use (e.g. `device-frame-1`'s body has effective default 5pt). The detector then assumes 18pt, predicts the body overflows, and `replace.py` returns false-positive overflow errors that block valid replacements.

**Fix**: prefer `self.default_font_size` (already populated in `__init__` by the static `get_default_font_size()` walking the layout's `defRPr`) before falling back to the master `bodyStyle` walk. The existing master-walk fallback is preserved for cases where layout-level defaults are unavailable.

### Patch #7 — `text_frame.clear()` gated on shape membership (in `legacy/replace.py`)

**Symptom**: the original loop unconditionally clears every text shape in the inventory before checking whether the caller's replacement JSON has anything to say about it. This contradicts slalom-pptx's documented Workflow A contract: "*Replace only what you want changed; omitted entries keep the original master text.*" In practice, decks shipped with empty `DATE` / `FOOTER` / `SLIDE_NUMBER` placeholders because those shapes were absent from the agent's replacement JSON yet still got blanked.

**Fix**: gate the `text_frame.clear()` on `shape_key in replacements.get(slide_key, {})`. Shapes the caller didn't include are skipped entirely, preserving master text. Explicit blanking still works by passing an entry with `"paragraphs": []` (the shape is in `replacements`, gets cleared, and no fill is added).

### Patch #8 — `\x0b` to `<a:br/>` conversion in run construction (in `legacy/replace.py`)

**Symptom**: master text captured by `inventory.py` contains `\x0b` (vertical tab) wherever the master used a soft line break - python-pptx represents `<a:br/>` as VT in `paragraph.text`. The agent then includes the VT in their replacement JSON expecting line-break semantics. But `replace.py`'s `apply_paragraph_properties` writes the text into `<a:t>` via python-pptx's `run.text = text`, which does NOT split on VT. OOXML serializers escape control chars per ISO 29500-1 §22.4.2.4 as `_xHHHH_` literals, so the VT round-trips as the string `_x000B_` and PowerPoint/LibreOffice render that escape *visibly* on the slide. A title intended as "Why we built `<line break>` Karakia" rendered as "Why we built _x000B_Karakia." Took the user two debug passes to spot.

**Fix**: in `apply_paragraph_properties`, split the incoming `text` on `\x0b` and emit alternating `<a:r><a:t>` runs and `<a:br/>` elements directly under the same `<a:p>`, preserving "soft break within one paragraph" semantics so paragraph-level properties (alignment, spacing, bullet) carry across the break. The leading run uses the existing or freshly-added paragraph run; subsequent segments append `<a:br/>` then a fresh run via `OxmlElement("a:br")` and `paragraph.add_run()`. Font properties are applied to *every* run created from the segments (the prior code only set them on the first), so formatting carries across the visual break.

### Patch #9 — `SLIDE_NUMBER` is editable in inventory (in `legacy/inventory.py`)

**Symptom**: `is_valid_shape` returned `False` for `SLIDE_NUMBER` placeholders, so they never made it into the inventory JSON. But Workflow A documents "*you MUST override SLIDE_NUMBER on every body slide*" because the master ships hardcoded position text (e.g., `"29"`, `"94"`, `"151"` on the slides the user extracted) that bears no relation to the output deck's actual order. The replacement JSON contract is keyed off the inventory, so there was no documented way to override - the user had to drop into python-pptx after `replace.py` to set `text_frame.text` on each SLIDE_NUMBER shape directly.

**Fix**: drop the `if placeholder_type == "SLIDE_NUMBER": return False` short-circuit. SLIDE_NUMBER placeholders now appear in the inventory as ordinary editable shapes. The numeric-only `FOOTER` filter stays - those are decorative numeric stamps with no editable content. Auto-derived `key_shapes` will start surfacing SLIDE_NUMBER in `references/slides/<category>.md` and `references/index.json`; that's accurate (the placeholder really is there) and gives agents a programmatic surface to override it.

### Patch #10 — auto-fill `SLIDE_NUMBER` when omitted (in `legacy/replace.py`)

**Symptom**: even with #9 exposing SLIDE_NUMBER in inventory, the contract still asks every body-slide replacement JSON to include a SLIDE_NUMBER entry. Patch #7 (already shipped) preserves master text on omitted shapes, so an oversight by the agent silently leaks the master's hardcoded number ("29") into the output. The user wanted the toolchain to help fulfil the documented contract instead of policing the agent's memory.

**Fix**: in the per-shape loop in `apply_replacements`, when `shape_data.placeholder_type == "SLIDE_NUMBER"` AND the shape is absent from `slide_replacements`, build a single-paragraph replacement on the fly: `{"paragraphs": [{"text": str(slide_index + 1)}]}`. Then proceed through the normal clear-and-fill path. Explicit overrides in the replacement JSON take precedence (the existing `if shape_key in slide_replacements` branch fires first). Cover slides typically don't carry SLIDE_NUMBER (verified via existing inventories) and are unaffected. The auto-fill uses 1-based deck position in the *output*, so `rearrange.py master out.pptx 13,32,45` produces slides numbered 1, 2, 3, not 13, 32, 45.

### Patch #11 — richer overflow error message (in `legacy/replace.py`)

**Symptom**: the post-replace overflow check raised errors of the form `slide-1/shape-8: overflow worsened by 0.19" (was 0.06", now 0.25")`. To act on it, the user had to re-open the inventory JSON and trace `shape-8` back to its placeholder ("CUSTOMER STORY: INDUSTRY...", a 2.44"-wide corner tag). 30 seconds per error, paid every retry.

**Fix**: when constructing the error string, look up `updated_inventory[slide_key][shape_key]` (already in scope) and append `placeholder_type` and a 30-char preview of `paragraphs[0].text`. The error becomes `slide-1/shape-8 (BODY, "CUSTOMER STORY: INDUSTRY..."): overflow worsened by 0.19" (was 0.06", now 0.25")`. Falls back to the old format (no parens) if the shape has neither a placeholder type nor any paragraphs - defensive, shouldn't happen in practice but cheap.

## Updating the vendor

Re-run `git show <commit>:<path>` to refresh a vendored file. After any update:

1. Re-apply the patch headers + patch bodies in the modified files (the patches are deliberate divergences, not cherry-picked upstream fixes).
2. Bump the commit hashes in `references/index.json` `vendored_from` and in this VENDOR.md.
3. `make clean && make bundle && make verify`.

Don't merge upstream changes wholesale — the patches in `legacy/` are stable, but a future upstream rewrite to the same files could regress them.
