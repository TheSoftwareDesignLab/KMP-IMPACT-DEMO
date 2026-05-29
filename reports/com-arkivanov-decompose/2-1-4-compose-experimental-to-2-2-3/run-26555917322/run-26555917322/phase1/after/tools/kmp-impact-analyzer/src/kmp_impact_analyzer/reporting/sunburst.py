"""Source-set Sunburst visualization embedded in the HTML report.

Adapted from Nuevosajustes/nuava visualizacion/generate_sunburst.py. Takes the
ConsolidatedResult produced by phase 4 (no file-system re-parsing) and builds
a D3 v7 hierarchical Sunburst grouped by source set → package directory → file.

The output is an HTML fragment (div + inline script) ready to be inserted into
report/index.html. The raw SVG (un-interactive) can also be requested for PR
comment rasterization.
"""

from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import PurePosixPath
from typing import Any

from ..contracts import ConsolidatedResult, ImpactRelation


# Source sets to display in a stable order. Files whose source_set is not in
# this list are kept under the same key they carry in the ConsolidatedResult.
SOURCE_SET_ORDER = ("commonMain", "androidMain", "iosMain", "commonTest",
                    "common", "android", "ios")


# ---------------------------------------------------------------------------
# Source-set normalisation
# ---------------------------------------------------------------------------

def _normalise_source_set(raw: str) -> str:
    """Project source_sets sometimes come as 'common' vs 'commonMain'. Keep the
    expanded form for grouping so the Sunburst matches the user's mental model.
    """
    if not raw:
        return "common"
    lower = raw.lower()
    if lower in {"common", "commonmain"}:
        return "commonMain"
    if lower in {"android", "androidmain"}:
        return "androidMain"
    if lower in {"ios", "iosmain"}:
        return "iosMain"
    if lower in {"test", "commontest"}:
        return "commonTest"
    return raw


def _arc_value(entry: dict[str, Any] | None) -> int:
    """Arc arc-span weight. Directs get the biggest slice so they stand out."""
    if entry is None:
        return 1
    rel = entry["relation"]
    if rel == "direct":
        return 10
    if rel == "expect_actual":
        return 1
    # transitive: farther distance → smaller slice, min 2
    return max(2, 6 - int(entry.get("distance", 1)))


# ---------------------------------------------------------------------------
# Hierarchy builder
# ---------------------------------------------------------------------------

def _build_tree(consolidated: ConsolidatedResult) -> dict[str, Any]:
    """Root → source-set nodes → package dirs → leaf files.

    Files come from two sources:
      1. Impacted files (trace entries) — carry full metadata.
      2. Un-impacted files (static_impact.total_project_files - impacted)
         are represented as counts, not drawn. A placeholder "non-impacted"
         child is added per source-set so the ring reflects the full project.

    Since the ConsolidatedResult doesn't enumerate non-impacted files, the
    tree is built only from known files. This is consistent with how the
    existing propagation SVG already filters.
    """
    # index: ss -> package dir -> [leaves]
    leaves_per_ss: dict[str, list[dict[str, Any]]] = defaultdict(list)

    # trace entries (impacted files with screens + metrics)
    for entry in consolidated.trace:
        p = PurePosixPath(entry.file_path)
        ss = _source_set_from_path(str(p))
        leaf = {
            "name": p.name,
            "path": str(p),
            "source_set": ss,
            "impact": entry.relation.value,
            "distance": entry.distance,
            "is_expect": False,
            "is_actual": False,
            "value": _arc_value(
                {"relation": entry.relation.value, "distance": entry.distance}
            ),
        }
        leaves_per_ss[ss].append(leaf)

    # Expect/actual pairs add flags on files already in trace (or introduce
    # new leaves if the file wasn't impacted). Build a path → leaf index.
    path_index: dict[str, dict[str, Any]] = {}
    for ss, files in leaves_per_ss.items():
        for leaf in files:
            path_index[leaf["path"]] = leaf

    # Only flag expect/actual on files that are *already* in the impact set —
    # injecting unimpacted bridge files as standalone grey arcs left the
    # diagram with floating slices the user could not interpret.
    for pair in consolidated.static_impact.expect_actual_pairs:
        expect_leaf = path_index.get(pair.expect_file)
        if expect_leaf:
            expect_leaf["is_expect"] = True
        for actual in pair.actual_files:
            act_leaf = path_index.get(actual)
            if act_leaf:
                act_leaf["is_actual"] = True

    # Assemble tree: root → source-set → dir chain → leaf
    root = {"name": "src", "children": []}
    order = [ss for ss in SOURCE_SET_ORDER if ss in leaves_per_ss]
    order += sorted(ss for ss in leaves_per_ss if ss not in SOURCE_SET_ORDER)

    for ss in order:
        ss_node = {"name": ss, "children": [], "source_set": ss}
        root["children"].append(ss_node)
        dir_map: dict[str, dict[str, Any]] = {"": ss_node}
        for leaf in sorted(leaves_per_ss[ss], key=lambda x: x["path"]):
            parts = _relative_kt_parts(leaf["path"], ss)
            for depth in range(len(parts) - 1):
                key = "/".join(parts[: depth + 1])
                parent_key = "/".join(parts[:depth])
                if key not in dir_map:
                    dir_node = {"name": parts[depth], "children": []}
                    dir_map[key] = dir_node
                    dir_map[parent_key]["children"].append(dir_node)
            leaf_parent = "/".join(parts[:-1])
            dir_map[leaf_parent]["children"].append(leaf)

    return root


def _source_set_from_path(path: str) -> str:
    """Infer source set from a file path like
    '.../src/commonMain/kotlin/foo/Bar.kt' → 'commonMain'. Falls back to
    the last directory under /src/ if no match."""
    parts = PurePosixPath(path).parts
    for i, p in enumerate(parts):
        if p == "src" and i + 1 < len(parts):
            return _normalise_source_set(parts[i + 1])
    return "commonMain"


def _relative_kt_parts(path: str, source_set: str) -> list[str]:
    """'/repo/shared/src/commonMain/kotlin/data/Repo.kt' → ['data', 'Repo.kt'].
    Strips everything up to and including 'kotlin'."""
    parts = list(PurePosixPath(path).parts)
    if "kotlin" in parts:
        idx = parts.index("kotlin")
        rel = parts[idx + 1:]
    else:
        # Fallback: strip up to the source set
        try:
            idx = parts.index(source_set)
            rel = parts[idx + 1:]
        except ValueError:
            rel = [PurePosixPath(path).name]
    if not rel:
        rel = [PurePosixPath(path).name]
    return rel


# ---------------------------------------------------------------------------
# Direct-files + expect/actual tree list (static HTML — sidebar)
# ---------------------------------------------------------------------------

def _direct_tree_html(consolidated: ConsolidatedResult) -> str:
    direct_by_ss: dict[str, list[str]] = defaultdict(list)
    for entry in consolidated.trace:
        if entry.relation == ImpactRelation.DIRECT:
            ss = _source_set_from_path(entry.file_path)
            direct_by_ss[ss].append(entry.file_path)

    if not direct_by_ss:
        return '<div class="sb-empty">No direct files.</div>'

    parts = []
    for ss in sorted(direct_by_ss):
        parts.append(f'<div class="sb-tree-ss">{html.escape(ss)}/</div>')
        for p in sorted(direct_by_ss[ss]):
            rel = _relative_kt_parts(p, ss)
            name = rel[-1]
            subdir = "/".join(rel[:-1])
            prefix = (
                f'<span class="sb-tree-dim">{html.escape(subdir)}/</span>'
                if subdir else ""
            )
            parts.append(
                '<div class="sb-tree-leaf sb-direct">'
                '<span class="sb-tree-bul"></span>'
                f'<span>{prefix}{html.escape(name)}</span>'
                '</div>'
            )
    return "".join(parts)


def _ea_tree_html(consolidated: ConsolidatedResult) -> str:
    pairs = consolidated.static_impact.expect_actual_pairs
    if not pairs:
        return ""

    parts = []
    for pair in pairs:
        expect_name = PurePosixPath(pair.expect_file).stem
        parts.append(
            f'<div class="sb-tree-ss">{html.escape(expect_name)}</div>'
        )
        entries = [(pair.expect_file, True)] + [
            (a, False) for a in pair.actual_files
        ]
        for fp, is_expect in entries:
            ss = _source_set_from_path(fp)
            rel = _relative_kt_parts(fp, ss)
            name = rel[-1]
            subdir = "/".join(rel[:-1])
            if subdir:
                prefix = (
                    f'<span class="sb-tree-dim">{html.escape(ss)}/'
                    f'{html.escape(subdir)}/</span>'
                )
            else:
                prefix = f'<span class="sb-tree-dim">{html.escape(ss)}/</span>'
            tag = (
                '<span class="sb-ea-tag">expect</span>'
                if is_expect else
                '<span class="sb-ea-tag">actual</span>'
            )
            parts.append(
                '<div class="sb-tree-leaf sb-ea">'
                '<span class="sb-tree-bul"></span>'
                f'<span>{prefix}{html.escape(name)} {tag}</span>'
                '</div>'
            )
    return "".join(parts)


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def _tree_max_depth(node: dict[str, Any], depth: int = 0) -> int:
    """Deepest leaf depth in the hierarchy (root = 0)."""
    children = node.get("children") or []
    if not children:
        return depth
    return max(_tree_max_depth(c, depth + 1) for c in children)


# Hard ceiling on visible rings — beyond ~5 rings the picture turns into a
# coloured noise spike, so anything deeper falls through to the tangential
# outer-label path. Both the D3 view and the cairosvg renderer respect this.
_RING_CEILING = 5
_RING_FLOOR = 2  # never collapse to a single ring even for tiny projects


def _visible_ring_count(tree: dict[str, Any]) -> int:
    """How many rings the sunburst should draw for *this* project.

    The root node sits at depth 0 (the white centre). Files at depth 1 fill
    the first ring, depth-2 nodes the second, etc. We render up to
    ``min(max_depth, _RING_CEILING)``.
    """
    return max(_RING_FLOOR, min(_tree_max_depth(tree), _RING_CEILING))


def build_sunburst_html(
    consolidated: ConsolidatedResult,
) -> str:
    """Build the HTML fragment (D3 Sunburst + info sidebar) to embed as a tab
    inside the report. All D3 + styles are scoped with a ``sb-`` / ``#sb-``
    prefix so they don't collide with the main report styles."""
    tree = _build_tree(consolidated)
    data_json = json.dumps(tree, ensure_ascii=False)
    visible_rings = _visible_ring_count(tree)

    dep_before = html.escape(consolidated.version_before)
    dep_after = html.escape(consolidated.version_after)
    dep_group = html.escape(consolidated.dependency_group)

    static = consolidated.static_impact
    total_files = static.total_project_files or len(consolidated.trace)
    direct_count = sum(
        1 for f in static.impacted_files if f.relation == ImpactRelation.DIRECT
    )
    trans_count = sum(
        1 for f in static.impacted_files
        if f.relation == ImpactRelation.TRANSITIVE
    )
    ea_file_count = sum(
        1 for f in static.impacted_files
        if f.relation == ImpactRelation.EXPECT_ACTUAL
    )
    ea_units = len(static.expect_actual_pairs)
    affected = direct_count + trans_count
    none_count = max(total_files - affected, 0)

    direct_rows = _direct_tree_html(consolidated)
    ea_rows = _ea_tree_html(consolidated)
    ea_block = (
        '<div><div class="sb-sec-label">Expect / Actual</div>'
        f'{ea_rows}</div>'
        if ea_rows else ""
    )

    # Single quotes used in the nested f-string because the outer is a
    # triple-quoted double-quoted string with many embedded braces escaped for
    # f-string literal output.
    return f"""
<style>
  .sb-wrap {{ background:#F5F4F0; color:#2C2C2C; padding:32px;
    border-radius:12px; border:1px solid #e2e8f0; }}
  /* Layout mirrors the GitGraph arc-diagram card on this page so a
     reviewer reading both visualisations gets the same model: a fixed
     left rail with the static lists (KPIs/files), a fixed top toolbar
     with the chart controls, and a single interactive surface (the
     circle) that responds to wheel-zoom + drag-pan. Nothing else moves. */
  .sb-card {{ display:grid; grid-template-columns:280px minmax(0,1fr);
    gap:32px; align-items:start; }}
  @media (max-width: 900px) {{
    .sb-card {{ grid-template-columns: 1fr; }}
    .sb-info {{ position:static !important; max-height:none !important; }}
    .sb-chart {{ position:static !important; max-height:none !important; }}
  }}
  /* Chart shell stays pinned while the page scrolls through the trace
     tables below; only the inner viewport ever transforms. */
  .sb-chart {{ position:sticky; top:88px; align-self:start;
    display:flex; flex-direction:column;
    max-height:calc(100vh - 110px);
    background:#FBFAF6; border:1px solid #E2E0DA; border-radius:10px;
    padding:14px; overflow:hidden; }}
  /* Toolbar above the circle — same role as the "Min. degree / Sort by /
     Showing N nodes" header in the GitGraph card. It stays put when the
     user zooms or pans inside the viewport. */
  .sb-chart-toolbar {{ display:flex; align-items:center;
    justify-content:space-between; gap:12px; padding:0 4px 10px;
    border-bottom:1px solid #E2E0DA; margin-bottom:10px;
    font-size:12px; color:#475569; user-select:none; flex:0 0 auto; }}
  .sb-chart-toolbar .sb-tool-group {{ display:flex; align-items:center;
    gap:8px; }}
  .sb-chart-toolbar button {{ font:inherit; font-size:11px;
    background:#fff; border:1px solid #D8D6D0; color:#475569;
    border-radius:5px; padding:3px 10px; cursor:pointer;
    line-height:1.4; }}
  .sb-chart-toolbar button:hover {{ background:#F1F5F9; }}
  .sb-chart-toolbar button:disabled {{ opacity:.4; cursor:default; }}
  .sb-chart-toolbar .sb-zoom-badge {{ font-variant-numeric:tabular-nums;
    background:#EEF2F6; border-radius:4px; padding:2px 8px;
    color:#1e293b; font-weight:600; min-width:54px; text-align:center; }}
  .sb-chart-toolbar .sb-tool-hint {{ color:#94a3b8; font-size:10.5px;
    letter-spacing:.04em; }}
  .sb-chart-toolbar kbd {{ background:#E2E0DA; border-radius:3px;
    padding:1px 5px; font-family:inherit; font-size:10px; color:#555; }}
  /* Pan-arrow d-pad: four square buttons arranged as a compact group
     (←/↓/↑/→) so the user can nudge the viewBox without touching the
     mouse wheel. Disabled state mirrors the zoom buttons. */
  .sb-chart-toolbar .sb-pad {{ display:inline-flex; align-items:center;
    gap:2px; margin-left:8px; padding-left:8px;
    border-left:1px solid #E2E0DA; }}
  .sb-chart-toolbar .sb-pad button {{ width:24px; height:22px; padding:0;
    font-size:13px; line-height:1; font-weight:700; }}
  /* Viewport is the ONLY interactive surface — wheel/drag are scoped
     here, so the sidebar and toolbar above never move. */
  .sb-chart-viewport {{ flex:1 1 auto; width:100%; min-height:440px;
    overflow:hidden; touch-action:none; cursor:grab;
    position:relative; border-radius:6px; background:#FBFAF6; }}
  .sb-chart-viewport:active {{ cursor:grabbing; }}
  .sb-chart-viewport svg {{ width:100%; height:100%; display:block;
    overflow:visible; }}
  .sb-info {{ display:flex; flex-direction:column; gap:14px;
    position:sticky; top:88px; align-self:start;
    max-height:calc(100vh - 110px); overflow-y:auto;
    padding-right:6px; }}
  .sb-info::-webkit-scrollbar {{ width:6px; }}
  .sb-info::-webkit-scrollbar-thumb {{ background:#cbd5e1; border-radius:3px; }}
  .sb-title {{ font-size:15px; font-weight:700; letter-spacing:-.01em; }}
  .sb-sub {{ font-size:12px; color:#888; margin-top:2px; }}
  .sb-sub .sb-ver {{ color:#B91C1C; font-weight:600; }}
  .sb-sec-label {{ font-size:11px; font-weight:700; text-transform:uppercase;
    letter-spacing:.07em; color:#777; margin-bottom:6px; padding-bottom:4px;
    border-bottom:1px solid #D8D6D0; }}
  .sb-block {{ border-radius:6px; padding:9px 11px; margin-bottom:4px; }}
  .sb-block-aff {{ background:#FEF2F2; border:1px solid #FECACA; }}
  .sb-block-safe {{ background:#F8F8F7; border:1px solid #E2E0DA; }}
  .sb-block-label {{ font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:.07em; margin-bottom:5px; }}
  .sb-block-label.sb-aff {{ color:#B91C1C; }}
  .sb-block-label.sb-saf {{ color:#555; }}
  .sb-stat-row {{ display:flex; justify-content:space-between;
    align-items:baseline; padding:3px 0;
    border-bottom:1px solid rgba(0,0,0,.05); font-size:12px; }}
  .sb-stat-row:last-child {{ border-bottom:none; }}
  .sb-stat-n {{ font-size:15px; font-weight:800; }}
  .sb-subtotal {{ display:flex; justify-content:space-between;
    align-items:baseline; padding-top:5px; margin-top:3px;
    border-top:1px solid rgba(0,0,0,.1); font-size:11px; font-weight:700; }}
  .sb-leg-row {{ display:flex; align-items:center; gap:7px; font-size:11px;
    padding:2px 0; }}
  .sb-sw {{ width:12px; height:12px; border-radius:2px; flex-shrink:0; }}
  .sb-tree-ss {{ font-size:11px; font-weight:700; color:#333;
    padding:4px 0 2px; }}
  .sb-tree-leaf {{ display:flex; align-items:flex-start; gap:6px;
    padding:1px 0 1px 10px; font-size:11px; line-height:1.5; color:#333; }}
  .sb-tree-bul {{ width:6px; height:6px; border-radius:50%; flex-shrink:0;
    margin-top:5px; }}
  .sb-tree-leaf.sb-direct .sb-tree-bul {{ background:#B91C1C; }}
  .sb-tree-leaf.sb-ea .sb-tree-bul {{ border:1.5px dashed #64748B; }}
  .sb-tree-dim {{ color:#888; }}
  .sb-ea-tag {{ font-size:9px; font-weight:700; text-transform:uppercase;
    letter-spacing:.05em; color:#64748B; background:#F1F5F9; border-radius:3px;
    padding:0 3px; vertical-align:middle; }}
  .sb-empty {{ font-size:11px; color:#9ca3af; font-style:italic; }}
  #sb-tt {{ position:fixed; background:#fff; border:1px solid #D8D6D0;
    border-radius:5px; padding:7px 11px; font-size:11px; pointer-events:none;
    box-shadow:0 2px 10px rgba(0,0,0,.08); max-width:240px; line-height:1.45;
    display:none; z-index:100; color:#2C2C2C; }}
  #sb-tt strong {{ display:block; font-size:12px; margin-bottom:1px; }}
  #sb-tt .sb-sub2 {{ color:#64748B; font-size:10px; }}
  /* Tree below the sunburst: shares the same palette so a reader sweeps
     from circle to tree and recognises the colours immediately. The tree
     card mirrors the circle card — fixed toolbar on top, scoped viewport
     that owns wheel-zoom + drag-pan + the d-pad — so the user gets the
     same interaction model on both visualisations. */
  .sb-tree-section {{ margin-top:28px; padding-top:24px;
    border-top:1px solid #D8D6D0;
    background:#FBFAF6; border-radius:10px;
    border:1px solid #E2E0DA; padding:18px 16px 16px; }}
  .sb-tree-head {{ display:flex; align-items:flex-start;
    justify-content:space-between; gap:16px; flex-wrap:wrap;
    margin-bottom:12px; }}
  .sb-tree-toolbar {{ padding:0 4px 0; border-bottom:none;
    margin-bottom:0; align-self:center; }}
  .sb-tree-title {{ font-size:13px; font-weight:700; color:#2C2C2C;
    letter-spacing:-.01em; }}
  .sb-tree-sub {{ font-size:11.5px; color:#888; margin:2px 0 0; }}
  .sb-tree-viewport {{ width:100%; height:560px;
    overflow:hidden; touch-action:none; cursor:grab;
    position:relative; border-radius:6px; background:#FBFAF6;
    border:1px dashed #E2E0DA; }}
  .sb-tree-viewport:active {{ cursor:grabbing; }}
  #sb-tree {{ width:100%; height:100%; display:block; }}
  #sb-tree .tree-link {{ fill:none; stroke:#CBD5E1; stroke-width:1.4;
    stroke-opacity:0.85; }}
  #sb-tree .tree-node circle {{ fill:#fff; stroke-width:2.5;
    transition: r .15s; }}
  #sb-tree .tree-node:hover circle {{ r: 8; }}
  #sb-tree .tree-node text {{ font-size:11px; font-weight:600;
    fill:#1E293B; }}
  #sb-tree .tree-node.leaf text {{ font-weight:500; fill:#374151; }}
</style>
<div class="sb-wrap">
  <div class="sb-card">
    <div class="sb-info">
      <div>
        <div class="sb-title">KMP Impact · {dep_group}</div>
        <div class="sb-sub">
          <span class="sb-ver">{dep_before} &rarr; {dep_after}</span>
          &nbsp;&middot;&nbsp; {total_files} archivos
        </div>
      </div>
      <div>
        <div class="sb-sec-label">Impacto</div>
        <div class="sb-block sb-block-aff">
          <div class="sb-block-label sb-aff">Afectados</div>
          <div class="sb-stat-row"><span>Directo</span>
            <span class="sb-stat-n" style="color:#B91C1C">
              {direct_count}</span></div>
          <div class="sb-stat-row"><span>Transitivo</span>
            <span class="sb-stat-n" style="color:#1D4ED8">
              {trans_count}</span></div>
          <div class="sb-subtotal" style="color:#B91C1C">
            <span>Total</span><span>{affected}</span></div>
        </div>
        <div class="sb-block sb-block-safe">
          <div class="sb-block-label sb-saf">No afectados</div>
          <div class="sb-stat-row"><span>Expect/Actual pairs</span>
            <span class="sb-stat-n" style="color:#94A3B8">{ea_units}</span></div>
          <div class="sb-subtotal" style="color:#AAA">
            <span>Total</span><span>{none_count}</span></div>
        </div>
      </div>
      <div id="sb-legend-block">
        <div class="sb-sec-label">Escala</div>
        <div class="sb-leg-row">
          <span class="sb-sw" style="background:#B91C1C"></span>Directo</div>
        <div class="sb-leg-row">
          <span class="sb-sw" style="background:#1D4ED8"></span>
          Transitivo dist. 1</div>
        <div class="sb-leg-row">
          <span class="sb-sw" style="background:#60A5FA"></span>
          Transitivo dist. 2+</div>
        <div class="sb-leg-row">
          <span class="sb-sw"
            style="background:#94A3B8;opacity:.5"></span>Sin impacto</div>
        <div class="sb-leg-row">
          <span class="sb-sw"
            style="background:none;border:1.5px dashed #94A3B8"></span>
          Expect/Actual (KMP)</div>
      </div>
      <div>
        <div class="sb-sec-label">Archivos directos</div>
        {direct_rows}
      </div>
      {ea_block}
    </div>
    <div class="sb-chart" id="sb-circle-card">
      <div class="sb-chart-toolbar">
        <div class="sb-tool-group">
          <button id="sb-zoom-out" title="Zoom out">−</button>
          <span class="sb-zoom-badge" id="sb-zoom-pct">100%</span>
          <button id="sb-zoom-in"  title="Zoom in">+</button>
          <button id="sb-zoom-reset" title="Reset view">Reset</button>
          <span class="sb-pad" role="group" aria-label="Pan">
            <button id="sb-pan-left"  title="Pan left">&larr;</button>
            <button id="sb-pan-down"  title="Pan down">&darr;</button>
            <button id="sb-pan-up"    title="Pan up">&uarr;</button>
            <button id="sb-pan-right" title="Pan right">&rarr;</button>
          </span>
        </div>
        <div class="sb-tool-hint">
          <kbd>scroll</kbd> zoom &middot;
          <kbd>drag</kbd> pan &middot;
          <kbd>click</kbd> ring focus
        </div>
      </div>
      <div class="sb-chart-viewport" id="sb-viewport">
        <svg id="sb-sun"></svg>
      </div>
    </div>
  </div>
  <!-- Visual D3 tree below the circle. Mirrors the sunburst card layout
       (toolbar with zoom + d-pad on the right, scoped viewport with the
       SVG inside) so the user gets the same interaction model on both
       visualisations and can pan/zoom only the tree without disturbing
       the page or the circle above. -->
  <div class="sb-tree-section" id="sb-tree-section">
    <div class="sb-tree-head">
      <div>
        <div class="sb-tree-title">Propagation tree</div>
        <div class="sb-tree-sub">Same hierarchy as the sunburst, flattened for reading.</div>
      </div>
      <div class="sb-chart-toolbar sb-tree-toolbar">
        <div class="sb-tool-group">
          <button id="sb-tz-out" title="Zoom out">−</button>
          <span class="sb-zoom-badge" id="sb-tz-pct">100%</span>
          <button id="sb-tz-in"  title="Zoom in">+</button>
          <button id="sb-tz-reset" title="Reset view">Reset</button>
          <span class="sb-pad" role="group" aria-label="Pan">
            <button id="sb-tp-left"  title="Pan left">&larr;</button>
            <button id="sb-tp-down"  title="Pan down">&darr;</button>
            <button id="sb-tp-up"    title="Pan up">&uarr;</button>
            <button id="sb-tp-right" title="Pan right">&rarr;</button>
          </span>
        </div>
        <div class="sb-tool-hint">
          <kbd>scroll</kbd> zoom &middot;
          <kbd>drag</kbd> pan
        </div>
      </div>
    </div>
    <div class="sb-tree-viewport" id="sb-tree-viewport">
      <svg id="sb-tree"></svg>
    </div>
  </div>
  <div id="sb-tt"></div>
</div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
(function() {{
  const DATA = {data_json};
  const W = 640, R = W / 6;
  // Wider font range so labels feel readable inside slices instead of
  // collapsing to tiny lowercase. Adjusted CH_RATIO so wide arcs accept the
  // bigger size without overflowing.
  const MAX_FS = 14.5, MIN_FS = 9.5, CH_RATIO = 0.5;
  // Truncate long file names aggressively so outer-ring labels stay readable
  // inside narrow slices. 14 chars + ellipsis prevents the long rotated
  // strings (e.g. "ExpensesDetailScreen") that the user flagged as visually
  // noisy on the right side of the circle.
  function dispName(d) {{
    const name = d.data.name.replace(/\\.kt$/, "");
    return name.length > 14 ? name.slice(0, 13) + "…" : name;
  }}
  function arcSpan(x0,x1,y0,y1) {{ return (x1-x0)*((y0+y1)/2)*R; }}
  function calcFS(x0,x1,y0,y1,n) {{
    if (!n) return MAX_FS;
    return Math.min(MAX_FS, Math.max(MIN_FS, arcSpan(x0,x1,y0,y1)/(n*CH_RATIO)));
  }}
  function leafColour(d) {{
    const imp = d.data.impact, dist = d.data.distance;
    if (imp === "direct") return "#B91C1C";
    if (imp === "transitive") return dist <= 1 ? "#1D4ED8" : "#60A5FA";
    return "#94A3B8";
  }}
  function folderColour(d) {{
    const leaves = d.descendants().filter(c => !c.children);
    if (leaves.some(c => c.data.impact === "direct")) return "#B91C1C";
    if (leaves.some(c => c.data.impact === "transitive")) {{
      const mn = d3.min(leaves.filter(c => c.data.impact === "transitive"),
                        c => c.data.distance);
      return mn <= 1 ? "#1D4ED8" : "#60A5FA";
    }}
    return "#94A3B8";
  }}
  const colour = d => d.children ? folderColour(d) : leafColour(d);
  function isImp(d) {{
    if (!d.children) {{
      const i = d.data.impact;
      return i === "direct" || i === "transitive";
    }}
    return d.descendants().some(
      c => c.data.impact === "direct" || c.data.impact === "transitive"
    );
  }}
  const opacity = d => isImp(d) ? 1 : 0.28;
  const root = d3.hierarchy(DATA)
    .sum(d => d.value || 0)
    .sort((a, b) => b.value - a.value);
  d3.partition().size([2*Math.PI, root.height + 1])(root);
  const arc = d3.arc()
    .startAngle(d => d.x0).endAngle(d => d.x1)
    .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.004))
    .padRadius(R * 1.5)
    .innerRadius(d => d.y0 * R)
    .outerRadius(d => Math.max(d.y0 * R, d.y1 * R - 1));
  // Responsive sizing — viewBox padding is large enough to fit even the
  // longest outer-ring labels rotated tangentially (the previous 110 px
  // budget still clipped names like "ExpenseScreenUiTest"). 200 px on each
  // side covers ~26 chars at our max font size.
  const PAD = 200;
  const svg = d3.select("#sb-sun")
    .attr("viewBox", [-W/2 - PAD, -W/2 - PAD, W + 2*PAD, W + 2*PAD])
    .attr("preserveAspectRatio", "xMidYMid meet");
  root.each(d => d.current = d);
  // VISIBLE_RINGS is computed in Python from the actual tree depth, so a
  // shallow project (e.g. depth 2) keeps a clean two-ring view, while a
  // deeper project (e.g. depth 5) gets all five rings. Beyond _RING_CEILING
  // (5) the picture collapses to outer-label-only territory.
  const VISIBLE_RINGS = {visible_rings};
  function arcVis(d) {{ return d.y1 <= VISIBLE_RINGS + 1 && d.y0 >= 1 && d.x1 > d.x0; }}
  function lblVis(d) {{
    return d.y1 <= VISIBLE_RINGS + 1 && d.y0 >= 1 && (d.y1-d.y0)*(d.x1-d.x0) > 0.02;
  }}
  function lblTransform(d) {{
    const x = ((d.x0+d.x1)/2)*180/Math.PI, y=(d.y0+d.y1)/2*R;
    return `rotate(${{x-90}}) translate(${{y}},0) rotate(${{x<180?0:180}})`;
  }}
  const path = svg.append("g")
    .selectAll("path")
    .data(root.descendants().slice(1))
    .join("path")
    .attr("fill", d => colour(d))
    .attr("fill-opacity", d => arcVis(d.current) ? opacity(d) : 0)
    .attr("pointer-events", d => arcVis(d.current) ? "auto" : "none")
    .attr("stroke", d => (d.data.is_expect || d.data.is_actual)
      ? "#64748B" : "none")
    .attr("stroke-width", d => (d.data.is_expect || d.data.is_actual)
      ? 1.5 : 0)
    .attr("stroke-dasharray", d => (d.data.is_expect || d.data.is_actual)
      ? "3,2" : "none")
    // Tie the dashed border opacity to arc visibility so the floating dashes
    // don't linger after a zoom hides the underlying arc.
    .attr("stroke-opacity", d => arcVis(d.current) ? 1 : 0)
    .attr("d", d => arc(d.current))
    .style("cursor", d => d.children ? "pointer" : "default")
    .on("click", (ev, p) => {{ if (p.children) zoomTo(p); }});
  const label = svg.append("g")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .style("user-select", "none")
    .selectAll("text")
    .data(root.descendants().slice(1))
    .join("text")
    .attr("dy", "0.35em")
    .attr("fill-opacity", d => +lblVis(d.current))
    .attr("transform", d => lblTransform(d.current))
    .style("font-size", d =>
      `${{calcFS(d.x0,d.x1,d.y0,d.y1,dispName(d).length).toFixed(1)}}px`)
    .style("font-weight", "700")
    .style("paint-order", "stroke")
    .style("stroke-width", "3px")
    .style("stroke-linejoin", "round")
    .style("stroke", d => {{
      const c = colour(d);
      return (c === "#B91C1C" || c === "#1D4ED8") ? "rgba(0,0,0,0.65)"
                                                  : "rgba(255,255,255,0.95)";
    }})
    .style("fill", d => {{
      const c = colour(d);
      return (c === "#B91C1C" || c === "#1D4ED8") ? "#FFF" : "#0F172A";
    }})
    .text(d => dispName(d));
  const cg = svg.append("g").style("cursor", "pointer");
  cg.append("circle").attr("r", R).attr("fill", "#F5F4F0")
    .attr("stroke", "#D8D6D0");
  const clbl = cg.append("text")
    .attr("text-anchor", "middle").attr("dy", "0.35em")
    .style("font-size", "11px").style("font-weight", "600")
    .style("fill", "#64748B").text("src");
  cg.on("click", () => zoomTo(currentFocus.parent || root));
  const tt = document.getElementById("sb-tt");
  path.on("mousemove", (ev, d) => {{
    const imp = d.data.impact, dist = d.data.distance;
    let badge, detail = "";
    if (d.children) {{
      const leaves = d.descendants().filter(c => !c.children);
      const nD = leaves.filter(c => c.data.impact === "direct").length;
      const nT = leaves.filter(c => c.data.impact === "transitive").length;
      const parts = [];
      if (nD) parts.push(`${{nD}} directo${{nD>1?"s":""}}`);
      if (nT) parts.push(`${{nT}} transitivo${{nT>1?"s":""}}`);
      badge = d.data.source_set
        ? `Source set: ${{d.data.name}}` : "Carpeta";
      detail = parts.join(" · ") || "sin impacto";
    }} else {{
      badge =
        imp === "direct" ? "Directo" :
        imp === "transitive" ? `Transitivo — dist. ${{dist}}` :
        imp === "expect_actual" ? "Expect/Actual (KMP)" : "Sin impacto";
      if (d.data.is_expect) badge += " · expect";
      if (d.data.is_actual) badge += " · actual";
      // Always include the source-set so duplicate filenames (CommonModule.kt
      // in commonMain vs androidMain) are disambiguated.
      const ssName = d.parent && d.parent.parent
        ? d.parent.parent.data.name : "";
      detail = (ssName ? `[${{ssName}}] ` : "") + (d.data.path || "");
    }}
    tt.innerHTML =
      `<strong>${{d.data.name}}</strong>` +
      `<span class="sb-sub2">${{badge}}</span>` +
      (detail ? `<br><span class="sb-sub2">${{detail}}</span>` : "");
    tt.style.display = "block";
    tt.style.left = ev.clientX + 14 + "px";
    tt.style.top = ev.clientY - 10 + "px";
  }}).on("mouseleave", () => tt.style.display = "none");
  let currentFocus = root;
  function zoomTo(focus) {{
    currentFocus = focus;
    root.each(d => d.target = {{
      x0: Math.max(0, Math.min(1,
        (d.x0-focus.x0)/(focus.x1-focus.x0))) * 2 * Math.PI,
      x1: Math.max(0, Math.min(1,
        (d.x1-focus.x0)/(focus.x1-focus.x0))) * 2 * Math.PI,
      y0: Math.max(0, d.y0 - focus.depth),
      y1: Math.max(0, d.y1 - focus.depth),
    }});
    const tr = svg.transition().duration(480);
    path.transition(tr)
      .tween("data", d => {{
        const i = d3.interpolate(d.current, d.target);
        return t => d.current = i(t);
      }})
      .filter(function(d) {{
        return +this.getAttribute("fill-opacity") || arcVis(d.target);
      }})
      .attr("fill-opacity", d => arcVis(d.target) ? opacity(d) : 0)
      .attr("stroke-opacity", d => arcVis(d.target) ? 1 : 0)
      .attr("pointer-events", d => arcVis(d.target) ? "auto" : "none")
      .attrTween("d", d => () => arc(d.current));
    label
      .filter(function(d) {{
        return +this.getAttribute("fill-opacity") || lblVis(d.target);
      }})
      .transition(tr)
      .attr("fill-opacity", d => +lblVis(d.target))
      .attrTween("transform", d => () => lblTransform(d.current))
      .on("end", function(d) {{
        const pos = d.target || d.current;
        const n = dispName(d);
        d3.select(this).text(n).style("font-size",
          `${{calcFS(pos.x0,pos.x1,pos.y0,pos.y1,n.length).toFixed(1)}}px`);
      }});
    clbl.text(focus.data.name);
  }}

  // ── Visual wheel-zoom + drag-pan inside the sticky chart viewport ───
  // Direct viewBox manipulation gives reliable pan/zoom for arbitrary
  // SVG content without fighting d3.zoom's event filter (the arcs cover
  // the whole canvas, which broke the previous d3.zoom-based attempt
  // because every mousedown landed on a <path> and was rejected). The
  // semantic click-to-zoom (animating the partition layout) still
  // works because we never call preventDefault on plain clicks; only
  // when a drag actually moved more than a few pixels we suppress the
  // synthetic click so a pan doesn't trigger an unintended zoomTo().
  const svgEl = document.getElementById("sb-sun");
  const viewportEl = document.getElementById("sb-viewport");
  const VB0 = {{ x: -W/2 - PAD, y: -W/2 - PAD, w: W + 2*PAD, h: W + 2*PAD }};
  let vb = Object.assign({{}}, VB0);
  const zoomPctEl  = document.getElementById("sb-zoom-pct");
  const zoomInBtn  = document.getElementById("sb-zoom-in");
  const zoomOutBtn = document.getElementById("sb-zoom-out");
  const zoomRstBtn = document.getElementById("sb-zoom-reset");
  const MIN_W = (W + 2*PAD) / 8;  // max zoom ~8x
  const MAX_W = (W + 2*PAD) * 3;  // max zoom out 3x
  function applyVB() {{
    svgEl.setAttribute(
      "viewBox",
      `${{vb.x.toFixed(2)}} ${{vb.y.toFixed(2)}} ${{vb.w.toFixed(2)}} ${{vb.h.toFixed(2)}}`
    );
    if (zoomPctEl) {{
      const pct = Math.round((VB0.w / vb.w) * 100);
      zoomPctEl.textContent = pct + "%";
      if (zoomOutBtn) zoomOutBtn.disabled = vb.w >= MAX_W - 1;
      if (zoomInBtn)  zoomInBtn.disabled  = vb.w <= MIN_W + 1;
    }}
  }}
  function zoomByFactor(factor, cx, cy) {{
    const newW = Math.max(MIN_W, Math.min(MAX_W, vb.w * factor));
    const ratio = newW / vb.w;
    vb.x = vb.x + cx * vb.w * (1 - ratio);
    vb.y = vb.y + cy * vb.h * (1 - ratio);
    vb.w = newW;
    vb.h = vb.h * ratio;
    applyVB();
  }}
  if (zoomInBtn)  zoomInBtn.addEventListener("click", () => zoomByFactor(1/1.3, 0.5, 0.5));
  if (zoomOutBtn) zoomOutBtn.addEventListener("click", () => zoomByFactor(1.3, 0.5, 0.5));
  if (zoomRstBtn) zoomRstBtn.addEventListener("click", () => {{
    vb = Object.assign({{}}, VB0); applyVB();
  }});
  // ── D-pad pan buttons. Each click nudges the viewBox by ~12% of its
  //    current size, so the relative step stays sensible at every zoom
  //    level (large at 100%, smaller after zooming in).
  function panBy(dx, dy) {{
    vb.x += dx * vb.w; vb.y += dy * vb.h; applyVB();
  }}
  const PAN_STEP = 0.12;
  const panLeftBtn  = document.getElementById("sb-pan-left");
  const panRightBtn = document.getElementById("sb-pan-right");
  const panUpBtn    = document.getElementById("sb-pan-up");
  const panDownBtn  = document.getElementById("sb-pan-down");
  if (panLeftBtn)  panLeftBtn.addEventListener("click",  () => panBy(-PAN_STEP, 0));
  if (panRightBtn) panRightBtn.addEventListener("click", () => panBy( PAN_STEP, 0));
  if (panUpBtn)    panUpBtn.addEventListener("click",    () => panBy(0, -PAN_STEP));
  if (panDownBtn)  panDownBtn.addEventListener("click",  () => panBy(0,  PAN_STEP));
  viewportEl.addEventListener("wheel", function (e) {{
    e.preventDefault();
    const r = viewportEl.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width;
    const py = (e.clientY - r.top) / r.height;
    zoomByFactor(e.deltaY < 0 ? 1/1.15 : 1.15, px, py);
  }}, {{ passive: false }});
  // Initial render so the badge shows 100% even before any interaction.
  applyVB();

  let dragging = false, last = null, downXY = null, didDrag = false;
  viewportEl.addEventListener("pointerdown", function (e) {{
    if (e.button !== 0) return;
    dragging = true;
    didDrag = false;
    last = {{ x: e.clientX, y: e.clientY }};
    downXY = {{ x: e.clientX, y: e.clientY }};
    try {{ viewportEl.setPointerCapture(e.pointerId); }} catch (_) {{}}
  }});
  viewportEl.addEventListener("pointermove", function (e) {{
    if (!dragging) return;
    const dx = e.clientX - downXY.x, dy = e.clientY - downXY.y;
    if (!didDrag && Math.hypot(dx, dy) > 4) didDrag = true;
    if (!didDrag) return;
    const r = viewportEl.getBoundingClientRect();
    vb.x -= (e.clientX - last.x) / r.width  * vb.w;
    vb.y -= (e.clientY - last.y) / r.height * vb.h;
    last = {{ x: e.clientX, y: e.clientY }};
    applyVB();
  }});
  function endDrag(e) {{
    dragging = false;
    try {{ viewportEl.releasePointerCapture(e.pointerId); }} catch (_) {{}}
  }}
  viewportEl.addEventListener("pointerup", endDrag);
  viewportEl.addEventListener("pointercancel", endDrag);
  viewportEl.addEventListener("pointerleave", endDrag);

  // Block the synthetic click that follows a pan so it doesn't trigger
  // the arc's semantic zoom. Capture phase so it runs before D3's
  // bubble-phase click handler on the arcs.
  viewportEl.addEventListener("click", function (e) {{
    if (didDrag) {{
      e.stopPropagation();
      e.preventDefault();
      didDrag = false;
    }}
  }}, true);

  viewportEl.addEventListener("dblclick", function (e) {{
    // Double-click on empty space (or modifier-double-click anywhere)
    // resets the viewBox; clicks on arcs/labels keep their meaning.
    const onArc = e.target && (e.target.tagName === "path" || e.target.tagName === "text");
    if (onArc && !e.shiftKey) return;
    vb = Object.assign({{}}, VB0);
    applyVB();
  }});

  // ── Visual D3 tree under the sunburst circle ─────────────────────────
  // Same hierarchy data, rendered as a horizontal indented tree. We prune
  // the data tree to keep only nodes that touch impacted files, otherwise
  // the tree fills with grey leaves that distract from the main story.
  function pruneToImpacted(node) {{
    if (!node.children) {{
      const i = node.impact;
      return (i === "direct" || i === "transitive" ||
              node.is_expect || node.is_actual) ? node : null;
    }}
    const kids = (node.children || [])
      .map(pruneToImpacted)
      .filter(Boolean);
    if (kids.length === 0) return null;
    return Object.assign({{}}, node, {{ children: kids }});
  }}
  const treeData = pruneToImpacted(JSON.parse(JSON.stringify(DATA)))
    || {{ name: "src", children: [] }};
  const treeRoot = d3.hierarchy(treeData);

  const NODE_DX = 22;        // vertical step between nodes
  const NODE_DY = 200;       // horizontal step between depth levels
  const tree = d3.tree().nodeSize([NODE_DX, NODE_DY]);
  tree(treeRoot);

  let xMin = Infinity, xMax = -Infinity;
  treeRoot.each(d => {{
    if (d.x < xMin) xMin = d.x;
    if (d.x > xMax) xMax = d.x;
  }});
  const treeWidth = (treeRoot.height + 1) * NODE_DY + 240;
  const treeHeight = (xMax - xMin) + NODE_DX * 2;

  // Initial viewBox covers the whole tree. We keep this constant so the
  // Reset button has a stable target, regardless of how much the user
  // panned/zoomed during the session.
  const TREE_VB0 = {{
    x: -100, y: xMin - NODE_DX,
    w: treeWidth, h: treeHeight,
  }};
  let tvb = Object.assign({{}}, TREE_VB0);

  const treeSvg = d3.select("#sb-tree")
    .attr("preserveAspectRatio", "xMidYMid meet");

  treeSvg.selectAll("*").remove();
  const treeG = treeSvg.append("g");

  treeG.append("g")
    .selectAll("path.tree-link")
    .data(treeRoot.links())
    .join("path")
      .attr("class", "tree-link")
      .attr("d", d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x));

  function nodeColour(d) {{
    return colour(d);
  }}

  const treeNodes = treeG.append("g")
    .selectAll("g.tree-node")
    .data(treeRoot.descendants())
    .join("g")
      .attr("class", d => "tree-node" + (d.children ? "" : " leaf"))
      .attr("transform", d => `translate(${{d.y}}, ${{d.x}})`);

  treeNodes.append("circle")
    .attr("r", d => d.depth === 0 ? 6 : (d.children ? 5 : 4))
    .attr("fill", d => d.children ? "#fff" : nodeColour(d))
    .attr("stroke", d => nodeColour(d));

  treeNodes.append("text")
    .attr("dy", "0.32em")
    .attr("x", d => d.children ? -10 : 10)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => {{
      const n = (d.data.name || "").replace(/\\.kt$/, "");
      return n.length > 26 ? n.slice(0, 24) + "…" : n;
    }})
    .clone(true).lower()
    .attr("stroke", "#F5F4F0").attr("stroke-width", 4);

  // ── Tree viewport: same wheel-zoom / drag-pan / d-pad model as the
  //    circle above, so the user moves through the tree without
  //    scrolling the page. We bind directly on the viewport so the
  //    interaction is fully scoped — the rest of the report stays put.
  const treeSvgEl = document.getElementById("sb-tree");
  const treeViewportEl = document.getElementById("sb-tree-viewport");
  const treeZoomPctEl = document.getElementById("sb-tz-pct");
  const treeZoomInBtn  = document.getElementById("sb-tz-in");
  const treeZoomOutBtn = document.getElementById("sb-tz-out");
  const treeZoomRstBtn = document.getElementById("sb-tz-reset");
  const treePadL = document.getElementById("sb-tp-left");
  const treePadR = document.getElementById("sb-tp-right");
  const treePadU = document.getElementById("sb-tp-up");
  const treePadD = document.getElementById("sb-tp-down");
  const TMIN_W = TREE_VB0.w / 8;
  const TMAX_W = TREE_VB0.w * 3;

  function applyTreeVB() {{
    treeSvgEl.setAttribute(
      "viewBox",
      `${{tvb.x.toFixed(2)}} ${{tvb.y.toFixed(2)}} ${{tvb.w.toFixed(2)}} ${{tvb.h.toFixed(2)}}`
    );
    if (treeZoomPctEl) {{
      const pct = Math.round((TREE_VB0.w / tvb.w) * 100);
      treeZoomPctEl.textContent = pct + "%";
      if (treeZoomOutBtn) treeZoomOutBtn.disabled = tvb.w >= TMAX_W - 1;
      if (treeZoomInBtn)  treeZoomInBtn.disabled  = tvb.w <= TMIN_W + 1;
    }}
  }}
  function treeZoomBy(factor, cx, cy) {{
    const newW = Math.max(TMIN_W, Math.min(TMAX_W, tvb.w * factor));
    const ratio = newW / tvb.w;
    tvb.x = tvb.x + cx * tvb.w * (1 - ratio);
    tvb.y = tvb.y + cy * tvb.h * (1 - ratio);
    tvb.w = newW;
    tvb.h = tvb.h * ratio;
    applyTreeVB();
  }}
  function treePanBy(dx, dy) {{
    tvb.x += dx * tvb.w; tvb.y += dy * tvb.h; applyTreeVB();
  }}
  applyTreeVB();

  if (treeZoomInBtn)  treeZoomInBtn.addEventListener("click",  () => treeZoomBy(1/1.3, 0.5, 0.5));
  if (treeZoomOutBtn) treeZoomOutBtn.addEventListener("click", () => treeZoomBy(1.3,  0.5, 0.5));
  if (treeZoomRstBtn) treeZoomRstBtn.addEventListener("click", () => {{
    tvb = Object.assign({{}}, TREE_VB0); applyTreeVB();
  }});
  if (treePadL) treePadL.addEventListener("click", () => treePanBy(-PAN_STEP, 0));
  if (treePadR) treePadR.addEventListener("click", () => treePanBy( PAN_STEP, 0));
  if (treePadU) treePadU.addEventListener("click", () => treePanBy(0, -PAN_STEP));
  if (treePadD) treePadD.addEventListener("click", () => treePanBy(0,  PAN_STEP));

  treeViewportEl.addEventListener("wheel", function (e) {{
    e.preventDefault();
    const r = treeViewportEl.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width;
    const py = (e.clientY - r.top) / r.height;
    treeZoomBy(e.deltaY < 0 ? 1/1.15 : 1.15, px, py);
  }}, {{ passive: false }});

  let tDrag = false, tLast = null, tDown = null, tMoved = false;
  treeViewportEl.addEventListener("pointerdown", function (e) {{
    if (e.button !== 0) return;
    tDrag = true; tMoved = false;
    tLast = {{ x: e.clientX, y: e.clientY }};
    tDown = {{ x: e.clientX, y: e.clientY }};
    try {{ treeViewportEl.setPointerCapture(e.pointerId); }} catch (_) {{}}
  }});
  treeViewportEl.addEventListener("pointermove", function (e) {{
    if (!tDrag) return;
    const dx = e.clientX - tDown.x, dy = e.clientY - tDown.y;
    if (!tMoved && Math.hypot(dx, dy) > 4) tMoved = true;
    if (!tMoved) return;
    const r = treeViewportEl.getBoundingClientRect();
    tvb.x -= (e.clientX - tLast.x) / r.width  * tvb.w;
    tvb.y -= (e.clientY - tLast.y) / r.height * tvb.h;
    tLast = {{ x: e.clientX, y: e.clientY }};
    applyTreeVB();
  }});
  function endTreeDrag(e) {{
    tDrag = false;
    try {{ treeViewportEl.releasePointerCapture(e.pointerId); }} catch (_) {{}}
  }}
  treeViewportEl.addEventListener("pointerup", endTreeDrag);
  treeViewportEl.addEventListener("pointercancel", endTreeDrag);
  treeViewportEl.addEventListener("pointerleave", endTreeDrag);
  treeViewportEl.addEventListener("dblclick", function () {{
    tvb = Object.assign({{}}, TREE_VB0); applyTreeVB();
  }});
}})();
</script>
"""


def build_sunburst_svg_standalone(
    consolidated: ConsolidatedResult,
) -> str:
    """Hierarchical Sunburst SVG (no JS), mirroring the HTML report's D3
    layout: src → source-set → package → file. Drawn with concentric arc
    slices so cairosvg can rasterise it without a browser runtime."""
    tree = _build_tree(consolidated)
    return _render_hierarchical_sunburst(tree, consolidated)


def build_sunburst_svg_legacy(
    consolidated: ConsolidatedResult,
) -> str:
    """Old 2-ring donut kept for debugging. Not wired into the workflow."""
    tree = _build_tree(consolidated)
    sets = []
    for ss_node in tree["children"]:
        leaves = _flatten_leaves(ss_node)
        if not leaves:
            continue
        direct = sum(1 for l in leaves if l["impact"] == "direct")
        trans = sum(1 for l in leaves if l["impact"] == "transitive")
        ea = sum(1 for l in leaves if l["impact"] == "expect_actual")
        none = len(leaves) - direct - trans - ea
        sets.append({
            "name": ss_node["name"],
            "direct": direct, "trans": trans, "ea": ea, "none": none,
            "total": len(leaves),
        })
    return _render_static_sunburst(sets, consolidated)


def _flatten_leaves(node: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    stack = [node]
    while stack:
        n = stack.pop()
        if "children" in n and n["children"]:
            stack.extend(n["children"])
        elif "impact" in n:
            out.append(n)
    return out


def _render_static_sunburst(
    sets: list[dict[str, Any]],
    consolidated: ConsolidatedResult,
) -> str:
    """Simple concentric donut: inner ring = source sets, outer ring = impact
    breakdown. Pure SVG, no scripts, ready for cairosvg."""
    W = 520
    CX = CY = W // 2
    INNER_R = 90
    MID_R = 140
    OUTER_R = 200
    import math

    total_files = sum(s["total"] for s in sets) or 1
    title = html.escape(consolidated.dependency_group)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W+60}" '
        f'width="{W}" height="{W+60}" '
        'font-family="system-ui,sans-serif">',
        '<style>.lbl{font-size:12px;fill:#1e293b;font-weight:600}'
        '.cap{font-size:14px;fill:#1e293b;font-weight:700}'
        '.sub{font-size:11px;fill:#64748b}</style>',
        f'<text x="{CX}" y="26" text-anchor="middle" class="cap">'
        f'Impact Sunburst · {title}</text>',
        f'<text x="{CX}" y="44" text-anchor="middle" class="sub">'
        f'{consolidated.version_before} -&gt; {consolidated.version_after}'
        f' &#183; {total_files} archivos</text>',
    ]

    # Inner ring = source-sets
    ss_colors = {
        "commonMain": "#312e81", "androidMain": "#0f766e",
        "iosMain": "#9d174d", "commonTest": "#6b7280",
    }
    ang0 = -math.pi / 2
    for s in sets:
        frac = s["total"] / total_files
        ang1 = ang0 + frac * 2 * math.pi
        path = _ring_segment(
            CX, CY + 30, INNER_R, MID_R - 5, ang0, ang1
        )
        color = ss_colors.get(s["name"], "#475569")
        parts.append(f'<path d="{path}" fill="{color}" opacity="0.85"/>')
        # mid-angle label
        mid = (ang0 + ang1) / 2
        lbl_r = (INNER_R + MID_R) / 2 - 2
        lx = CX + math.cos(mid) * lbl_r
        ly = CY + 30 + math.sin(mid) * lbl_r
        if frac > 0.08:
            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" '
                f'class="lbl" fill="#fff">{html.escape(s["name"])}</text>'
            )
        ang0 = ang1

    # Outer ring = impact segments within each source-set
    impact_colors = {
        "direct": "#B91C1C", "trans": "#1D4ED8",
        "ea": "#94A3B8", "none": "#e5e7eb",
    }
    ang0 = -math.pi / 2
    for s in sets:
        ss_frac = s["total"] / total_files
        ss_ang1 = ang0 + ss_frac * 2 * math.pi
        sub_total = s["total"] or 1
        sub_ang = ang0
        for key in ("direct", "trans", "ea", "none"):
            count = s[key]
            if not count:
                continue
            portion = count / sub_total
            sub_next = sub_ang + portion * (ss_ang1 - ang0)
            path = _ring_segment(
                CX, CY + 30, MID_R, OUTER_R, sub_ang, sub_next
            )
            parts.append(
                f'<path d="{path}" fill="{impact_colors[key]}" '
                f'opacity="0.9"/>'
            )
            sub_ang = sub_next
        ang0 = ss_ang1

    # Legend
    legend_y = W + 40
    parts.append(
        f'<g transform="translate(20,{legend_y})">'
        '<rect width="14" height="14" fill="#B91C1C"/>'
        '<text x="20" y="11" class="sub">Directo</text>'
        '<rect x="90" width="14" height="14" fill="#1D4ED8"/>'
        '<text x="110" y="11" class="sub">Transitivo</text>'
        '<rect x="200" width="14" height="14" fill="#94A3B8"/>'
        '<text x="220" y="11" class="sub">Expect/Actual</text>'
        '<rect x="330" width="14" height="14" fill="#e5e7eb" '
        'stroke="#cbd5e1"/>'
        '<text x="350" y="11" class="sub">Sin impacto</text>'
        '</g>'
    )

    parts.append('</svg>')
    return "\n".join(parts)


def _render_hierarchical_sunburst(
    tree: dict[str, Any],
    consolidated: ConsolidatedResult,
) -> str:
    """Replicates the D3 partition layout used by the HTML report in pure SVG.

    Each node gets (x0, x1) angular extent and (y0, y1) radial depth. Leaf
    values bubble up via sum; children are sorted by value descending. Colours
    match the interactive view:
      direct        → #B91C1C
      transitive d1 → #1D4ED8
      transitive d2+→ #60A5FA
      none          → #94A3B8
      expect/actual → dashed stroke #64748B
    Non-impacted arcs are dimmed to 0.28 opacity.
    """
    import math

    # ── 1. compute .value for each node (sum of leaves) ─────────────────────
    def _sum_value(node: dict[str, Any]) -> float:
        if node.get("children"):
            total = 0.0
            for c in node["children"]:
                total += _sum_value(c)
            node["_v"] = total
            return total
        v = float(node.get("value", 1))
        node["_v"] = v
        return v

    _sum_value(tree)

    # sort children by value descending (same as the D3 view)
    def _sort(node: dict[str, Any]) -> None:
        if node.get("children"):
            node["children"].sort(key=lambda c: -c["_v"])
            for c in node["children"]:
                _sort(c)

    _sort(tree)

    # ── 2. partition: assign (x0, x1, depth) ────────────────────────────────
    def _partition(node: dict[str, Any], x0: float, x1: float, depth: int) -> None:
        node["x0"] = x0
        node["x1"] = x1
        node["depth"] = depth
        if node.get("children"):
            total = sum(c["_v"] for c in node["children"]) or 1.0
            acc = x0
            for c in node["children"]:
                frac = c["_v"] / total
                nx1 = acc + frac * (x1 - x0)
                _partition(c, acc, nx1, depth + 1)
                acc = nx1

    _partition(tree, 0.0, 2.0 * math.pi, 0)

    # ── 3. flatten ──────────────────────────────────────────────────────────
    def _max_depth(node: dict[str, Any]) -> int:
        if not node.get("children"):
            return node["depth"]
        return max(_max_depth(c) for c in node["children"])

    max_depth = _max_depth(tree)

    def _walk(node: dict[str, Any], out: list) -> None:
        out.append(node)
        for c in node.get("children", []) or []:
            _walk(c, out)

    flat: list[dict[str, Any]] = []
    _walk(tree, flat)

    # ── 4. impact metadata per node ─────────────────────────────────────────
    def _is_impacted(node: dict[str, Any]) -> bool:
        if not node.get("children"):
            return node.get("impact") in ("direct", "transitive")
        return any(_is_impacted(c) for c in node["children"])

    def _node_colour(node: dict[str, Any]) -> str:
        # Leaf
        if not node.get("children"):
            imp = node.get("impact")
            if imp == "direct":
                return "#B91C1C"
            if imp == "transitive":
                return "#1D4ED8" if int(node.get("distance", 9)) <= 1 else "#60A5FA"
            return "#94A3B8"
        # Folder / source set → match its worst-case leaf
        leaves: list[dict[str, Any]] = []
        _walk(node, leaves)
        leaves = [l for l in leaves if not l.get("children")]
        if any(l.get("impact") == "direct" for l in leaves):
            return "#B91C1C"
        trans = [l for l in leaves if l.get("impact") == "transitive"]
        if trans:
            best = min(int(l.get("distance", 9)) for l in trans)
            return "#1D4ED8" if best <= 1 else "#60A5FA"
        return "#94A3B8"

    def _has_expect_actual(node: dict[str, Any]) -> bool:
        if not node.get("children"):
            return bool(node.get("is_expect") or node.get("is_actual"))
        return False  # only leaves get the dashed stroke

    # ── 5. emit SVG ─────────────────────────────────────────────────────────
    # Layout adapts to the actual tree depth. A shallow project shows fewer,
    # thicker rings; a deep one shows up to ``_RING_CEILING`` thinner rings.
    # Files past the ceiling fall through to outer tangential labels (5.b
    # below).
    visible_rings = _visible_ring_count(tree)
    R_INNER_ROOT = 70
    # Keep a roughly constant total radius so the picture doesn't shrink for
    # shallow projects nor explode for deep ones. 160 px of total ring
    # thickness divided across the visible rings.
    TOTAL_RING_R = 160
    ring_thickness = TOTAL_RING_R // visible_rings
    MAX_R = R_INNER_ROOT + visible_rings * ring_thickness
    OUTER_MARGIN = 130          # room for tangential file-name labels
    TITLE_H = 70
    LEGEND_H = 50
    W = 2 * (MAX_R + OUTER_MARGIN) + 40
    H_ring = 2 * (MAX_R + OUTER_MARGIN) + 40
    H = TITLE_H + H_ring + LEGEND_H
    CX = W / 2
    CY = TITLE_H + H_ring / 2

    def _radius(depth: int) -> float:
        return R_INNER_ROOT + max(0, depth) * ring_thickness

    dep_group = html.escape(consolidated.dependency_group)
    before = html.escape(consolidated.version_before)
    after = html.escape(consolidated.version_after)
    total_files = consolidated.static_impact.total_project_files or len(
        consolidated.trace
    )

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" '
        'font-family="system-ui,sans-serif">',
        '<rect width="100%" height="100%" fill="#F5F4F0"/>',
        f'<text x="{CX}" y="30" text-anchor="middle" fill="#1E293B" '
        f'font-size="18" font-weight="700">KMP Impact . {dep_group}</text>',
        f'<text x="{CX}" y="52" text-anchor="middle" fill="#64748b" '
        f'font-size="12">{before} -&gt; {after} . {total_files} archivos</text>',
    ]

    # 5.a arcs — clamp to ``visible_rings`` so we mirror the D3 view's
    # ``arcVis(d) { y1 <= VISIBLE_RINGS + 1; }``. Files past that depth
    # surface as tangential outer labels instead (block 5.b below).
    for node in flat:
        d = node["depth"]
        if d == 0:
            continue
        if d > visible_rings:
            continue
        x0, x1 = node["x0"], node["x1"]
        if x1 - x0 < 1e-4:
            continue
        r_in = _radius(d - 1)
        r_out = _radius(d) - 2
        colour = _node_colour(node)
        opacity = "1" if _is_impacted(node) else "0.28"

        large_arc = 1 if (x1 - x0) > math.pi else 0
        # D3 orientation: angle 0 = top, clockwise. Python math uses angle 0 = right, ccw.
        # Convert: svg_angle = x - π/2.
        a0 = x0 - math.pi / 2
        a1 = x1 - math.pi / 2
        x0o = CX + r_out * math.cos(a0)
        y0o = CY + r_out * math.sin(a0)
        x1o = CX + r_out * math.cos(a1)
        y1o = CY + r_out * math.sin(a1)
        x0i = CX + r_in * math.cos(a0)
        y0i = CY + r_in * math.sin(a0)
        x1i = CX + r_in * math.cos(a1)
        y1i = CY + r_in * math.sin(a1)

        path = (
            f"M {x0o:.2f} {y0o:.2f} "
            f"A {r_out:.2f} {r_out:.2f} 0 {large_arc} 1 {x1o:.2f} {y1o:.2f} "
            f"L {x1i:.2f} {y1i:.2f} "
            f"A {r_in:.2f} {r_in:.2f} 0 {large_arc} 0 {x0i:.2f} {y0i:.2f} Z"
        )
        stroke_attrs = ""
        if _has_expect_actual(node):
            stroke_attrs = ' stroke="#64748B" stroke-width="1.5" stroke-dasharray="3,2"'
        parts.append(
            f'<path d="{path}" fill="{colour}" fill-opacity="{opacity}"'
            f'{stroke_attrs}/>'
        )

    # 5.b labels — two paths so the picture matches the D3 viewer:
    #  - depth 1..visible_rings: label inside the arc (white on red/blue,
    #    slate otherwise).
    #  - leaf files past the visible ring count: the file name appears as a
    #    tangential label outside the outer ring, coloured by relation.
    OUTER_LABEL_R = _radius(visible_rings) + 14
    for node in flat:
        d = node["depth"]
        if d == 0:
            continue
        x0, x1 = node["x0"], node["x1"]
        span = x1 - x0
        if span < 0.04:
            continue
        mid = (x0 + x1) / 2
        a_mid = mid - math.pi / 2  # convert to SVG (top = -π/2)

        if d <= visible_rings:
            if span < 0.18:
                continue
            r_in = _radius(d - 1)
            r_out = _radius(d) - 2
            r_label = (r_in + r_out) / 2
            lx = CX + r_label * math.cos(a_mid)
            ly = CY + r_label * math.sin(a_mid)
            raw_name = str(node.get("name", ""))
            label = raw_name.replace(".kt", "")
            max_chars = int(span * (r_label / 12))
            if len(label) > max(max_chars, 4):
                label = label[: max(max_chars, 4) - 1] + "."
            colour = _node_colour(node)
            fill = "#FFFFFF" if colour in ("#B91C1C", "#1D4ED8") else "#1E293B"
            angle_deg = (mid * 180 / math.pi) - 90
            rotate = angle_deg + (180 if (mid > math.pi) else 0)
            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" '
                f'dominant-baseline="middle" '
                f'transform="rotate({rotate:.1f} {lx:.1f} {ly:.1f})" '
                f'font-size="11" font-weight="700" fill="{fill}">'
                f'{html.escape(label)}</text>'
            )
        elif not node.get("children"):
            raw = str(node.get("name", "")).replace(".kt", "")
            if not raw:
                continue
            label = raw if len(raw) <= 18 else raw[:17] + "."
            colour = _node_colour(node)
            angle_deg = (mid * 180 / math.pi) - 90
            on_left = mid > math.pi
            anchor = "end" if on_left else "start"
            rotate = angle_deg + (180 if on_left else 0)
            lx = CX + OUTER_LABEL_R * math.cos(a_mid)
            ly = CY + OUTER_LABEL_R * math.sin(a_mid)
            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
                f'dominant-baseline="middle" '
                f'transform="rotate({rotate:.1f} {lx:.1f} {ly:.1f})" '
                f'font-size="10" font-weight="600" fill="{colour}" '
                f'opacity="0.85">{html.escape(label)}</text>'
            )

    # 5.c central circle + "src" label
    parts.append(
        f'<circle cx="{CX}" cy="{CY}" r="{R_INNER_ROOT}" '
        f'fill="#F5F4F0" stroke="#D8D6D0"/>'
        f'<text x="{CX}" y="{CY + 4}" text-anchor="middle" '
        f'font-size="13" font-weight="700" fill="#64748B">src</text>'
    )

    # 5.d legend (pinned to the bottom of the viewport)
    lg_y = H - 30
    items = [
        ("#B91C1C", "Directo"),
        ("#1D4ED8", "Transitivo d1"),
        ("#60A5FA", "Transitivo d2+"),
        ("#94A3B8", "Sin impacto"),
    ]
    step = (W - 40) / 5
    x_cursor = 20
    for colour, txt in items:
        parts.append(
            f'<rect x="{x_cursor:.0f}" y="{lg_y}" width="14" height="14" '
            f'rx="3" fill="{colour}"/>'
            f'<text x="{x_cursor + 20:.0f}" y="{lg_y + 11}" fill="#475569" '
            f'font-size="11">{txt}</text>'
        )
        x_cursor += step
    parts.append(
        f'<rect x="{x_cursor:.0f}" y="{lg_y}" width="14" height="14" '
        f'rx="3" fill="none" stroke="#64748B" stroke-width="1.5" '
        f'stroke-dasharray="3,2"/>'
        f'<text x="{x_cursor + 20:.0f}" y="{lg_y + 11}" fill="#475569" '
        f'font-size="11">Expect/Actual</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def _ring_segment(cx: float, cy: float, r_in: float, r_out: float,
                  a0: float, a1: float) -> str:
    """SVG path for an annular sector."""
    import math
    large = 1 if (a1 - a0) > math.pi else 0
    x0i, y0i = cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)
    x1i, y1i = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
    x0o, y0o = cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)
    x1o, y1o = cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)
    return (
        f"M {x0i:.2f} {y0i:.2f} "
        f"L {x0o:.2f} {y0o:.2f} "
        f"A {r_out:.2f} {r_out:.2f} 0 {large} 1 {x1o:.2f} {y1o:.2f} "
        f"L {x1i:.2f} {y1i:.2f} "
        f"A {r_in:.2f} {r_in:.2f} 0 {large} 0 {x0i:.2f} {y0i:.2f} Z"
    )


# ---------------------------------------------------------------------------
# Standalone Legend + Tree (rendered server-side so the PR comment images
# stay deterministic — no browser, no D3 runtime needed).
# ---------------------------------------------------------------------------

def build_legend_svg(consolidated: ConsolidatedResult) -> str:
    """Static SVG of the Escala / Scale block. Mirrors the colours and rows
    of the live legend on the report's sunburst tab."""
    direct = sum(
        1 for f in consolidated.static_impact.impacted_files
        if f.relation == ImpactRelation.DIRECT
    )
    trans = sum(
        1 for f in consolidated.static_impact.impacted_files
        if f.relation == ImpactRelation.TRANSITIVE
    )
    ea_pairs = len(consolidated.static_impact.expect_actual_pairs)
    rows = [
        ("Directo", "#B91C1C", str(direct), False),
        ("Transitivo dist. 1", "#1D4ED8", "—", False),
        ("Transitivo dist. 2+", "#60A5FA", "—", False),
        ("Sin impacto", "#94A3B8", "—", False),
        ("Expect/Actual (KMP)", "#94A3B8", str(ea_pairs), True),  # dashed border
    ]
    # Use a slightly larger row height + side padding so the block looks
    # like a polished card rather than a thin strip.
    W, ROW_H, PAD_X, PAD_Y, TITLE_H = 360, 36, 24, 24, 26
    H = PAD_Y + TITLE_H + ROW_H * len(rows) + PAD_Y
    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="system-ui,sans-serif">'
        f'<rect width="100%" height="100%" fill="#F5F4F0" '
        f'stroke="#D8D6D0" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{PAD_X}" y="{PAD_Y + 14}" font-size="11" font-weight="700" '
        f'letter-spacing="2" fill="#777">ESCALA</text>'
        f'<line x1="{PAD_X}" y1="{PAD_Y + 22}" x2="{W - PAD_X}" '
        f'y2="{PAD_Y + 22}" stroke="#D8D6D0" stroke-width="1"/>'
    )
    y = PAD_Y + TITLE_H + 8
    for label, colour, count, dashed in rows:
        sw_x = PAD_X + 4
        sw_y = y + 6
        if dashed:
            parts.append(
                f'<rect x="{sw_x}" y="{sw_y}" width="20" height="20" rx="3" '
                f'fill="none" stroke="#94A3B8" stroke-width="1.6" '
                f'stroke-dasharray="4 3"/>'
            )
        else:
            parts.append(
                f'<rect x="{sw_x}" y="{sw_y}" width="20" height="20" rx="3" '
                f'fill="{colour}"/>'
            )
        parts.append(
            f'<text x="{sw_x + 32}" y="{sw_y + 14}" font-size="13" '
            f'fill="#1F2937">{html.escape(label)}</text>'
        )
        if count != "—":
            parts.append(
                f'<text x="{W - PAD_X}" y="{sw_y + 14}" text-anchor="end" '
                f'font-size="13" font-weight="700" fill="#374151">'
                f'{html.escape(count)}</text>'
            )
        y += ROW_H
    parts.append("</svg>")
    return "\n".join(parts)


def _classify_node(node: dict[str, Any]) -> str:
    if not node.get("children"):
        imp = node.get("impact", "")
        if imp == "direct":
            return "direct"
        if imp == "transitive":
            return "transitive_d1" if node.get("distance", 99) <= 1 else "transitive_d2"
        if imp == "expect_actual" or node.get("is_expect") or node.get("is_actual"):
            return "expect_actual"
        return "none"
    descendants_class = "none"
    for child in node["children"]:
        c = _classify_node(child)
        if c == "direct":
            return "direct"
        if c == "transitive_d1" and descendants_class != "direct":
            descendants_class = "transitive_d1"
        elif c == "transitive_d2" and descendants_class not in ("direct", "transitive_d1"):
            descendants_class = "transitive_d2"
        elif c == "expect_actual" and descendants_class == "none":
            descendants_class = "expect_actual"
    return descendants_class


_TREE_COLOURS = {
    "direct":         "#B91C1C",
    "transitive_d1":  "#1D4ED8",
    "transitive_d2":  "#60A5FA",
    "expect_actual":  "#7C3AED",
    "none":           "#94A3B8",
}


def _prune_to_impacted(node: dict[str, Any]) -> dict[str, Any] | None:
    """Same logic as the JS pruneToImpacted in sunburst.html: drop leaves
    that aren't direct/transitive/expect_actual to keep the tree focused."""
    if not node.get("children"):
        if node.get("impact") in ("direct", "transitive", "expect_actual"):
            return dict(node)
        if node.get("is_expect") or node.get("is_actual"):
            return dict(node)
        return None
    pruned = []
    for c in node["children"]:
        kept = _prune_to_impacted(c)
        if kept is not None:
            pruned.append(kept)
    if not pruned:
        return None
    return {**{k: v for k, v in node.items() if k != "children"}, "children": pruned}


def build_tree_svg(consolidated: ConsolidatedResult) -> str:
    """Static horizontal D3-style propagation tree, rendered in pure Python.

    Pruned to nodes that touch impacted files so the tree stays focused on
    the propagation story rather than dumping the whole project. Layout is
    a simple Reingold–Tilford-style allocation: leaves stack along the y
    axis at depth × NODE_DY; internal nodes are placed at the centroid of
    their children. Node circles + curved bezier links + text labels match
    the look of the live D3 tree under the sunburst tab.
    """
    raw_tree = _build_tree(consolidated)
    pruned = _prune_to_impacted(raw_tree) or {"name": "src", "children": []}

    NODE_DX = 24
    NODE_DY = 165
    PAD_LEFT = 74
    PAD_TOP = 40

    leaves_y = [0]

    def assign(node: dict[str, Any], depth: int) -> dict[str, Any]:
        node["_depth"] = depth
        if not node.get("children"):
            node["_y"] = leaves_y[0] * NODE_DX
            leaves_y[0] += 1
            return node
        for c in node["children"]:
            assign(c, depth + 1)
        ys = [c["_y"] for c in node["children"]]
        node["_y"] = (ys[0] + ys[-1]) / 2
        return node

    assign(pruned, 0)
    # Width = depth * NODE_DY + label margin; height = leaves * NODE_DX
    max_depth = 0

    def collect_depth(n: dict[str, Any]) -> None:
        nonlocal max_depth
        max_depth = max(max_depth, n["_depth"])
        for c in n.get("children", []):
            collect_depth(c)
    collect_depth(pruned)
    width = PAD_LEFT + (max_depth + 1) * NODE_DY + 150
    height = PAD_TOP + max(leaves_y[0], 1) * NODE_DX + PAD_TOP

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="system-ui,sans-serif">'
        f'<rect width="100%" height="100%" fill="#F5F4F0"/>'
        f'<text x="{PAD_LEFT}" y="22" font-size="14" font-weight="700" fill="#1F2937">'
        f'Propagation tree</text>'
        f'<text x="{PAD_LEFT}" y="38" font-size="11" fill="#6B7280">'
        f'Same hierarchy as the sunburst, flattened for reading.</text>'
    )

    def x_for(d: int) -> float:
        return PAD_LEFT + d * NODE_DY

    def y_for(node: dict[str, Any]) -> float:
        return PAD_TOP + node["_y"] + NODE_DX / 2

    def short_name(name: str) -> str:
        n = name.replace(".kt", "")
        return n if len(n) <= 26 else n[:25] + "…"

    # Links — bezier curves between parent and each child.
    def emit_links(node: dict[str, Any]) -> None:
        if not node.get("children"):
            return
        x1 = x_for(node["_depth"])
        y1 = y_for(node)
        for c in node["children"]:
            x2 = x_for(c["_depth"])
            y2 = y_for(c)
            mx = (x1 + x2) / 2
            parts.append(
                f'<path d="M {x1:.1f} {y1:.1f} C {mx:.1f} {y1:.1f}, '
                f'{mx:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}" '
                f'fill="none" stroke="#CBD5E1" stroke-width="1.4" '
                f'stroke-opacity="0.85"/>'
            )
            emit_links(c)
    emit_links(pruned)

    # Nodes + labels.
    def emit_nodes(node: dict[str, Any]) -> None:
        cls = _classify_node(node)
        colour = _TREE_COLOURS[cls]
        x = x_for(node["_depth"])
        y = y_for(node)
        is_leaf = not node.get("children")
        r = 4 if is_leaf else (5 if node["_depth"] > 0 else 6)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFF" '
            f'stroke="{colour}" stroke-width="2.5"/>'
        )
        text_x = x + 10 if is_leaf or node["_depth"] == 0 else x - 10
        anchor = "start" if is_leaf or node["_depth"] == 0 else "end"
        weight = "500" if is_leaf else "600"
        # cairosvg does not respect paint-order reliably, so we just paint a
        # plain fill — the panel background (#F5F4F0) is light enough that
        # #1F2937 type stays readable without a halo stroke.
        parts.append(
            f'<text x="{text_x:.1f}" y="{y + 4:.1f}" font-size="11" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="#1F2937">'
            f'{html.escape(short_name(node.get("name", "")))}</text>'
        )
        for c in node.get("children", []):
            emit_nodes(c)
    emit_nodes(pruned)

    parts.append("</svg>")
    return "\n".join(parts)
