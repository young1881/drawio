# Icons

Icons turn abstract boxes into something readable at a glance — a person, a database, a
robot. Use them whenever a node represents a concrete real-world thing. There are two reliable
mechanisms; pick by what the node is.

> **The one hard rule:** never invent a draw.io stencil name. draw.io can't validate stencil
> names offline, and a wrong name (`mxgraph.aws4.lambdaa`) renders as a *blank* shape the user
> only discovers on open. Use the bundled icon set (below) or a vendor stencil string copied
> verbatim from the [catalog](#cloud-vendor-stencils). If nothing fits, fall back to a labeled
> generic shape — a clear box beats a blank icon.

## Contents
- [Mechanism 1 — bundled line icons (the clean, uniform look)](#mechanism-1--bundled-line-icons)
- [Concept → icon map](#concept--icon-map)
- [Layout recipes](#layout-recipes)
- [Mechanism 2 — cloud vendor stencils](#cloud-vendor-stencils)

---

## Mechanism 1 — bundled line icons

For generic concepts (user, file, search, database, server, robot, shield, clock, …) use the
bundled set. They are uniform 24×24 single-stroke icons, recolored on demand and embedded as a
base64 SVG data-URI, so they render everywhere, survive PNG/SVG export, and stay visually
consistent — the look in a polished architecture slide. **Recolor each icon to its box's accent
font color** so the icon matches the group (blue layer → `#1E3A8A`, green → `#065F46`, etc.).

Don't hand-write the data-URI. Use the helper, which recolors + encodes for you:

```bash
# See what's available (names + concept aliases)
python3 scripts/icon_cell.py --list

# Just the style fragment — paste into an existing cell's style="..."
python3 scripts/icon_cell.py database --color "#1E3A8A"

# A full <mxCell> to drop into <root> (icon as a child of a container panel)
python3 scripts/icon_cell.py user --color "#1E3A8A" --cell --id ico-user \
    --x 20 --y 18 --size 40 --parent panel-episodic

# A labeled icon node (icon with the label centered below it)
python3 scripts/icon_cell.py server --color "#065F46" --cell --id n-api \
    --x 80 --y 120 --size 48 --label "API Gateway" --parent 1
```

The helper accepts concept aliases (`robot`→bot, `magnifier`→search, `gem`→diamond,
`pencil`→edit, `funnel`→filter, `auth`→lock, `service`→server, …), so you can call it with the
word that fits your content. An icon cell is just an `image` vertex — it validates like any
other shape, and you place/parent it like any other cell (child geometry is relative to its
parent container).

To inspect or theme the raw SVGs, `python3 scripts/icon_cell.py --export-dir assets/icons`
writes them as editable `stroke="currentColor"` files (already exported under `assets/icons/`).

## Concept → icon map

| If the node is…                          | Icon name (or alias)        |
|------------------------------------------|------------------------------|
| A person / end user / customer           | `user` (`person`, `customer`)|
| A team / multiple users                  | `users` (`team`)             |
| A single document / record               | `file` (`document`)          |
| A document store / episodic log / corpus | `files` (`stack`, `episodic`)|
| Search / retrieval / a query             | `search` (`magnifier`, `retrieval`) |
| Core / distilled / valuable memory       | `diamond` (`gem`, `core`)    |
| An AI agent / LLM / bot                  | `bot` (`agent`, `ai`, `llm`) |
| Write / edit / append                    | `edit` (`pencil`, `write`)   |
| Integrity / security / high-fidelity     | `shield` (`security`)        |
| A message / low-density text / comment   | `message` (`chat`)           |
| Time / history / timestamp               | `clock` (`time`)             |
| Update / overwrite / sync / cycle        | `refresh` (`sync`, `update`) |
| Distill / condense / filter              | `filter` (`funnel`, `distill`) |
| Metrics / high info density / stats      | `bar-chart` (`metrics`, `density`) |
| A stable goal / objective / baseline     | `target` (`goal`)            |
| A service / host / backend / API         | `server` (`service`, `api`)  |
| A database / datastore                   | `database` (`db`, `sql`)     |
| A cache / event / fast path              | `zap` (`cache`, `flash`)     |
| Cloud / external platform                | `cloud`                      |
| Compute / processor                      | `cpu` (`compute`, `chip`)    |
| Layers / tiers                           | `layers` (`tier`)            |
| Auth / lock / private                    | `lock` (`auth`, `secure`)    |
| Web / internet / network                 | `globe` (`web`, `network`)   |
| Mobile app / phone                       | `smartphone` (`mobile`, `app`) |
| Desktop / frontend / screen              | `monitor` (`frontend`)       |
| Config / ops / settings                  | `settings` (`gear`, `config`) |
| Success / pass / done                    | `check-circle` (`success`)   |
| Warning / risk / error                   | `alert-triangle` (`risk`, `warning`) |
| Email / inbox                            | `mail` (`email`)             |
| Folder / directory                       | `folder`                     |
| Secret / credential / token              | `key` (`secret`, `token`)    |
| Code / build / CI                        | `code` (`build`, `ci`)       |
| Repo / branch / VCS                      | `git-branch` (`repo`)        |
| Flow / next                              | `arrow-right`                |

Run `--list` for the authoritative set; it's easy to extend by adding an entry to `ICONS` in
`scripts/icon_cell.py`.

## Layout recipes

These reproduce the common "iconified" looks. Mix them with the architecture / flowchart
patterns — an icon is just an extra child cell.

### Recipe A — Panel header with left icon + title (layer / module headers)

A large titled panel (a Container) with the icon on the left and a bilingual title to its
right; feature rows go below. This is the Episodic/Core-Memory look.

```xml
<!-- the panel (blue layer) -->
<mxCell id="panel-episodic" value="" style="rounded=1;arcSize=6;html=1;fillColor=#EEF2FF;strokeColor=#C7D2FE;strokeWidth=1;opacity=90;" vertex="1" parent="1">
  <mxGeometry x="120" y="120" width="760" height="220" as="geometry" />
</mxCell>
<!-- icon (child; from: icon_cell.py files --color "#1E3A8A" --cell --id ico-epi --x 28 --y 26 --size 44 --parent panel-episodic) -->
<!-- ...paste the generated <mxCell> here... -->
<!-- title text (child, to the right of the icon) -->
<mxCell id="epi-title" value="Episodic Memory（情节记忆）" style="text;html=1;align=left;verticalAlign=middle;fontSize=18;fontStyle=1;fontColor=#1E3A8A;" vertex="1" parent="panel-episodic">
  <mxGeometry x="88" y="26" width="640" height="30" as="geometry" />
</mxCell>
<mxCell id="epi-tags" value="追加写入 (Append-Only) · 高保真 (High-Fidelity) · 保留上下文" style="text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor=#1E3A8A;" vertex="1" parent="panel-episodic">
  <mxGeometry x="88" y="58" width="640" height="22" as="geometry" />
</mxCell>
```

The panel's own `value` is empty here on purpose: the title lives in a separate child text cell
so the icon can sit beside it. (This differs from the plain container in `architecture.md`
Pattern A, which keeps the title in the container's own `value` — that's fine when there's no
icon. Once you add a header icon, switch to the empty-value + child-title form.)

### Recipe B — Feature row (small icon + bold label + sub-label)

A row of N equal cells, each a small icon over/left of a bold label and a gray caption — the
pencil/shield/message/clock row. Place these as children of the panel, below the header. The
feature-cell wrapper has `fillColor=none;strokeColor=none;` — it's invisible layout scaffolding
whose only job is to anchor the icon/label children's relative geometry as a movable unit.

```xml
<!-- one feature cell (child of the panel); add the icon via icon_cell.py at --size 24 -->
<mxCell id="feat-append" value="" style="rounded=1;arcSize=6;html=1;fillColor=none;strokeColor=none;" vertex="1" parent="panel-episodic">
  <mxGeometry x="28" y="110" width="170" height="80" as="geometry" />
</mxCell>
<!-- icon: icon_cell.py edit --color "#1E3A8A" --cell --id fi-append --x 0 --y 6 --size 24 --parent feat-append -->
<mxCell id="feat-append-t" value="追加写入" style="text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=1;fontColor=#1E3A8A;" vertex="1" parent="feat-append">
  <mxGeometry x="34" y="0" width="136" height="22" as="geometry" />
</mxCell>
<mxCell id="feat-append-s" value="不可覆盖" style="text;html=1;align=left;verticalAlign=top;fontSize=11;fontColor=#6B7280;" vertex="1" parent="feat-append">
  <mxGeometry x="34" y="24" width="136" height="34" as="geometry" />
</mxCell>
```

### Recipe C — Labeled icon node (icon with text below)

A compact node where the icon *is* the node and the label sits beneath — good for actors and
endpoints in an architecture/flow ("用户会话", "AI Agent"). One call does it:

```bash
python3 scripts/icon_cell.py user --color "#1F2937" --cell --id n-user \
    --x 380 --y 40 --size 40 --label "用户会话 / User" --parent 1
```

Connect labeled icon nodes with the standard edges from the flowchart/architecture references.

### Recipe D — Boxed icon node (icon-left, label-right, inside a fill)

The most common node shape in a polished architecture diagram: a filled box with the icon on
the left and a bold title (plus optional sub-line) on the right — e.g. the "用户会话" and
"AI Agent" boxes. Build it as a box with two children (an icon and the text); connect these
boxes with normal edges.

```xml
<mxCell id="n-user" value="" style="rounded=1;arcSize=10;html=1;fillColor=#FFFFFF;strokeColor=#C7D2FE;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="360" y="40" width="320" height="70" as="geometry" />
</mxCell>
<!-- icon child: icon_cell.py user --color "#1E3A8A" --cell --id ico-nu --x 18 --y 19 --size 32 --parent n-user -->
<mxCell id="nu-title" value="用户会话（原始对话流）" style="text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;fontColor=#1F2937;" vertex="1" parent="n-user">
  <mxGeometry x="64" y="14" width="240" height="22" as="geometry" />
</mxCell>
<mxCell id="nu-sub" value="User Conversation / Turns" style="text;html=1;align=left;verticalAlign=middle;fontSize=11;fontColor=#6B7280;" vertex="1" parent="n-user">
  <mxGeometry x="64" y="36" width="240" height="20" as="geometry" />
</mxCell>
```

Tip: keep the icon vertically centered (box height 70, icon 32 → `y = (70-32)/2 = 19`) and start
the text at `x ≈ icon_x + icon_size + 14` so the columns align.

## Cloud vendor stencils

For real cloud-service logos, draw.io's *vendor* stencils are consistent and reliable — use
these verbatim (don't bundle anything). The AWS pattern puts the service glyph in a colored
square via `resIcon`; Azure/GCP/K8s expose named shapes. These are stable, known-good strings:

```
AWS (aws4) — colored resource icon:
  Lambda      sketch=0;outlineConnect=0;html=1;aspect=fixed;align=center;verticalLabelPosition=bottom;verticalAlign=top;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;
  EC2         ...resIcon=mxgraph.aws4.ec2;
  S3          ...resIcon=mxgraph.aws4.s3;
  RDS         ...resIcon=mxgraph.aws4.rds;
  DynamoDB    ...resIcon=mxgraph.aws4.dynamodb;
  API Gateway ...resIcon=mxgraph.aws4.api_gateway;
  (the leading props are identical; only resIcon changes)

Azure (mxgraph.azure):
  VM          shape=mxgraph.azure.virtual_machine;html=1;
  SQL DB      shape=mxgraph.azure.sql_database;html=1;
  Functions   shape=mxgraph.azure.function_apps;html=1;

GCP (mxgraph.gcp2):
  Compute     shape=mxgraph.gcp2.compute_engine;html=1;
  Cloud SQL   shape=mxgraph.gcp2.cloud_sql;html=1;
  GKE         shape=mxgraph.gcp2.kubernetes_engine;html=1;

Kubernetes (mxgraph.kubernetes):
  Pod         shape=mxgraph.kubernetes.pod;html=1;
  Service     shape=mxgraph.kubernetes.svc;html=1;
```

Give vendor icons a label via the cell `value` and `verticalLabelPosition=bottom`. If you need a
service not listed, prefer a bundled generic icon (`server`, `database`, `cloud`) with a text
label over guessing a `resIcon` name — a labeled generic shape never renders blank.
