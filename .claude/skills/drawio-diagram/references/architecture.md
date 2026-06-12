# Architecture / Topology

For showing **how parts connect, depend on, or layer over each other**: system architecture,
microservices, layered (n-tier) stacks, module dependency, network topology, and
ecosystem/hub-and-spoke overviews.

All style strings and colors come from the shared design system in SKILL.md. The patterns
below are the *layout shapes*; swap color families per logical group.

## Contents
- [Pattern A — Layered architecture (tiers)](#pattern-a--layered-architecture-tiers)
- [Pattern B — Hub & spoke / ecosystem](#pattern-b--hub--spoke--ecosystem)
- [Pattern C — Grouped components with dependencies](#pattern-c--grouped-components-with-dependencies)
- [Shapes & connector cheatsheet](#shapes--connector-cheatsheet)

---

## Pattern A — Layered architecture (tiers)

Horizontal bands stacked top→bottom (e.g. UI → Service → Data). Each band is a Container; the
components sit inside as children. Edges flow downward between adjacent tiers. Give each tier
its own color family so the layers read at a glance.

Layout math: full-width bands at the same `x` and `width`, stacked with a constant `y` step
(band height + gap). Children are placed relative to their band.

```xml
<!-- Tier 1 container (blue) -->
<mxCell id="tier-ui" value="Presentation Layer" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=14;fontStyle=1;fillColor=#EEF2FF;fontColor=#1E3A8A;strokeColor=#C7D2FE;strokeWidth=1;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="60" y="100" width="1080" height="120" as="geometry" />
</mxCell>
<mxCell id="ui-web" value="Web App" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=0;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="tier-ui">
  <mxGeometry x="40" y="45" width="200" height="55" as="geometry" />
</mxCell>
<mxCell id="ui-mobile" value="Mobile App" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=0;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="tier-ui">
  <mxGeometry x="280" y="45" width="200" height="55" as="geometry" />
</mxCell>

<!-- Tier 2 container (green), 140px below tier 1 -->
<mxCell id="tier-svc" value="Service Layer" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=14;fontStyle=1;fillColor=#ECFDF5;fontColor=#065F46;strokeColor=#D1FAE5;strokeWidth=1;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="60" y="240" width="1080" height="120" as="geometry" />
</mxCell>
<mxCell id="svc-api" value="API Gateway" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fillColor=#A7F3D0;fontColor=#065F46;strokeColor=none;opacity=95;" vertex="1" parent="tier-svc">
  <mxGeometry x="40" y="45" width="200" height="55" as="geometry" />
</mxCell>

<!-- Cross-tier edge: attach bottom-center of source to top-center of target -->
<mxCell id="e-ui-svc" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;strokeWidth=2;strokeColor=#94A3B8;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="ui-web" target="svc-api">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Note: an edge between two cells in *different* containers should have `parent="1"`, and its
`source`/`target` still reference the children by id directly.

## Pattern B — Hub & spoke / ecosystem

One central node, satellites radiating around it. Good for "X and everything it talks to" or a
platform with its integrations. Place the hub at canvas center; distribute spokes on a circle.

Position math for N spokes around center `(cx, cy)` at radius `r` (each box `w×h`):
for spoke k (k = 0..N-1), `angle = 2π·k/N - π/2` (start at top), then
`x = cx + r·cos(angle) - w/2`, `y = cy + r·sin(angle) - h/2`.
Typical: `cx=600, cy=420, r=260`. Use radius ≥ (largest box dimension + 120) so nothing overlaps.

```xml
<!-- Hub: dark/neutral, larger -->
<mxCell id="hub" value="Core Platform" style="ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fillColor=#1F2937;fontColor=#FFFFFF;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="500" y="360" width="200" height="120" as="geometry" />
</mxCell>
<!-- Spoke (repeat with computed x,y; rotate color family or keep one) -->
<mxCell id="spoke-auth" value="Auth Service" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#A5B4FC;fontColor=#1E3A8A;strokeColor=none;opacity=95;" vertex="1" parent="1">
  <mxGeometry x="520" y="120" width="160" height="70" as="geometry" />
</mxCell>
<!-- Connect hub to each spoke; floating attach (no exit/entry) lets draw.io pick the nearest edge -->
<mxCell id="e-hub-auth" style="edgeStyle=none;html=1;endArrow=none;strokeWidth=2;strokeColor=#94A3B8;" edge="1" parent="1" source="hub" target="spoke-auth">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

For ecosystems where the relationship is non-directional, `endArrow=none` reads cleaner than
arrows. Use `edgeStyle=none` (straight lines) for radial spokes so they point at the hub.

## Pattern C — Grouped components with dependencies

Free-placed component boxes grouped into labeled boxes (bounded contexts, teams, zones), with
directional dependency arrows between components. Use this when the structure isn't a clean
stack or star. Group with Containers (Pattern A style) and draw orthogonal edges between
components, choosing `exit*/entry*` so arrows don't cross boxes.

Tips:
- Keep dependency arrows mostly one direction (e.g. left→right or top→down) to imply flow.
- Label an edge by putting text in its `value` (e.g. `value="REST"` / `value="gRPC"`).
- A dashed edge (`dashed=1`) reads as an optional / async / weaker dependency.

## Shapes & connector cheatsheet

Append to a vertex `style` to change the shape (default is rectangle when `rounded` is set):

| Meaning              | Style fragment |
|----------------------|----------------|
| Rounded box (default)| `rounded=1;arcSize=12;` |
| Sharp rectangle      | `rounded=0;` |
| Database / datastore | `shape=cylinder3;` (or `shape=cylinder;`) |
| Queue / pipe         | `shape=process;` |
| Cloud / external     | `shape=cloud;` |
| Actor / user         | `shape=mxgraph.basic.user;` or `shape=actor;` |
| Decision / gateway   | `rhombus;` |
| Circle / node        | `ellipse;` |
| Document             | `shape=document;` |
| Clean line icons (user, db, server, robot, cloud…) | use the bundled helper — see `references/icons.md` |
| Cloud-vendor logos (AWS/Azure/GCP/K8s) | verbatim stencil strings in `references/icons.md` |

Connector variants (edge `style`):

| Meaning                 | Style fragment |
|-------------------------|----------------|
| Directional (default)   | `endArrow=classic;endFill=1;` |
| Bidirectional           | `startArrow=classic;startFill=1;endArrow=classic;endFill=1;` |
| Association (no arrow)   | `endArrow=none;` |
| Async / optional         | `dashed=1;` |
| Orthogonal routing       | `edgeStyle=orthogonalEdgeStyle;` |
| Straight                 | `edgeStyle=none;` |
| Attach points (0..1)     | `exitX=0.5;exitY=1;entryX=0.5;entryY=0;` |
