"""Extract per-slide pptx fragments + text inventories from the master template.

Wraps the upstream pptx skill's rearrange.py / inventory.py. The per-slide pptx
files are transient (preprocess.sh writes them to a mktemp dir and discards
them); only the inventories are persisted to the skill's assets/.

Thumbnails are NOT pre-baked - they're rendered on demand via the upstream
pptx skill's thumbnail.py (see references/workflows.md *On-demand thumbnails*).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from slide_map import SLIDE_MAP, SlideEntry


def _run(cmd: list[str], description: str) -> None:
    """Run a subprocess; on failure print the command and the captured output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(f"FAILED: {description}\n  cmd: {' '.join(cmd)}\n")
        if result.stdout:
            sys.stderr.write(f"  stdout: {result.stdout}\n")
        if result.stderr:
            sys.stderr.write(f"  stderr: {result.stderr}\n")
        raise SystemExit(1)


def extract_slide(
    entry: SlideEntry,
    master: Path,
    slides_dir: Path,
    inv_dir: Path,
    pptx_scripts: Path,
) -> None:
    """Extract one slide as a transient .pptx + persist its .json inventory."""
    slide_pptx = slides_dir / f"{entry.name}.pptx"
    inv_json = inv_dir / f"{entry.name}.json"

    _run(
        ["python3", str(pptx_scripts / "rearrange.py"),
         str(master), str(slide_pptx), str(entry.idx)],
        f"rearrange idx={entry.idx} -> {entry.name}",
    )
    _run(
        ["python3", str(pptx_scripts / "inventory.py"),
         str(slide_pptx), str(inv_json)],
        f"inventory {entry.name}",
    )


def extract_all(
    master: Path,
    slides_dir: Path,
    inv_dir: Path,
    pptx_scripts: Path,
) -> dict[str, str]:
    """Extract every entry in SLIDE_MAP. Returns a status summary by name."""
    slides_dir.mkdir(parents=True, exist_ok=True)
    inv_dir.mkdir(parents=True, exist_ok=True)

    statuses: dict[str, str] = {}
    for entry in SLIDE_MAP:
        sys.stderr.write(f"  {entry.name} (idx {entry.idx}, {entry.category})...\n")
        extract_slide(entry, master, slides_dir, inv_dir, pptx_scripts)
        statuses[entry.name] = "ok"
    return statuses


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--master", type=Path, required=True)
    p.add_argument("--slides", type=Path, required=True,
                   help="Transient dir for per-slide pptx fragments (preprocess.sh wipes after).")
    p.add_argument("--inventories", type=Path, required=True)
    p.add_argument("--pptx-scripts", type=Path, required=True)
    args = p.parse_args()
    extract_all(args.master, args.slides, args.inventories, args.pptx_scripts)
