# Flowchart / Process

For **ordered steps, decisions/branches, who-does-what lanes, state transitions, and
timelines**. The common thread is *sequence* — one thing leads to the next, sometimes
branching on a condition.

Style strings and colors come from the shared design system in SKILL.md.

## Contents
- [Pattern A — Linear / branching flowchart](#pattern-a--linear--branching-flowchart)
- [Pattern B — Swimlanes (who does what)](#pattern-b--swimlanes-who-does-what)
- [Pattern C — State machine](#pattern-c--state-machine)
- [Pattern D — Timeline / roadmap](#pattern-d--timeline--roadmap)
- [Flowchart shape vocabulary](#flowchart-shape-vocabulary)

---

## Pattern A — Linear / branching flowchart

Top-to-bottom is the default reading direction (use left-to-right for short, wide flows).
Standard flowchart grammar: rounded **terminator** (start/end), **rectangle** (process step),
**diamond** (decision, 2+ labeled outgoing edges). Keep one vertical centerline; branch
decisions out to the side and merge back.

Layout: fixed column x for the main spine, constant vertical step (e.g. 100px between box
tops). Decisions send a "Yes" edge straight down and a "No" edge out to a side column.

```xml
<!-- Start terminator -->
<mxCell id="start" value="Start" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#A7F3D0;fontColor=#065F46;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="500" y="80" width="160" height="50" as="geometry" />
</mxCell>
<!-- Process step -->
<mxCell id="step-validate" value="Validate input" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="500" y="180" width="160" height="60" as="geometry" />
</mxCell>
<!-- Decision -->
<mxCell id="dec-valid" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#FDE68A;fontColor=#92400E;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="510" y="290" width="140" height="90" as="geometry" />
</mxCell>
<!-- End terminator -->
<mxCell id="end" value="Done" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#D1D5DB;fontColor=#1F2937;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="500" y="440" width="160" height="50" as="geometry" />
</mxCell>

<!-- Sequence edges; put the branch label in the edge value -->
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="start" target="step-validate">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell id="e-yes" value="Yes" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=0.5;exitY=1;entryX=0.5;entryY=0;fontSize=11;fontColor=#374151;" edge="1" parent="1" source="dec-valid" target="end">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- "No" loops back: leave the diamond on the left, return to a previous step's left side -->
<mxCell id="e-no" value="No" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=0;exitY=0.5;entryX=0;entryY=0.5;fontSize=11;fontColor=#374151;" edge="1" parent="1" source="dec-valid" target="step-validate">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Decision discipline: every diamond needs labeled outgoing edges covering each outcome.
Color steps by phase if the flow has distinct stages (e.g. all "ingest" steps blue, all
"process" steps green).

### Routing loop-back & merge edges with waypoints

A "No → go back" or a long merge edge often needs to detour around other boxes instead of
cutting straight through them. Force the path by adding explicit waypoints — an `<Array
as="points">` of `<mxPoint>`s inside the edge's `<mxGeometry>`. The edge leaves `source` at its
`exit` point, passes through each waypoint in order, then enters `target` at its `entry` point.
A clean loop-back routes out to one side, up the margin, and back in:

```xml
<mxCell id="e-no" value="No" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=1;exitY=0.5;entryX=1;entryY=0.5;fontSize=11;fontColor=#374151;" edge="1" parent="1" source="dec-valid" target="step-validate">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="760" y="335" />
      <mxPoint x="760" y="210" />
    </Array>
  </mxGeometry>
</mxCell>
```

Here the edge exits the diamond's right side, goes out to x=760 (clear of the spine), travels
up to the target's level, then enters the step's right side. Pick a waypoint x/y that sits in
empty space — outside every box's bounds — so the line never overlaps a shape.

## Pattern B — Swimlanes (who does what)

Use the built-in `swimlane` shape: a titled lane that acts as a container for the steps that
role/system performs. Horizontal lanes stack vertically; a step's `parent` is its lane, so its
geometry is relative to the lane. Cross-lane edges (`parent="1"`) show hand-offs.

```xml
<!-- A pool of horizontal lanes: nest child lanes in a parent swimlane -->
<mxCell id="pool" value="Order Process" style="swimlane;html=1;startSize=30;horizontal=0;fontSize=14;fontStyle=1;fillColor=none;strokeColor=#94A3B8;" vertex="1" parent="1">
  <mxGeometry x="60" y="100" width="1080" height="360" as="geometry" />
</mxCell>
<mxCell id="lane-customer" value="Customer" style="swimlane;html=1;startSize=30;horizontal=0;fontSize=13;fontStyle=1;fillColor=#EEF2FF;fontColor=#1E3A8A;strokeColor=#C7D2FE;" vertex="1" parent="pool">
  <mxGeometry x="30" y="0" width="1050" height="120" as="geometry" />
</mxCell>
<mxCell id="lane-system" value="System" style="swimlane;html=1;startSize=30;horizontal=0;fontSize=13;fontStyle=1;fillColor=#ECFDF5;fontColor=#065F46;strokeColor=#D1FAE5;" vertex="1" parent="pool">
  <mxGeometry x="30" y="120" width="1050" height="120" as="geometry" />
</mxCell>
<!-- Step inside a lane (geometry is relative to lane-customer) -->
<mxCell id="s-place" value="Place order" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=12;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="lane-customer">
  <mxGeometry x="40" y="40" width="150" height="50" as="geometry" />
</mxCell>
```

`horizontal=0` makes a lane title read vertically on the left (the usual look for horizontal
lanes). For vertical lanes (columns), drop `horizontal=0`.

## Pattern C — State machine

Circles/rounded boxes for states, directional edges for transitions labeled with the trigger.
A small filled circle marks the initial state. Lay states out where transitions cross least —
often a rough circle or left-to-right chain. Self-transitions are edges with the same source
and target.

```xml
<mxCell id="init" value="" style="ellipse;fillColor=#1F2937;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="80" y="200" width="24" height="24" as="geometry" />
</mxCell>
<mxCell id="st-idle" value="Idle" style="rounded=1;arcSize=40;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="160" y="186" width="120" height="52" as="geometry" />
</mxCell>
<mxCell id="t-start" value="start()" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;fontSize=11;fontColor=#374151;" edge="1" parent="1" source="st-idle" target="st-running">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- self-transition -->
<mxCell id="t-retry" value="retry" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;fontSize=11;" edge="1" parent="1" source="st-running" target="st-running">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Pattern D — Timeline / roadmap

A horizontal spine with milestones along it, or sequential phase boxes connected by arrows.
For dated milestones, draw one long thin line and hang labeled markers off it; for phases, use
equal-width boxes left→right with arrows between.

```xml
<!-- Phase boxes, evenly spaced left to right; one color family per phase or a gradient of one -->
<mxCell id="ph1" value="Phase 1&#xa;Discovery" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="80" y="320" width="220" height="90" as="geometry" />
</mxCell>
<mxCell id="ph2" value="Phase 2&#xa;Build" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fillColor=#A7F3D0;fontColor=#065F46;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="360" y="320" width="220" height="90" as="geometry" />
</mxCell>
<mxCell id="e-ph" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="ph1" target="ph2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

For a milestone timeline, add a date caption above/below each marker as a separate `text` cell,
alternating above/below to avoid crowding.

## Flowchart shape vocabulary

| Element            | Style fragment |
|--------------------|----------------|
| Start/End terminator | `rounded=1;arcSize=50;` (pill) |
| Process step       | `rounded=1;arcSize=10;` |
| Decision           | `rhombus;` |
| Input/Output (parallelogram) | `shape=parallelogram;perimeter=parallelogramPerimeter;` |
| Subprocess         | `shape=process;` (double-struck sides) |
| Document           | `shape=document;` |
| Manual / prep      | `shape=hexagon;` |
| Data store         | `shape=cylinder3;` |
| On-page connector  | `ellipse;` (small circle) |

Edge labels: put the condition in the edge `value` and add `fontSize=11;fontColor=#374151;` to
its style. Keep label text short ("Yes"/"No"/"timeout") so it doesn't overlap the line.
