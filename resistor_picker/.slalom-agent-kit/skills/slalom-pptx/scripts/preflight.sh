#!/usr/bin/env bash
set -euo pipefail

# Preflight checks for the slalom-pptx skill.
#
# Detects (and optionally auto-installs) every dependency:
#   - Anthropic upstream `pptx` skill (rearrange / inventory / replace / thumbnail / unpack / pack / validate)
#   - python-pptx, Pillow, defusedxml, markitdown[pptx]
#   - LibreOffice (`soffice`) - optional, only needed for thumbnails / Workflow D3
#
# Platform-aware: detects macOS / Linux / Windows-via-WSL/Cygwin and picks the
# right package manager (brew / apt-get / dnf / yum / pacman / zypper / apk / winget / choco).
#
# Skill-environment-aware: works whether the skill is invoked via Claude Code (local
# CLI), Claude Desktop (which embeds CC), or claude.ai Cowork / code-interpreter
# (sandboxed Linux container). The detection logic is the same; only install
# commands differ by platform.
#
# Usage:
#   ./preflight.sh              # detect only; print install commands for missing
#   ./preflight.sh --install    # detect + attempt to auto-install missing deps
#
# Exit 0 on success (and prints `PPTX_DIR=...` for `eval`); exit non-zero with
# clear remediation otherwise.

INSTALL_MODE=0
for arg in "$@"; do
  case "$arg" in
    --install) INSTALL_MODE=1 ;;
    --help|-h) sed -n '3,22p' "$0"; exit 0 ;;
  esac
done

ok()   { printf "  OK    %s\n" "$1"; }
warn() { printf "  WARN  %s\n" "$1"; }
fail() { printf "  FAIL  %s\n" "$1"; }

# --- Platform detection ---------------------------------------------------
detect_platform() {
  local kernel="$(uname -s 2>/dev/null || echo unknown)"
  case "$kernel" in
    Darwin*)  echo "macos" ;;
    Linux*)
      # Distinguish WSL from native Linux for completeness, but install paths
      # are identical (both use Linux package managers).
      if grep -qi microsoft /proc/version 2>/dev/null; then echo "wsl"; else echo "linux"; fi
      ;;
    CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
    *) echo "unknown" ;;
  esac
}

# Pick the first available package manager for the current platform; echo its
# name (or empty string if none found).
detect_pkgmgr() {
  local platform="$1"
  case "$platform" in
    macos)
      command -v brew >/dev/null 2>&1 && { echo brew; return; }
      ;;
    linux|wsl)
      for pm in apt-get dnf yum pacman zypper apk; do
        command -v "$pm" >/dev/null 2>&1 && { echo "$pm"; return; }
      done
      ;;
    windows)
      command -v winget >/dev/null 2>&1 && { echo winget; return; }
      command -v choco  >/dev/null 2>&1 && { echo choco; return; }
      ;;
  esac
  echo ""
}

# Print the install command for LibreOffice on the given platform/pkg manager.
libreoffice_install_cmd() {
  case "$1" in
    brew)    echo "brew install --cask libreoffice" ;;
    apt-get) echo "sudo apt-get update && sudo apt-get install -y libreoffice" ;;
    dnf)     echo "sudo dnf install -y libreoffice" ;;
    yum)     echo "sudo yum install -y libreoffice" ;;
    pacman)  echo "sudo pacman -S --noconfirm libreoffice-fresh" ;;
    zypper)  echo "sudo zypper install -y libreoffice" ;;
    apk)     echo "sudo apk add libreoffice" ;;
    winget)  echo "winget install --silent TheDocumentFoundation.LibreOffice" ;;
    choco)   echo "choco install -y libreoffice-fresh" ;;
    *)       echo "" ;;
  esac
}

PLATFORM="$(detect_platform)"
PKGMGR="$(detect_pkgmgr "$PLATFORM")"

echo "=== Slalom PPTX skill preflight ==="
echo "  platform: $PLATFORM"
echo "  package manager: ${PKGMGR:-none-detected}"

errors=0

# --- 1. Vendored pptx primitives -----------------------------------------
SCRIPT_DIR_PF="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR_PF="$(dirname "$SCRIPT_DIR_PF")"
PPTX_DIR="$SKILL_DIR_PF/scripts/vendor"

if [ -f "$PPTX_DIR/legacy/rearrange.py" ] && [ -f "$PPTX_DIR/modern/pack.py" ]; then
  ok "vendored pptx: $PPTX_DIR"
  # Surface the pinned commits recorded in references/index.json (provenance only).
  INDEX_JSON="$SKILL_DIR_PF/references/index.json"
  if [ -f "$INDEX_JSON" ] && command -v python3 >/dev/null 2>&1; then
    LEGACY_C="$(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));v=d.get('vendored_from') or {};print(v.get('legacy_pptx_skill_commit') or '')" "$INDEX_JSON" 2>/dev/null || true)"
    MODERN_C="$(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));v=d.get('vendored_from') or {};print(v.get('modern_pptx_skill_commit') or '')" "$INDEX_JSON" 2>/dev/null || true)"
    [ -n "$LEGACY_C" ] && printf "  INFO  legacy vendored from: %s\n" "${LEGACY_C:0:12}"
    [ -n "$MODERN_C" ] && printf "  INFO  modern vendored from: %s\n" "${MODERN_C:0:12}"
  fi
else
  fail "vendored pptx primitives missing under $PPTX_DIR"
  echo "    Expected: legacy/{rearrange,replace,inventory}.py + modern/{unpack,pack}.py"
  echo "    See $SKILL_DIR_PF/scripts/vendor/pptx/VENDOR.md to refresh the vendor tree."
  errors=$((errors + 1))
fi

# --- 2. Python deps -------------------------------------------------------
need_py=()
python3 -c "import pptx"        2>/dev/null && ok "python-pptx"      || need_py+=("python-pptx")
python3 -c "from PIL import Image" 2>/dev/null && ok "Pillow"        || need_py+=("Pillow")
python3 -c "import defusedxml"  2>/dev/null && ok "defusedxml"        || need_py+=("defusedxml")
python3 -m markitdown --help    >/dev/null 2>&1 && ok "markitdown[pptx]" || need_py+=("markitdown[pptx]")

if [ "${#need_py[@]}" -gt 0 ]; then
  PIP_CMD="pip"
  command -v pip3 >/dev/null 2>&1 && PIP_CMD="pip3"
  if [ "$INSTALL_MODE" -eq 1 ]; then
    echo "  attempting: $PIP_CMD install ${need_py[*]}"
    "$PIP_CMD" install --user "${need_py[@]}" 2>&1 | tail -3 | sed 's/^/    /' || true
    failed=()
    for pkg in "${need_py[@]}"; do
      mod="${pkg%%[*}"
      mod="${mod//-/_}"
      [ "$mod" = "Pillow" ] && mod="PIL"
      if [ "$mod" = "markitdown" ]; then
        python3 -m markitdown --help >/dev/null 2>&1 || failed+=("$pkg")
      else
        python3 -c "import $mod" 2>/dev/null || failed+=("$pkg")
      fi
    done
    if [ "${#failed[@]}" -gt 0 ]; then
      fail "still missing after install: ${failed[*]}"
      errors=$((errors + 1))
    else
      ok "python deps installed"
    fi
  else
    fail "python deps missing: ${need_py[*]}"
    echo "    $PIP_CMD install ${need_py[*]}"
    errors=$((errors + 1))
  fi
fi

# --- 3. LibreOffice (optional) -------------------------------------------
if command -v soffice >/dev/null 2>&1 || command -v libreoffice >/dev/null 2>&1; then
  ok "soffice (LibreOffice)"
else
  warn "soffice not on PATH - thumbnails and Workflow D3 visual QA disabled"
  install_cmd="$(libreoffice_install_cmd "$PKGMGR")"
  if [ -z "$install_cmd" ]; then
    case "$PLATFORM" in
      windows) echo "    Manual install (Windows): https://www.libreoffice.org/download/" ;;
      *) echo "    No supported package manager detected. Install manually: https://www.libreoffice.org/download/" ;;
    esac
  elif [ "$INSTALL_MODE" -eq 1 ]; then
    echo "  attempting: $install_cmd"
    eval "$install_cmd" 2>&1 | tail -3 | sed 's/^/    /' || true
    if command -v soffice >/dev/null 2>&1 || command -v libreoffice >/dev/null 2>&1; then
      ok "LibreOffice installed"
    else
      warn "LibreOffice install incomplete; run manually: $install_cmd"
    fi
  else
    echo "    $install_cmd"
    [ "$INSTALL_MODE" -eq 0 ] && echo "    (re-run with --install to attempt automatically)"
  fi
fi

echo
if [ "$errors" -gt 0 ]; then
  echo "Preflight: $errors required dependency missing. Fix above and re-run."
  exit 1
fi

echo "Preflight: OK"
echo "PPTX_DIR=$PPTX_DIR"
echo "(eval the above line to export PPTX_DIR for later commands)"
exit 0
