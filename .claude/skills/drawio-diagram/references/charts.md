# Statistical charts (bar / pie / line)

Draw.io has no data-binding engine — a chart is just shapes you place at **computed
coordinates**. So the job here is arithmetic: map each data value to a pixel position with a
consistent scale, then draw the bar/slice/point. Do the math explicitly (write the numbers
into the geometry) rather than eyeballing.

> When the user really wants flexible, data-heavy charts, say so honestly — a real charting
> tool is better. Draw.io charts shine for a *small, fixed* set of values embedded in a larger
> diagram or slide. For more than ~12 bars or multi-series clutter, suggest the alternative.

Colors come from the shared palette in SKILL.md. One series = one color family.

## Contents
- [Define the plot area first](#define-the-plot-area-first)
- [Bar chart](#bar-chart)
- [Pie / donut](#pie--donut)
- [Line chart](#line-chart)

---

## Define the plot area first

Pick these numbers once, then every shape derives from them:

```
originX     = left edge of plotting area (where the Y axis sits), e.g. 120
baselineY   = the X axis (bottom of bars),                        e.g. 520
plotW       = width of plotting area,                             e.g. 900
plotH       = max bar height in pixels,                           e.g. 360   (so top of plot = baselineY - plotH = 160)
maxVal      = the largest data value, rounded up to a "nice" number for the scale
```

**Size the page last.** These coordinates are absolute, so after you've placed every shape,
set `pageWidth`/`pageHeight` in the skeleton to contain the rightmost/bottommost edge plus a
~40px margin. With the example numbers the last bar ends near x≈880 and labels reach y≈546, so
a 1000×640 (or larger) page fits; don't leave the default 1200×800 if your data needs more
width for many bars.

Draw the axes as two thin rectangles (crisp and easy) or as edges:

```xml
<!-- Y axis -->
<mxCell id="axis-y" value="" style="rounded=0;fillColor=#94A3B8;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="120" y="160" width="2" height="362" as="geometry" />
</mxCell>
<!-- X axis (baseline) -->
<mxCell id="axis-x" value="" style="rounded=0;fillColor=#94A3B8;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="120" y="520" width="900" height="2" as="geometry" />
</mxCell>
```

## Bar chart

For N bars, choose a bar width `barW` and gap `gap` so `N*barW + (N-1)*gap ≤ plotW` (leave
some left padding `pad`). Then for bar k (k = 0..N-1) with value `v`:

```
barH = round(v / maxVal * plotH)
x    = originX + pad + k * (barW + gap)
y    = baselineY - barH
```

Worked example — data `Q1=80, Q2=140, Q3=110, Q4=200`, `maxVal=200`, `plotH=360`,
`baselineY=520`, `originX=120`, `pad=40`, `barW=120`, `gap=80`:
- Q1: barH = 80/200*360 = 144 → y = 376, x = 160
- Q2: barH = 252 → y = 268, x = 360
- Q3: barH = 198 → y = 322, x = 560
- Q4: barH = 360 → y = 160, x = 760

```xml
<!-- One bar (Q2). Put the value label as a separate text cell just above it. -->
<mxCell id="bar-q2" value="" style="rounded=1;arcSize=6;fillColor=#A5B4FC;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="360" y="268" width="120" height="252" as="geometry" />
</mxCell>
<mxCell id="val-q2" value="140" style="text;html=1;align=center;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#1E3A8A;" vertex="1" parent="1">
  <mxGeometry x="360" y="244" width="120" height="20" as="geometry" />
</mxCell>
<!-- Category label below the baseline -->
<mxCell id="cat-q2" value="Q2" style="text;html=1;align=center;verticalAlign=middle;fontSize=12;fontColor=#374151;" vertex="1" parent="1">
  <mxGeometry x="360" y="526" width="120" height="20" as="geometry" />
</mxCell>
```

Variations:
- **Grouped bars**: treat each group as a slot; place sub-bars side by side inside the slot,
  each a different color family; add a legend (small colored boxes + labels) top-right.
- **Stacked bars**: stack segments in one column — segment heights derived from each value,
  each segment's `y` = previous segment's `y` − this segment's height.
- **Horizontal bars**: swap roles — bars grow rightward from a left baseline; `barLen =
  v/maxVal*plotW`, fixed bar height, stacked top→down. Better when category names are long.

## Pie / donut

Use the built-in pie-slice shape. Each slice is one cell:
`shape=pie;startAngle=<a>;endAngle=<b>;` where **a and b are fractions of the full circle in
[0,1]**, swept around a circle. Convert each datum to a fraction of the total and accumulate:

```
total      = sum of all values
frac_k     = v_k / total
start_0    = 0
start_k    = start_(k-1) + frac_(k-1)        (running cumulative start)
end_k      = start_k + frac_k
```

All slices share the same `x,y,width,height` (the bounding circle). Worked example —
`A=50, B=30, C=20`, total=100 → fractions 0.5, 0.3, 0.2:
- A: startAngle=0,   endAngle=0.5
- B: startAngle=0.5, endAngle=0.8
- C: startAngle=0.8, endAngle=1.0

```xml
<mxCell id="slice-a" value="A 50%" style="shape=pie;startAngle=0;endAngle=0.5;whiteSpace=wrap;html=1;fillColor=#A5B4FC;strokeColor=#FFFFFF;strokeWidth=2;fontColor=#1E3A8A;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="420" y="200" width="320" height="320" as="geometry" />
</mxCell>
<mxCell id="slice-b" value="B 30%" style="shape=pie;startAngle=0.5;endAngle=0.8;whiteSpace=wrap;html=1;fillColor=#A7F3D0;strokeColor=#FFFFFF;strokeWidth=2;fontColor=#065F46;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="420" y="200" width="320" height="320" as="geometry" />
</mxCell>
<mxCell id="slice-c" value="C 20%" style="shape=pie;startAngle=0.8;endAngle=1;whiteSpace=wrap;html=1;fillColor=#C4B5FD;strokeColor=#FFFFFF;strokeWidth=2;fontColor=#5B21B6;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="420" y="200" width="320" height="320" as="geometry" />
</mxCell>
```

A white `strokeColor` with `strokeWidth=2` gives the clean separated-slice look. For a
**donut**, add `innerRadius` is not supported on `shape=pie`; instead overlay a background-
colored circle (`ellipse;fillColor=#f8f9fa;strokeColor=none;`) centered on the pie.

**No-ambiguity fallback (recommended when exact slice direction matters):** a 100% stacked
horizontal bar reads proportions just as well and is trivially correct — one rectangle per
category, width = `frac_k * totalBarWidth`, laid end to end. Use this if you can't verify the
pie renders correctly.

## Line chart

Plot points at computed coordinates and connect them. Markers are small circles; the line is
edges between consecutive markers (or a polyline edge with waypoints). For series of N points
with even spacing:

```
stepX = plotW / (N - 1)
x_k   = originX + k * stepX
y_k   = baselineY - round(v_k / maxVal * plotH)
```

```xml
<!-- A marker (centered on the point: subtract half the 10px size) -->
<mxCell id="pt-0" value="" style="ellipse;fillColor=#A5B4FC;strokeColor=#FFFFFF;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="115" y="375" width="10" height="10" as="geometry" />
</mxCell>
<mxCell id="pt-1" value="" style="ellipse;fillColor=#A5B4FC;strokeColor=#FFFFFF;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="295" y="195" width="10" height="10" as="geometry" />
</mxCell>
<!-- Segment connecting marker 0 → 1 -->
<mxCell id="seg-0" style="edgeStyle=none;html=1;endArrow=none;strokeWidth=2;strokeColor=#A5B4FC;" edge="1" parent="1" source="pt-0" target="pt-1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Connecting markers by `source`/`target` keeps the line attached if you nudge a point.
For multiple series, repeat with a different color family and add a legend.
Add value labels as small `text` cells slightly above each marker, and category labels along
the baseline like the bar chart.
