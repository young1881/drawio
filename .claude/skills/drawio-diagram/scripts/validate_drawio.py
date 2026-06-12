#!/usr/bin/env python3
"""Validate a .drawio (mxGraph XML) file for the mistakes that make draw.io refuse to
open a file or silently drop shapes.

Checks performed (per <diagram> page):
  - the file is well-formed XML
  - the mandatory root cells id="0" and id="1" exist
  - every mxCell id is unique
  - every edge source/target points at an id that exists on the same page
  - every cell parent points at an id that exists on the same page
  - vertices have an <mxGeometry> child

(Entity safety — unescaped & < > in values — is already guaranteed: such a file would
fail the well-formedness check above, so no separate test is needed.)

Usage:
    python3 validate_drawio.py path/to/file.drawio [more.drawio ...]

Exit code 0 = all clean, 1 = at least one error found. Warnings never fail the run.
"""
import sys
import xml.etree.ElementTree as ET


def validate_file(path):
    errors, warnings = [], []

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except ET.ParseError as e:
        return [f"XML is not well-formed: {e}"], []
    except FileNotFoundError:
        return [f"File not found: {path}"], []

    diagrams = root.findall(".//diagram")
    if not diagrams:
        # Some files put mxGraphModel at top level without <diagram>; handle both.
        models = root.findall(".//mxGraphModel")
        if not models:
            errors.append("No <diagram> or <mxGraphModel> element found.")
            return errors, warnings
        diagrams = [None] * len(models)
        model_list = models
    else:
        model_list = [d.find(".//mxGraphModel") for d in diagrams]

    for idx, model in enumerate(model_list):
        page = f"page {idx + 1}"
        if model is None:
            errors.append(f"[{page}] <diagram> has no <mxGraphModel>.")
            continue

        root_el = model.find("root")
        if root_el is None:
            errors.append(f"[{page}] <mxGraphModel> has no <root>.")
            continue

        cells = root_el.findall("mxCell")
        ids = [c.get("id") for c in cells if c.get("id") is not None]

        # Required root cells
        if "0" not in ids:
            errors.append(f"[{page}] missing mandatory root cell id=\"0\".")
        if "1" not in ids:
            errors.append(f"[{page}] missing mandatory layer cell id=\"1\".")

        # Unique ids
        seen, dupes = set(), set()
        for cid in ids:
            if cid in seen:
                dupes.add(cid)
            seen.add(cid)
        for d in sorted(dupes):
            errors.append(f"[{page}] duplicate cell id: \"{d}\".")

        id_set = set(ids)

        for c in cells:
            cid = c.get("id", "<no-id>")
            is_edge = c.get("edge") == "1"
            is_vertex = c.get("vertex") == "1"

            # parent must resolve (id=0 may legitimately have no parent)
            parent = c.get("parent")
            if parent is None:
                if cid != "0":
                    warnings.append(f"[{page}] cell \"{cid}\" has no parent attribute.")
            elif parent not in id_set:
                errors.append(
                    f"[{page}] cell \"{cid}\" parent=\"{parent}\" does not exist."
                )

            # edge endpoints must resolve when present
            for end in ("source", "target"):
                ref = c.get(end)
                if ref is not None and ref not in id_set:
                    errors.append(
                        f"[{page}] edge \"{cid}\" {end}=\"{ref}\" does not exist."
                    )
            if is_edge and c.get("source") is None and c.get("target") is None:
                # floating edge with only points is allowed, but flag the common mistake
                geo = c.find("mxGeometry")
                has_points = geo is not None and geo.find("mxPoint") is not None
                if not has_points:
                    warnings.append(
                        f"[{page}] edge \"{cid}\" has no source/target and no points."
                    )

            # vertices should carry geometry
            if is_vertex and c.find("mxGeometry") is None:
                errors.append(f"[{page}] vertex \"{cid}\" has no <mxGeometry>.")

    return errors, warnings


def main(argv):
    paths = argv[1:]
    if not paths:
        print("usage: validate_drawio.py file.drawio [more.drawio ...]")
        return 2

    any_error = False
    for path in paths:
        errors, warnings = validate_file(path)
        print(f"\n=== {path} ===")
        if not errors and not warnings:
            print("OK — no problems found.")
        for w in warnings:
            print(f"  WARN  {w}")
        for e in errors:
            print(f"  ERROR {e}")
        summary = f"{len(errors)} error(s), {len(warnings)} warning(s)"
        print(f"  -> {summary}")
        any_error = any_error or bool(errors)

    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
