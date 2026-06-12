#!/usr/bin/env python3
"""Emit a paste-ready Draw.io icon cell (or just the style fragment) from a bundled
line-icon set.

Why this exists: draw.io's built-in *generic* stencils are a visual mishmash, and
guessing stencil names silently renders blank shapes. This script instead carries a
small set of clean, uniform 24x24 single-stroke icons (Feather/Lucide-style),
recolors them to any hex on demand, and embeds them as a base64 SVG data-URI — so
they always render, survive PNG/SVG export, and look consistent across a diagram.

Usage:
  List icons:
    python3 icon_cell.py --list
  Just the style fragment (drop into an existing mxCell's style="..."):
    python3 icon_cell.py database --color "#1E3A8A"
  A full <mxCell> ready to paste into <root> (icon as a child of a container):
    python3 icon_cell.py user --color "#1E3A8A" --cell --id ico-user \
        --x 20 --y 18 --size 40 --parent panel-episodic
  A labeled icon node (icon with text below it):
    python3 icon_cell.py server --color "#065F46" --cell --id n-api \
        --x 80 --y 120 --size 48 --label "API Gateway" --parent 1
  Export the whole set as editable .svg files (stroke=currentColor):
    python3 icon_cell.py --export-dir ../assets/icons

Names are concept-friendly; several aliases map to a canonical icon (see --list).
If no icon fits a concept, use a labeled generic shape from the references instead of
inventing a stencil name.
"""
import argparse
import base64
import sys
from pathlib import Path
from xml.sax.saxutils import escape

# Each value is the inner SVG markup. Stroke color / width / line caps are set once
# on the wrapping <svg>, so inner elements inherit them and stay uniform.
ICONS = {
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "file": '<path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M13 2v7h7"/><path d="M8 13h8"/><path d="M8 17h6"/>',
    "files": '<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "diamond": '<path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l4 13 4-13-3-6"/><path d="M2 9h20"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4"/><circle cx="12" cy="3" r="1"/><path d="M9 13h.01"/><path d="M15 13h.01"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M9 17h6"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "message": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "refresh": '<path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "bar-chart": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="1"/><rect x="3" y="13" width="18" height="7" rx="1"/><path d="M7 7.5h.01"/><path d="M7 16.5h.01"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    "cloud": '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/><rect x="9" y="9" width="6" height="6"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5 9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>',
    "smartphone": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
    "alert-triangle": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
    "folder": '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2z"/>',
    "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.6-9.6"/><path d="m16 6 3 3"/><path d="m18 4 3 3"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "git-branch": '<line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}

# Concept-friendly aliases -> canonical icon name.
ALIASES = {
    "person": "user", "account": "user", "customer": "user",
    "team": "users", "group": "users",
    "document": "file", "doc": "file", "page": "file",
    "stack": "files", "documents": "files", "copy": "files", "episodic": "files",
    "magnifier": "search", "find": "search", "retrieval": "search", "query": "search",
    "gem": "diamond", "core": "diamond", "jewel": "diamond",
    "robot": "bot", "agent": "bot", "ai": "bot", "llm": "bot",
    "pencil": "edit", "write": "edit", "compose": "edit",
    "security": "shield", "protect": "shield", "fidelity": "shield",
    "chat": "message", "comment": "message", "bubble": "message",
    "time": "clock", "history": "clock", "timestamp": "clock",
    "sync": "refresh", "update": "refresh", "reload": "refresh", "cycle": "refresh",
    "funnel": "filter", "distill": "filter", "condense": "filter",
    "chart": "bar-chart", "metrics": "bar-chart", "stats": "bar-chart", "density": "bar-chart",
    "goal": "target", "objective": "target", "aim": "target",
    "service": "server", "host": "server", "backend": "server", "api": "server",
    "db": "database", "datastore": "database", "storage": "database", "sql": "database",
    "cache": "zap",
    "chip": "cpu", "compute": "cpu", "processor": "cpu",
    "tier": "layers", "layer": "layers",
    "secure": "lock", "auth": "lock", "private": "lock",
    "web": "globe", "internet": "globe", "network": "globe", "www": "globe",
    "mobile": "smartphone", "phone": "smartphone", "app": "smartphone",
    "desktop": "monitor", "screen": "monitor", "frontend": "monitor",
    "gear": "settings", "config": "settings", "ops": "settings",
    "flash": "zap", "fast": "zap", "event": "zap",
    "success": "check-circle", "done": "check-circle", "pass": "check-circle", "ok": "check-circle",
    "warning": "alert-triangle", "risk": "alert-triangle", "error": "alert-triangle", "alert": "alert-triangle",
    "email": "mail", "inbox": "mail",
    "directory": "folder",
    "secret": "key", "credential": "key", "token": "key",
    "developer": "code", "build": "code", "ci": "code",
    "branch": "git-branch", "vcs": "git-branch", "repo": "git-branch",
    "arrow": "arrow-right", "next": "arrow-right", "flow": "arrow-right",
}


def resolve(name):
    key = name.strip().lower()
    return ALIASES.get(key, key)


def svg_markup(name, color):
    canonical = resolve(name)
    if canonical not in ICONS:
        raise KeyError(canonical)
    inner = ICONS[canonical]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        'width="24" height="24" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{inner}</svg>'
    )


def data_uri(name, color):
    b64 = base64.b64encode(svg_markup(name, color).encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def style_fragment(name, color, labeled):
    base = "shape=image;html=1;imageAspect=0;aspect=fixed;"
    if labeled:
        base += (
            "verticalLabelPosition=bottom;verticalAlign=top;"
            "labelPosition=center;align=center;fontSize=12;"
        )
    return base + f"image={data_uri(name, color)};"


def full_cell(name, color, cid, x, y, size, parent, label):
    style = style_fragment(name, color, bool(label))
    value = escape(label) if label else ""
    # A labeled node needs extra height for the text below the icon.
    h = size + 22 if label else size
    return (
        f'<mxCell id="{escape(cid)}" value="{value}" style="{style}" '
        f'vertex="1" parent="{escape(parent)}">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{size}" height="{h}" as="geometry" />\n'
        f'</mxCell>'
    )


def do_list():
    print("Bundled icons (use any name or alias):\n")
    for n in sorted(ICONS):
        al = sorted(a for a, c in ALIASES.items() if c == n)
        suffix = f"   aliases: {', '.join(al)}" if al else ""
        print(f"  {n}{suffix}")


def do_export(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for n in sorted(ICONS):
        # Export with currentColor so the files are editable / themeable.
        (out / f"{n}.svg").write_text(svg_markup(n, "currentColor"), encoding="utf-8")
    print(f"Exported {len(ICONS)} icons to {out.resolve()}")


def main(argv):
    p = argparse.ArgumentParser(description="Generate a Draw.io icon cell / style.")
    p.add_argument("name", nargs="?", help="icon name or alias (see --list)")
    p.add_argument("--color", default="#1F2937", help="stroke hex color (default #1F2937)")
    p.add_argument("--size", type=int, default=28, help="icon size in px (default 28)")
    p.add_argument("--label", default="", help="label text (makes a labeled icon node)")
    p.add_argument("--cell", action="store_true", help="emit a full <mxCell> not just the style")
    p.add_argument("--id", default="icon-1", help="cell id (with --cell)")
    p.add_argument("--x", type=int, default=0, help="x (with --cell)")
    p.add_argument("--y", type=int, default=0, help="y (with --cell)")
    p.add_argument("--parent", default="1", help="parent cell id (with --cell)")
    p.add_argument("--list", action="store_true", help="list available icons and aliases")
    p.add_argument("--export-dir", help="write the whole set as .svg files and exit")
    args = p.parse_args(argv[1:])

    if args.list:
        do_list()
        return 0
    if args.export_dir:
        do_export(args.export_dir)
        return 0
    if not args.name:
        p.error("an icon name is required (or use --list / --export-dir)")

    try:
        if args.cell:
            print(full_cell(args.name, args.color, args.id, args.x, args.y,
                            args.size, args.parent, args.label))
        else:
            print(style_fragment(args.name, args.color, bool(args.label)))
    except KeyError as e:
        print(f"unknown icon: {e}. Run --list to see available names.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
