---
name: drawio-diagram
description: >-
  Generate professional, good-looking Draw.io (.drawio / mxGraph XML) diagrams from a
  natural-language description. Use this skill WHENEVER the user wants a diagram, chart,
  or visual — architecture / system / topology diagrams, flowcharts / workflows / sequence /
  swimlane / state machines, statistical charts (bar / pie / line), or matrix / comparison /
  quadrant / mind-map / kanban layouts — and especially when they mention "drawio",
  "draw.io", "diagrams.net", ".drawio file", "mxgraph", or ask to "draw / 画 / 生成 a diagram".
  Trigger even if the user only describes the content ("show how these services connect",
  "turn this process into a flowchart", "visualize this data") without naming drawio
  explicitly. Produces a complete, importable .drawio XML file with a consistent visual
  design system and validates it before handing it back.
---

# Draw.io Diagram Generator

Turn a description (or a chunk of content) into a complete, polished `.drawio` file.
The whole job is: **pick the right layout for the meaning, then realize it as mxGraph XML
using one consistent design system.** Form serves content — choose the structure that makes
the information obvious, not the structure that is easiest to draw.

## Workflow

1. **Read the content and classify it.** What relationship is the user actually trying to
   show? Connections between parts → architecture. Ordered steps → flowchart. Quantities →
   chart. Two crossed dimensions → matrix. This decision drives everything else. See
   [Choosing the layout](#choosing-the-layout).
2. **Open the matching reference file** for concrete, copy-paste mxCell templates and the
   layout math for that family. Don't reinvent geometry — the references already encode
   spacing that lines up.
3. **Build on the base skeleton** (below). Lay elements out on a coordinate grid, apply the
   shared design system, then connect with edges.
4. **Validate** with `scripts/validate_drawio.py` and fix anything it reports.
5. **Save** to a `.drawio` file (or output the XML inline if the user asked for that), and
   tell the user the path and what diagram type you chose.

Build the diagram by writing the XML to a file, not by narrating cell-by-cell in chat.

## Base skeleton

Every diagram is this exact wrapper. Fill `<root>` with your cells. Keep `id="0"` and
`id="1"` — they are the mandatory background layer and main layer; every other cell's
`parent` chains back to `1` (or to a container that chains back to `1`).

```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.0.0" type="device">
  <diagram id="diagram-1" name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1"
        connect="1" arrows="1" fold="1" page="1" pageScale="1"
        pageWidth="1200" pageHeight="800" math="0" shadow="0" background="#f8f9fa">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- your cells go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Sizing rules of thumb: set `pageWidth`/`pageHeight` to comfortably contain everything plus a
~40px margin. A typical landscape diagram is 1200×800 or 1400×900; a tall flow is portrait
(e.g. 900×1300). Multi-page: emit several `<diagram>` blocks, each with its own unique cell ids.

## The anatomy of a cell

A **vertex** (box / shape) and an **edge** (connector) are both `mxCell`s. The two things you
control are the `style` string (semicolon-separated key=value pairs) and the `mxGeometry`
(position/size for vertices, endpoints for edges).

```xml
<!-- vertex: a box at (x,y) sized w×h -->
<mxCell id="svc-api" value="API Gateway" style="rounded=1;whiteSpace=wrap;html=1;..."
    vertex="1" parent="1">
  <mxGeometry x="80" y="160" width="200" height="80" as="geometry" />
</mxCell>

<!-- edge: connects two vertices by id; geometry is usually empty -->
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;..." edge="1" parent="1"
    source="svc-api" target="svc-db">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Use **stable, meaningful ids** (`svc-api`, `step-validate`, `bar-q1`) rather than random
strings — it makes edges readable and keeps you from cross-wiring. Every `source`/`target`/
`parent` must point at an id that exists.

Multi-line text uses the XML entity `&#xa;` for a newline inside `value`. Escape `&`→`&amp;`,
`<`→`&lt;`, `>`→`&gt;` inside any value or it will corrupt the file.

## Shared design system

Reuse these verbatim across the whole diagram — visual consistency is what separates a
professional diagram from a noisy one. Pick **one accent color per logical group**, not a
rainbow per box.

### Color palette

Each family gives a strong fill (group headers / primary nodes), a soft fill (leaf nodes /
cells), a very-soft fill (container backgrounds), and a matching dark font color for text on
the fills.

| Family   | Strong fill | Soft fill | Container bg | Dark font (text) |
|----------|-------------|-----------|--------------|------------------|
| Blue     | `#A5B4FC`   | `#C7D2FE` | `#EEF2FF`    | `#1E3A8A`        |
| Green    | `#A7F3D0`   | `#D1FAE5` | `#ECFDF5`    | `#065F46`        |
| Purple   | `#C4B5FD`   | `#E9D5FF` | `#F5F3FF`    | `#5B21B6`        |
| Amber    | `#FDE68A`   | `#FEF3C7` | `#FFFBEB`    | `#92400E`        |
| Pink/Red | `#FECACA`   | `#FBCFE8` | `#FEF2F2`    | `#7F1D1D`        |
| Neutral  | `#94A3B8`   | `#D1D5DB` | `#E5E7EB`    | `#1F2937`        |

Special-purpose:
- **Dark banner** (title bars / summary strips): `fillColor=#1F2937;fontColor=#FFFFFF`.
- **Warning / hard constraint / risk**: use the Pink/Red family.
- **Undefined / placeholder**: neutral container bg + `dashed=1;fontStyle=2` (italic) +
  `fontColor=#94A3B8`.

### Reusable style strings

```
Title       text;html=1;align=center;verticalAlign=middle;fontSize=26;fontStyle=1;fontColor=#1a1a1a;
Subtitle    text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=2;fontColor=#6B7280;
Note/caption text;html=1;align=center;verticalAlign=middle;fontSize=10;fontStyle=2;fontColor=#6B7280;

Primary box rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=15;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;
Leaf box    rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=12;fontStyle=0;fillColor=#C7D2FE;fontColor=#1E3A8A;strokeColor=none;opacity=90;
Container   rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=13;fontStyle=1;fillColor=#EEF2FF;strokeColor=#C7D2FE;strokeWidth=1;opacity=80;
Banner      rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#1F2937;fontColor=#FFFFFF;strokeColor=none;opacity=95;

Edge        edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;
```

Swap the three color tokens (`fillColor`, `fontColor`, and container `strokeColor`) to change
family. To switch a box to the Green family: `fillColor=#A7F3D0;fontColor=#065F46`.

### Typography & layout grid

- **Font hierarchy**: title 26 → section/primary 15-18 → body 12-14 → caption 10-11. Bold
  (`fontStyle=1`) for headers, italic (`fontStyle=2`) for asides, regular for body.
- **Layout on a grid**: align elements to multiples of 10. Keep equal gutters between peers
  (a 30px gap between columns, consistent row heights). Reserve y≈20-90 for title+subtitle and
  the bottom strip for a legend/summary when useful.
- **Breathing room beats density**: leave whitespace; don't fill every pixel.
- **Containers for grouping**: to group children, make a Container vertex, then set each
  child's `parent` to the container id. Child `mxGeometry` is then **relative to the
  container's top-left**, not the page. This keeps a group movable as a unit.

## Choosing the layout

Match the *meaning* of the content to a family, then open that reference file. When content is
mixed, it's fine to combine (e.g. an architecture diagram whose nodes are arranged as a
flow). The references contain ready-made templates, exact style strings, and the spacing math.

| If the content is about…                                   | Use family            | Read |
|------------------------------------------------------------|-----------------------|------|
| How parts connect / depend / are layered; systems, services, network topology, ecosystems (central hub + radiating nodes) | Architecture / Topology | `references/architecture.md` |
| Ordered steps, decisions/branches, who-does-what lanes, state transitions, timelines/roadmaps | Flowchart / Process   | `references/flowchart.md` |
| Quantities & comparisons of values — bar, pie/donut, line/trend | Statistical chart     | `references/charts.md` |
| Two crossed dimensions (grid), option comparison tables, 2×2 quadrants, mind maps, kanban columns | Matrix / Comparison   | `references/matrix.md` |

Quick mental test: *connection* → architecture; *sequence/decision* → flowchart; *magnitude*
→ chart; *cross-classification* → matrix.

## Validate before delivering

After writing the file, run the validator and fix any errors it reports:

```bash
python3 scripts/validate_drawio.py path/to/your-diagram.drawio
```

It checks: well-formed XML; the mandatory `id="0"`/`id="1"` root cells; unique ids; every
`source`/`target`/`parent` resolves to a real id; vertices have geometry. These are the
mistakes that make draw.io refuse to open a file or silently drop shapes, so a clean run is
the bar for "done". Then report the saved path and the diagram type you used.

## Common pitfalls

- **Unescaped `&`/`<`/`>` in `value`** → corrupt file. Always entity-encode.
- **Dangling edges** — `source`/`target` pointing at an id that doesn't exist; the edge
  silently disappears. The validator catches this.
- **Overlapping boxes** because widths/gaps weren't summed. Lay out left-to-right keeping a
  running x; for a row of N boxes of width `w` with gap `g`: box k sits at `x0 + k*(w+g)`.
- **Rainbow syndrome** — one color per box. Color encodes *grouping*; reuse one family per group.
- **Tiny text in big boxes / clipped text in small boxes.** Size boxes to their text, and keep
  `whiteSpace=wrap;html=1` so long labels wrap instead of overflowing.
- **Edges crossing through unrelated boxes.** Use `exitX/exitY` + `entryX/entryY` (0..1 on the
  box border) to choose clean attach points, or add waypoints — see the flowchart reference.
