"""Hardened icon extractor for the Slalom master template.

Replaces the fragile heuristic in the old preprocess.sh (which required the literal
word "icon" in the descr attribute and silently dropped icons named only "Lightning bolt"
or "Technology"). New rule:

    Any <p:pic> on the iconography slides (78, 79, 80; 1-indexed) with a non-empty
    `descr` is treated as an icon. The descr becomes the file stem after normalisation.

Pairs PNG and SVG: when a pic embeds a PNG, we look at the next-numbered relationship
(rId+1) to pick up the matching SVG, mirroring how PowerPoint stores icon pairs.
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

ICONOGRAPHY_SLIDE_NUMS = (78, 79, 80)


def _normalise(descr: str) -> str:
    """Convert a free-form descr like 'Engineering / infrastructure icon' to a file stem.

    Cleanup rules:
        - lowercase
        - drop the literal word 'icon' (case-insensitive)
        - whitespace -> '-', '/' -> '-'
        - collapse repeated dashes, strip leading/trailing dashes
    """
    s = descr.strip()
    s = re.sub(r"(?i)\bicons?\b", "", s)
    s = s.lower()
    s = s.replace("/", "-")
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def _parse_rels(rels_path: Path) -> dict[str, str]:
    """Return {rId: target_path} for one slide's _rels file."""
    import xml.etree.ElementTree as ET
    if not rels_path.exists():
        return {}
    tree = ET.parse(rels_path)
    return {rel.get("Id"): rel.get("Target", "") for rel in tree.getroot()}


def extract(master_pptx: Path, icons_dir: Path) -> int:
    """Extract every icon on the iconography slides into icons_dir as PNG + SVG pairs.

    Returns the number of icons written. Existing files in icons_dir are preserved if
    they don't conflict; conflicting names are overwritten so re-runs are idempotent.
    """
    import xml.etree.ElementTree as ET

    icons_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    with tempfile.TemporaryDirectory() as tmp:
        unpacked = Path(tmp) / "unpacked"
        with zipfile.ZipFile(master_pptx) as zf:
            zf.extractall(unpacked)

        media_dir = unpacked / "ppt" / "media"

        for n in ICONOGRAPHY_SLIDE_NUMS:
            slide_xml = unpacked / "ppt" / "slides" / f"slide{n}.xml"
            rels_xml = unpacked / "ppt" / "slides" / "_rels" / f"slide{n}.xml.rels"
            if not slide_xml.exists():
                continue

            rels = _parse_rels(rels_xml)
            tree = ET.parse(slide_xml)
            for pic in tree.getroot().iter(f"{NS_P}pic"):
                cnvpr = pic.find(f".//{NS_P}cNvPr")
                if cnvpr is None:
                    continue
                descr = (cnvpr.get("descr") or "").strip()
                if not descr:
                    continue
                stem = _normalise(descr)
                if not stem:
                    continue

                blip = pic.find(f".//{NS_A}blip")
                if blip is None:
                    continue
                embed_rid = blip.get(f"{NS_R}embed")
                if not embed_rid:
                    continue

                png_target = rels.get(embed_rid, "")
                if not png_target:
                    continue
                png_src = media_dir / Path(png_target).name
                if not png_src.exists():
                    continue

                ext = png_src.suffix.lower()
                if ext != ".png":
                    sys.stderr.write(f"  warn: icon {stem!r} has non-PNG primary ({ext}); skipping\n")
                    continue

                shutil.copy2(png_src, icons_dir / f"{stem}.png")
                written += 1

                # SVG pair: PowerPoint stores it as the next rId
                m = re.match(r"rId(\d+)$", embed_rid)
                if m:
                    next_rid = f"rId{int(m.group(1)) + 1}"
                    svg_target = rels.get(next_rid, "")
                    if svg_target.lower().endswith(".svg"):
                        svg_src = media_dir / Path(svg_target).name
                        if svg_src.exists():
                            shutil.copy2(svg_src, icons_dir / f"{stem}.svg")
    return written


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--master", type=Path, required=True)
    p.add_argument("--icons-dir", type=Path, required=True)
    args = p.parse_args()
    n = extract(args.master, args.icons_dir)
    print(f"Wrote {n} icons to {args.icons_dir}")
