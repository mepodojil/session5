#!/usr/bin/env bash
set -euo pipefail

# Preprocess the Slalom master template into individual slides, inventories, icons,
# thumbnails, and the per-category references/ tree.
#
# This is a thin orchestrator. The actual logic lives in scripts/lib/:
#   slide_map.py   - categorized list of (name, idx, category, when_to_use)
#   extract.py     - rearrange + inventory + thumbnail per slide
#   icons.py       - hardened icon extractor (any pic on iconography slides)
#   render.py      - emits references/{index.md, index.json, colors.md, workflows.md, icons.md, slides/<cat>.md}
#
# Re-run after editing slide_map.py to update the catalog.
#
# Usage: ./preprocess.sh [path-to-pptx-skill-scripts]
# Example: ./preprocess.sh ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/pptx/scripts

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LIB_DIR="$SCRIPT_DIR/lib"

MASTER="$SKILL_DIR/assets/master/Slalom Template document.pptx"
INV_DIR="$SKILL_DIR/assets/inventories"
ICONS_DIR="$SKILL_DIR/assets/icons"
REF_DIR="$SKILL_DIR/references"

# Transient extraction dir for single-slide pptx files. extract.py needs writable
# slide files to feed inventory.py and thumbnail.py; the artifacts themselves are
# not shipped (the master + idx is the canonical surface for slide selection).
SLIDES_TMP="$(mktemp -d -t slalom-pptx-slides.XXXXXX)"
trap 'rm -rf "$SLIDES_TMP"' EXIT

VENDOR_PPTX="$SKILL_DIR/scripts/vendor"
PPTX_SCRIPTS="${1:-$VENDOR_PPTX/legacy}"

if [ ! -f "$PPTX_SCRIPTS/rearrange.py" ]; then
  echo "ERROR: Cannot find vendored pptx scripts at: $PPTX_SCRIPTS"
  echo "Expected layout: <skill>/scripts/vendor/pptx/legacy/{rearrange,replace,inventory}.py"
  echo "If you've moved the vendor tree, pass the legacy/ path explicitly: $0 /path/to/legacy"
  exit 1
fi

if [ ! -f "$MASTER" ]; then
  echo "ERROR: Master template not found at: $MASTER"
  exit 1
fi

# Vendor commits are pinned at vendor time, not detected at runtime.
# Keep these in sync with vendor/pptx/VENDOR.md if the vendor is refreshed.
LEGACY_VENDOR_COMMIT="69c0b1a0674149f27b61b2635f935524b6add202"
MODERN_VENDOR_COMMIT="d230a6dd6eb1a0dbee9fec55e2f00a96e28dff81"

echo "Master:        $MASTER"
echo "Pptx scripts:  $PPTX_SCRIPTS (vendored)"
echo "Skill root:    $SKILL_DIR"
echo "Slides tmp:    $SLIDES_TMP"
echo "Vendor legacy: $LEGACY_VENDOR_COMMIT"
echo "Vendor modern: $MODERN_VENDOR_COMMIT"
echo

echo "=== Cleaning previous output ==="
rm -rf "$INV_DIR" "$ICONS_DIR" "$REF_DIR/slides"
# Legacy directories removed in 0.2.0 (replaced by master+idx + on-demand thumbnails).
rm -rf "$SKILL_DIR/assets/slides" "$SKILL_DIR/assets/thumbnails"
rm -f "$REF_DIR/index.md" "$REF_DIR/index.json" \
      "$REF_DIR/colors.md" "$REF_DIR/workflows.md" "$REF_DIR/icons.md"
mkdir -p "$INV_DIR" "$ICONS_DIR" "$REF_DIR"

cd "$LIB_DIR"

echo "=== Validating slide_map.py ==="
python3 slide_map.py >/dev/null  # asserts uniqueness, exits non-zero on dup

echo
echo "=== Extracting transient slides + persisting inventories ==="
python3 extract.py \
  --master "$MASTER" \
  --slides "$SLIDES_TMP" \
  --inventories "$INV_DIR" \
  --pptx-scripts "$PPTX_SCRIPTS"

echo
echo "=== Extracting icons ==="
python3 icons.py \
  --master "$MASTER" \
  --icons-dir "$ICONS_DIR"

echo
echo "=== Rendering references/ ==="
python3 render.py \
  --master "$MASTER" \
  --inventories "$INV_DIR" \
  --icons "$ICONS_DIR" \
  --references "$REF_DIR" \
  --vendored-legacy-commit "$LEGACY_VENDOR_COMMIT" \
  --vendored-modern-commit "$MODERN_VENDOR_COMMIT"

echo
echo "=== Done ==="
echo "  Inventories:  $(ls "$INV_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')"
echo "  Icons (PNG):  $(ls "$ICONS_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ')"
echo "  Icons (SVG):  $(ls "$ICONS_DIR"/*.svg 2>/dev/null | wc -l | tr -d ' ')"
echo "  References:   $(find "$REF_DIR" -type f | wc -l | tr -d ' ')"
