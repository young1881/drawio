# Matrix / Comparison / Mind-map

For **cross-classification and side-by-side structure**: two-dimensional matrices (rows ×
columns), option comparison tables, 2×2 quadrants, mind maps, and kanban boards. The unifying
idea is a *regular grid* of positions — the work is computing aligned coordinates so columns
and rows line up perfectly.

Styles and colors come from the shared design system in SKILL.md.

## Contents
- [Pattern A — Row × Column matrix](#pattern-a--row--column-matrix)
- [Pattern B — Comparison table](#pattern-b--comparison-table)
- [Pattern C — 2×2 quadrant](#pattern-c--2x2-quadrant)
- [Pattern D — Mind map](#pattern-d--mind-map)
- [Pattern E — Kanban board](#pattern-e--kanban-board)

---

## Pattern A — Row × Column matrix

The workhorse. A top-left corner cell, a row of column headers, a column of row headers, and a
grid of body cells at each intersection. Compute one set of x-positions for columns and one set
of y-positions for rows, then reuse them everywhere so everything aligns.

Layout: with row-header width `rhW`, column width `cW`, column gap `cGap`, header row height
`hH`, body row height `rH`, row gap `rGap`, and grid origin `(gx, gy)`:
- column j left edge: `gx + rhW + cGap + j*(cW + cGap)`
- row i top edge:     `gy + hH + rGap + i*(rH + rGap)`
- the corner sits at `(gx, gy)`, size `rhW × hH`
- color each **row** (or each column) with one family so the band reads as a group

```xml
<!-- Corner -->
<mxCell id="corner" value="Capability ↓ / Stage →" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=11;fontStyle=2;fillColor=#E5E7EB;fontColor=#475569;strokeColor=none;opacity=90;" vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="220" height="60" as="geometry" />
</mxCell>
<!-- A column header (amber) -->
<mxCell id="col-write" value="Write" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=15;fontStyle=1;fillColor=#FDE68A;fontColor=#92400E;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="280" y="100" width="240" height="60" as="geometry" />
</mxCell>
<!-- A row header (blue) -->
<mxCell id="row-l1" value="L1 Integrity&#xa;accuracy focus" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="40" y="180" width="220" height="120" as="geometry" />
</mxCell>
<!-- A body cell at (L1 × Write): light container, optionally with chips inside -->
<mxCell id="cell-l1-w" value="" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#EEF2FF;strokeColor=#C7D2FE;strokeWidth=1;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="280" y="180" width="240" height="120" as="geometry" />
</mxCell>
<!-- A "chip" inside the body cell (parent = the cell; geometry relative to it) -->
<mxCell id="chip-1" value="Precision / Recall" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=11;fillColor=#C7D2FE;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="cell-l1-w">
  <mxGeometry x="10" y="12" width="220" height="46" as="geometry" />
</mxCell>
```

A flow arrow across the headers (`Write → Manage → Read → Use`) reinforces a left-to-right
progression; use the standard edge with `exitX=1;exitY=0.5;entryX=0;entryY=0.5;`. For an empty
intersection, use a dashed neutral placeholder cell ("— not defined —", italic, `dashed=1`).

## Pattern B — Comparison table

Side-by-side option columns, each a Container holding feature rows; or a true grid where the
first column lists criteria and each option is a column. Highlight the recommended option's
header in a strong color and the rest in neutral. Use ✓ / ✗ / — (as cell text) or colored
chips (green/red/neutral) for at-a-glance scanning.

```xml
<!-- Option column header (recommended → strong color) -->
<mxCell id="opt-b" value="Option B&#xa;(Recommended)" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fillColor=#A7F3D0;fontColor=#065F46;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="520" y="120" width="220" height="56" as="geometry" />
</mxCell>
<!-- A "yes" feature cell -->
<mxCell id="b-feat1" value="✓ Built-in auth" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=12;fillColor=#D1FAE5;fontColor=#065F46;strokeColor=none;opacity=90;" vertex="1" parent="1">
  <mxGeometry x="520" y="186" width="220" height="44" as="geometry" />
</mxCell>
```

## Pattern C — 2×2 quadrant

Four equal squares meeting at a center, plus two axis labels. Use it for prioritization
(impact × effort), positioning maps, etc. Give the four quadrants a tinted background and place
items as small chips at their (x,y) position within a quadrant.

```xml
<!-- Quadrant background (top-right = high/high → strong color) -->
<mxCell id="q-tr" value="High Impact · Low Effort&#xa;(Quick Wins)" style="rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=top;spacingTop=10;fontSize=13;fontStyle=1;fillColor=#ECFDF5;fontColor=#065F46;strokeColor=#D1FAE5;strokeWidth=1;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="600" y="160" width="360" height="280" as="geometry" />
</mxCell>
<!-- Axis labels as text cells along the middle lines; items as chips placed inside quadrants -->
```

Draw the dividing cross as two thin rectangles or edges through the center, and put axis names
at the extremes (`text` cells, italic).

## Pattern D — Mind map

A central topic with branches fanning out; each branch can have sub-branches. Place the root in
the center, level-1 nodes around it (see hub-and-spoke math in `architecture.md`), and level-2
nodes further out along each branch's direction. Connect with curved or straight edges
(`endArrow=none`), coloring each main branch (and its descendants) one family so subtrees are
visually distinct.

```xml
<mxCell id="root" value="Central Topic" style="rounded=1;arcSize=40;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fillColor=#1F2937;fontColor=#FFFFFF;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="520" y="380" width="180" height="70" as="geometry" />
</mxCell>
<mxCell id="branch-1" value="Branch A" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="220" y="200" width="150" height="50" as="geometry" />
</mxCell>
<mxCell id="e-b1" style="edgeStyle=none;rounded=1;html=1;endArrow=none;strokeWidth=2;strokeColor=#A5B4FC;curved=1;" edge="1" parent="1" source="root" target="branch-1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Pattern E — Kanban board

Vertical columns (status lanes) each holding stacked cards. Each column is a Container; each
card is a child (geometry relative to the column). Equal-width columns laid left→right; cards
stack with a constant vertical step inside.

```xml
<mxCell id="col-todo" value="To Do" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;align=center;verticalAlign=top;spacingTop=8;fontSize=14;fontStyle=1;fillColor=#E5E7EB;fontColor=#1F2937;strokeColor=#94A3B8;strokeWidth=1;opacity=90;" vertex="1" parent="1">
  <mxGeometry x="60" y="120" width="260" height="520" as="geometry" />
</mxCell>
<mxCell id="card-1" value="Set up CI" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacingLeft=10;fontSize=12;fillColor=#FFFFFF;fontColor=#1F2937;strokeColor=#D1D5DB;strokeWidth=1;" vertex="1" parent="col-todo">
  <mxGeometry x="16" y="44" width="228" height="56" as="geometry" />
</mxCell>
```

Color a card's left edge by priority by giving it a colored `strokeColor` + thicker
`strokeWidth`, or add a small colored chip child for a label/tag.
