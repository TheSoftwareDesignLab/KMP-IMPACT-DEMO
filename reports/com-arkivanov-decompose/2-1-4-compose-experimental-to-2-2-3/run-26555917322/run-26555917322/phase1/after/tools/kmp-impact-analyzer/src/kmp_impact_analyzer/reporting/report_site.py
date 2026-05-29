"""Generate thesis-friendly HTML reports and CI summaries from pipeline outputs."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path
from typing import Any

from ..contracts import (
    CompatibilityWarning,
    ConsolidatedResult,
    DynamicStatus,
    ImpactRelation,
    ShadowManifest,
    UIRegressions,
)
from ..utils.log import get_logger
from .sunburst import build_sunburst_html
from .utg_image import build_utg_svg

log = get_logger(__name__)

_SKIPPED_ARTIFACT_PARTS = {
    '.git',
    '.gradle',
    '.idea',
    '.venv',
    '.venv-subagent',
    'build',
    'generated',
    'node_modules',
    'evidence',
}


def _risk_level(consolidated: ConsolidatedResult) -> str:
    direct = sum(1 for f in consolidated.static_impact.impacted_files if f.relation == ImpactRelation.DIRECT)
    screens = consolidated.total_impacted_screens
    if direct >= 8 or consolidated.total_impacted_files >= 20 or screens >= 6:
        return "high"
    if direct >= 3 or consolidated.total_impacted_files >= 8 or screens >= 2:
        return "medium"
    return "low"


def _recommendation(consolidated: ConsolidatedResult) -> str:
    risk = _risk_level(consolidated)
    dynamic = consolidated.dynamic_regressions.status
    if risk == "high":
        return "Hold merge until impacted files are reviewed and targeted regression checks pass."
    if dynamic == DynamicStatus.BLOCKED:
        return "Proceed cautiously: static evidence exists, but UI validation is still blocked and should be completed."
    if risk == "medium":
        return "Review the directly impacted files and run focused smoke tests before merging."
    return "Low apparent impact; merge is reasonable after normal review and basic validation."


def _dynamic_summary(ui: UIRegressions) -> str:
    if ui.status == DynamicStatus.COMPLETED:
        return f"completed ({len(ui.diffs)} screen diffs)"
    if ui.status == DynamicStatus.BLOCKED:
        return f"blocked ({ui.blocked_reason})"
    return "skipped"


def _top_impacted_files(consolidated: ConsolidatedResult, limit: int = 10) -> list[dict[str, Any]]:
    sorted_files = sorted(
        consolidated.static_impact.impacted_files,
        key=lambda fi: (
            0 if fi.relation == ImpactRelation.DIRECT else 1,
            -fi.metrics.mcc,
            -fi.metrics.rloc,
            fi.file_path,
        ),
    )
    rows: list[dict[str, Any]] = []
    for fi in sorted_files[:limit]:
        rows.append(
            {
                "file_path": fi.file_path,
                "relation": fi.relation.value,
                "distance": fi.distance,
                "source_set": fi.source_set,
                "rloc": fi.metrics.rloc,
                "mcc": fi.metrics.mcc,
                "declarations": fi.declarations,
            }
        )
    return rows


def _phase_status(consolidated: ConsolidatedResult) -> dict[str, dict[str, str]]:
    dynamic = consolidated.dynamic_regressions
    has_dynamic_data = len(dynamic.diffs) > 0 or len(dynamic.before_screens) > 0
    if dynamic.status == DynamicStatus.COMPLETED or has_dynamic_data:
        phase3_status = "completed"
        phase3_detail = f"{len(dynamic.diffs)} differences"
    elif dynamic.status == DynamicStatus.BLOCKED:
        phase3_status = "blocked"
        phase3_detail = dynamic.blocked_reason or "Blocked"
    else:
        phase3_status = "skipped"
        phase3_detail = "Skipped"

    return {
        "phase1": {
            "title": "Shadow Build",
            "status": "completed",
            "detail": "Completed",
        },
        "phase2": {
            "title": "Static Analysis",
            "status": "completed",
            "detail": f"{consolidated.total_impacted_files} files",
        },
        "phase3": {
            "title": "Dynamic Analysis",
            "status": phase3_status,
            "detail": phase3_detail,
        },
        "phase4": {
            "title": "Consolidation",
            "status": "completed",
            "detail": f"{consolidated.total_impacted_screens} screen(s)",
        },
        "phase5": {
            "title": "Visualization",
            "status": "completed",
            "detail": "CodeCharta",
        },
    }


def build_summary_payload(
    consolidated: ConsolidatedResult,
    manifest: ShadowManifest | None = None,
    report_url: str = "",
) -> dict[str, Any]:
    risk = _risk_level(consolidated)
    dyn = consolidated.dynamic_regressions
    payload = {
        "dependency_group": consolidated.dependency_group,
        "version_before": consolidated.version_before,
        "version_after": consolidated.version_after,
        "risk_level": risk,
        "recommendation": _recommendation(consolidated),
        "report_url": report_url,
        "total_impacted_files": consolidated.total_impacted_files,
        "total_impacted_screens": consolidated.total_impacted_screens,
        "direct_impacts": sum(1 for f in consolidated.static_impact.impacted_files if f.relation == ImpactRelation.DIRECT),
        "transitive_impacts": sum(1 for f in consolidated.static_impact.impacted_files if f.relation != ImpactRelation.DIRECT),
        "expect_actual_impacts": sum(1 for f in consolidated.static_impact.impacted_files if f.relation == ImpactRelation.EXPECT_ACTUAL),
        "expect_actual_pairs_total": len(consolidated.static_impact.expect_actual_pairs),
        "total_project_files": consolidated.static_impact.total_project_files,
        "dynamic_status": dyn.status.value,
        "dynamic_summary": _dynamic_summary(dyn),
        "dynamic_diffs": len(dyn.diffs),
        "before_screens": len(set(dyn.before_screens)),
        "after_screens": len(set(dyn.after_screens)),
        "dynamic_nodes_before": dyn.nodes_before,
        "dynamic_nodes_after": dyn.nodes_after,
        "dynamic_structures_before": dyn.structures_before,
        "dynamic_structures_after": dyn.structures_after,
        "screen_mappings": len(consolidated.screen_mappings),
        "trace_entries": len(consolidated.trace),
        "seed_files": consolidated.static_impact.seed_files,
        "impacted_screens": consolidated.impacted_screens,
        "top_impacted_files": _top_impacted_files(consolidated),
        "compat_warnings": [w.model_dump() for w in consolidated.stack_compatibility.warnings],
        "stack_detected": consolidated.stack_compatibility.detected,
    }
    if manifest is not None:
        payload["version_key"] = manifest.version_change.version_key
        payload["compilation_after"] = manifest.compilation_after.get("status", "skipped")
        payload["compile_errors"] = len(manifest.compilation_after.get("errors", []))
        payload["has_detekt"] = bool(manifest.detekt_reports)
        payload["has_kover"] = bool(manifest.kover_reports)

    # Detect which tools actually ran from impacted files and manifest
    has_ksp = consolidated.static_impact.ksp_edges_added > 0
    has_detekt_metrics = any(
        fi.metrics.metrics_source == "detekt"
        for fi in consolidated.static_impact.impacted_files
    )
    has_kover_data = any(
        fi.metrics.test_coverage >= 0
        for fi in consolidated.static_impact.impacted_files
    )
    payload["tools_used"] = {
        "tree_sitter": True,
        "ksp": has_ksp,
        "detekt": has_detekt_metrics or bool(manifest and manifest.detekt_reports),
        "kover": has_kover_data or bool(manifest and manifest.kover_reports),
        "droidbot": consolidated.dynamic_regressions.status.value != "skipped",
        "codecharta": True,
    }
    return payload


def build_summary_markdown(summary: dict[str, Any]) -> str:
    report_line = (
        f"- **Full report:** {summary['report_url']}"
        if summary.get("report_url")
        else "- **Full report:** generated as static artifact/site in `output/report/`"
    )
    lines = [
        "### Dependabot impact companion",
        "",
        f"- **Dependency:** `{summary['dependency_group']}`",
        f"- **Version change:** `{summary['version_before']}` → `{summary['version_after']}`",
        f"- **Risk:** **{summary['risk_level'].upper()}**",
        f"- **Recommendation:** {summary['recommendation']}",
        f"- **Static impact:** {summary['total_impacted_files']} files ({summary['direct_impacts']} direct / {summary['transitive_impacts']} transitive-or-expect-actual)",
        f"- **UI impact:** {summary['total_impacted_screens']} screens",
        f"- **Dynamic analysis:** {summary['dynamic_summary']}",
        report_line,
        "",
        "### Top impacted files",
        "",
        "| File | Relation | Source set | RLOC | MCC |",
        "|------|----------|------------|------|-----|",
    ]
    for row in summary.get("top_impacted_files", []):
        lines.append(
            f"| `{row['file_path']}` | {row['relation']} | {row['source_set']} | {row['rloc']} | {row['mcc']} |"
        )
    if not summary.get("top_impacted_files"):
        lines.append("| _None_ | - | - | - | - |")
    return "\n".join(lines) + "\n"


def _render_tool_badges(summary: dict[str, Any]) -> str:
    """Render colored badges for the optional analysis tools that ran.

    tree-sitter, DroidBot and CodeCharta are intentionally omitted: they are
    always present and adding them as badges only created visual noise per the
    user's feedback. The badges that remain genuinely communicate whether the
    Gradle-side tooling fired on this run.
    """
    tools = summary.get("tools_used", {})
    badges = []
    tool_config = [
        ("ksp", "KSP", "#6366f1", "Type resolution"),
        ("detekt", "Detekt", "#f59e0b", "Cyclomatic complexity"),
        ("kover", "Kover", "#3b82f6", "Test coverage"),
    ]
    for key, label, color, desc in tool_config:
        if tools.get(key):
            badges.append(
                f'<span style="display:inline-flex;align-items:center;gap:4px;'
                f'padding:4px 12px;border-radius:20px;font-size:11px;font-weight:600;'
                f'background:{color}15;color:{color};border:1px solid {color}40;" '
                f'title="{html.escape(desc)}">'
                f'<span style="width:6px;height:6px;border-radius:50%;background:{color};"></span>'
                f'{html.escape(label)}</span>'
            )
    return "\n".join(badges)


def _kpi_ratio(part: int, total: int) -> str:
    if total <= 0:
        return "—"
    pct = round((part / total) * 100)
    return f"{part}/{total} ({pct}%)"


def _expect_actual_caption(summary: dict[str, Any]) -> str:
    """Make the Expect/Actual KPI explicit even when no pair was hit."""
    total_pairs = summary.get("expect_actual_pairs_total", 0)
    affected = summary.get("expect_actual_impacts", 0)
    if total_pairs == 0:
        return "no pairs in project"
    if affected == 0:
        return f"{total_pairs} detected · 0 affected"
    return f"{affected} affected of {total_pairs}"


def _render_compat_warnings(summary: dict[str, Any]) -> str:
    """Render the stack-compatibility warnings as a banner if there are any."""
    warnings: list[dict[str, Any]] = summary.get("compat_warnings") or []
    if not warnings:
        return ""
    blocks: list[str] = []
    for w in warnings:
        title = html.escape(w.get("title", ""))
        detail = html.escape(w.get("detail", ""))
        suggestion = html.escape(w.get("suggestion", ""))
        detected = w.get("detected", {}) or {}
        bullets = " · ".join(
            f"<code>{html.escape(k)}={html.escape(str(v))}</code>"
            for k, v in detected.items()
            if v
        )
        blocks.append(
            f"""<div style='background:#fef2f2;border:1px solid #fecaca;border-radius:10px;
            padding:14px 18px;margin:10px 0;'>
              <div style='font-size:13px;font-weight:700;color:#991b1b;margin-bottom:4px;'>
                Stack compatibility · {title}
              </div>
              <div style='font-size:12.5px;color:#7f1d1d;margin-bottom:6px;'>{detail}</div>
              <div style='font-size:12px;color:#475569;margin-bottom:6px;'>{bullets}</div>
              <div style='font-size:12.5px;color:#0f172a;'><strong>Suggested action:</strong> {suggestion}</div>
            </div>"""
        )
    return "\n".join(blocks)


def _render_compilation_badge(summary: dict[str, Any]) -> str:
    """Render compilation status of the AFTER copy."""
    status = summary.get("compilation_after", "skipped")
    errors = summary.get("compile_errors", 0)
    if status == "success":
        return (
            '<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;'
            'padding:8px 16px;font-size:12px;color:#166534;margin:8px 0;">'
            '✅ The AFTER version compiles successfully — no breaking changes detected</div>'
        )
    elif status == "failure":
        return (
            f'<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;'
            f'padding:8px 16px;font-size:12px;color:#991b1b;margin:8px 0;">'
            f'⚠️ The AFTER version does not compile — {errors} compilation error(s) detected</div>'
        )
    return ""


def _artifact_links(output_dir: Path) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for pattern in ("*.json", "*.cc.json"):
        for path in sorted(output_dir.rglob(pattern)):
            rel = path.relative_to(output_dir)
            if set(rel.parts) & _SKIPPED_ARTIFACT_PARTS:
                continue
            pair = (rel.as_posix(), rel.as_posix())
            if pair in seen:
                continue
            seen.add(pair)
            links.append(pair)
    return links


def _load_toml_content(output_root: Path, variant: str) -> str:
    """Load libs.versions.toml content from phase1 shadow directories."""
    for candidate in [
        output_root / "phase1" / variant / "gradle" / "libs.versions.toml",
        output_root / "phase1" / variant / "gradle" / "libs.versions.toml",
    ]:
        if candidate.exists():
            try:
                return candidate.read_text(encoding="utf-8")
            except OSError:
                pass
    # Try to find any .toml in the variant directory
    variant_dir = output_root / "phase1" / variant
    if variant_dir.exists():
        for toml_path in variant_dir.rglob("libs.versions.toml"):
            try:
                return toml_path.read_text(encoding="utf-8")
            except OSError:
                pass
    return ""


def _load_embeddable_utg(output_root: Path) -> dict[str, Any] | None:
    iframe_path = output_root / 'phase3' / 'impact-utg' / 'index.html'
    if iframe_path.exists():
        return {'mode': 'iframe', 'href': 'phase3/impact-utg/index.html'}
    for rel in ['phase3/before/utg.js', 'phase3/after/utg.js']:
        path = output_root / rel
        if path.exists():
            return {'mode': 'js', 'path': path, 'label': rel}
    return None


def _render_propagation_graph_svg(consolidated: ConsolidatedResult) -> str:
    """Render a scrollable, selectable propagation graph."""
    direct_files = []
    trans1_files = []
    trans2_files = []

    def _sort_key(fi: Any) -> tuple[int, str]:
        return (-fi.metrics.rloc, fi.file_path)

    for fi in sorted(consolidated.static_impact.impacted_files, key=_sort_key):
        if fi.relation == ImpactRelation.DIRECT:
            direct_files.append(fi)
        elif fi.distance <= 1:
            trans1_files.append(fi)
        else:
            trans2_files.append(fi)

    # Keep every node visible; the surrounding container scrolls vertically
    # instead of collapsing long columns into "+N more".
    col_x = [44, 236, 430, 624]
    col_w = 158
    box_h = 42
    box_gap = 9
    header_y = 30
    start_y = 70

    def _node_id(path: str) -> str:
        return "n-" + str(abs(hash(path)))

    def _label(path: str) -> str:
        stem = Path(path).stem
        return stem if len(stem) <= 18 else stem[:17] + "…"

    def _column_boxes(files: list[Any], cx: int, col: str) -> list[dict[str, Any]]:
        boxes = []
        for i, fi in enumerate(files):
            y = start_y + i * (box_h + box_gap)
            boxes.append({
                "id": _node_id(fi.file_path),
                "file": fi.file_path,
                "label": _label(fi.file_path),
                "parents": [_node_id(p) for p in getattr(fi, "propagated_from", [])],
                "column": col,
                "x": cx,
                "y": y,
            })
        return boxes

    direct_boxes = _column_boxes(direct_files, col_x[1], "direct")
    trans1_boxes = _column_boxes(trans1_files, col_x[2], "trans1")
    trans2_boxes = _column_boxes(trans2_files, col_x[3], "trans2")
    all_boxes = direct_boxes + trans1_boxes + trans2_boxes
    tallest_count = max(len(direct_boxes), len(trans1_boxes), len(trans2_boxes), 1)
    svg_h = start_y + tallest_count * (box_h + box_gap) + 24
    dep_box_y = start_y + max(0, (len(direct_boxes) - 1)) * (box_h + box_gap) // 2
    dep_id = "dependency-root"

    parts = [
        "<div class='prop-graph-wrap'>",
        "<div class='prop-graph-help'>Click a box to highlight only the files reached in the next column. Scroll vertically when the columns are long.</div>",
        "<div class='prop-graph-scroll'>",
        f"<svg viewBox='0 0 830 {svg_h}' xmlns='http://www.w3.org/2000/svg' class='prop-graph-svg' style='height:{svg_h}px;'>",
    ]

    headers = [
        (col_x[0] + col_w // 2, "DEPENDENCY", "#4338ca"),
        (col_x[1] + col_w // 2, "DIRECT", "#dc2626"),
        (col_x[2] + col_w // 2, f"TRANSITIVE\n(dist 1: {len(trans1_files)})", "#f59e0b"),
        (col_x[3] + col_w // 2, f"TRANSITIVE\n(dist 2+: {len(trans2_files)})", "#f97316"),
    ]
    for hx, label, color in headers:
        for li, line in enumerate(label.split("\n")):
            parts.append(
                f"<text x='{hx}' y='{header_y + li * 16}' text-anchor='middle' "
                f"fill='{color}' font-size='11' font-weight='700'>{html.escape(line)}</text>"
            )

    dep_name = html.escape(consolidated.dependency_group.split(".")[-1].upper())
    dep_label2 = f"{html.escape(consolidated.version_before)} → {html.escape(consolidated.version_after)}"
    parts.append(
        f"<g class='prop-node prop-dep' data-id='{dep_id}' data-column='dependency' tabindex='0'>"
        f"<rect x='{col_x[0]}' y='{dep_box_y}' width='{col_w}' height='{box_h + 10}' rx='8' fill='#4338ca'/>"
        f"<text x='{col_x[0] + col_w // 2}' y='{dep_box_y + 22}' text-anchor='middle' fill='white' font-size='13' font-weight='700'>{dep_name}</text>"
        f"<text x='{col_x[0] + col_w // 2}' y='{dep_box_y + 38}' text-anchor='middle' fill='white' font-size='10' opacity='0.72'>{dep_label2}</text>"
        "</g>"
    )

    dep_cx = col_x[0] + col_w
    dep_cy = dep_box_y + (box_h + 10) // 2
    for box in direct_boxes:
        parts.append(
            f"<line class='prop-edge prop-edge-real' data-from='{dep_id}' data-to='{box['id']}' "
            f"x1='{dep_cx}' y1='{dep_cy}' x2='{box['x']}' y2='{box['y'] + box_h // 2}'/>"
        )

    box_by_id = {box["id"]: box for box in all_boxes}
    for box in trans1_boxes + trans2_boxes:
        for parent_id in box["parents"]:
            parent = box_by_id.get(parent_id)
            if not parent:
                continue
            parts.append(
                f"<line class='prop-edge prop-edge-real prop-edge-hop' data-from='{parent_id}' data-to='{box['id']}' "
                f"x1='{parent['x'] + col_w}' y1='{parent['y'] + box_h // 2}' "
                f"x2='{box['x']}' y2='{box['y'] + box_h // 2}'/>"
            )

    def _column_mid(boxes: list[dict[str, Any]]) -> int | None:
        if not boxes:
            return None
        ys = [b["y"] + box_h // 2 for b in boxes]
        return (min(ys) + max(ys)) // 2

    direct_cy = _column_mid(direct_boxes)
    trans1_cy = _column_mid(trans1_boxes)
    trans2_cy = _column_mid(trans2_boxes)
    if direct_cy is not None and trans1_cy is not None:
        parts.append(
            f"<line class='prop-guide' x1='{col_x[1] + col_w}' y1='{direct_cy}' x2='{col_x[2]}' y2='{trans1_cy}'/>"
            f"<text class='prop-guide-label' x='{(col_x[1] + col_w + col_x[2]) // 2}' y='{(direct_cy + trans1_cy) // 2 - 7}' text-anchor='middle'>imports of imports</text>"
        )
    if trans1_cy is not None and trans2_cy is not None:
        parts.append(
            f"<line class='prop-guide orange' x1='{col_x[2] + col_w}' y1='{trans1_cy}' x2='{col_x[3]}' y2='{trans2_cy}'/>"
            f"<text class='prop-guide-label orange' x='{(col_x[2] + col_w + col_x[3]) // 2}' y='{(trans1_cy + trans2_cy) // 2 - 7}' text-anchor='middle'>further hops</text>"
        )

    def _draw_boxes(boxes: list[dict[str, Any]], fill: str) -> None:
        for box in boxes:
            parts.append(
                f"<g class='prop-node' data-id='{box['id']}' data-column='{box['column']}' "
                f"data-parents='{html.escape(json.dumps(box['parents']))}' tabindex='0'>"
                f"<title>{html.escape(box['file'])}</title>"
                f"<rect x='{box['x']}' y='{box['y']}' width='{col_w}' height='{box_h}' rx='7' fill='{fill}'/>"
                f"<text x='{box['x'] + col_w // 2}' y='{box['y'] + box_h // 2 + 2}' text-anchor='middle' fill='white' font-size='11' font-weight='700'>{html.escape(box['label'])}</text>"
                f"<text x='{box['x'] + col_w // 2}' y='{box['y'] + box_h // 2 + 15}' text-anchor='middle' fill='white' font-size='9' opacity='0.72'>.kt</text>"
                "</g>"
            )

    _draw_boxes(direct_boxes, "#dc2626")
    _draw_boxes(trans1_boxes, "#f59e0b")
    _draw_boxes(trans2_boxes, "#f97316")

    parts.append("</svg></div></div>")
    parts.append("""
<script>
(function () {
  const root = document.currentScript.previousElementSibling;
  if (!root || !root.classList.contains('prop-graph-wrap')) return;
  const nodes = Array.from(root.querySelectorAll('.prop-node'));
  const edges = Array.from(root.querySelectorAll('.prop-edge-real'));
  function reset() {
    nodes.forEach(n => n.classList.remove('is-dimmed', 'is-selected', 'is-related'));
    edges.forEach(e => e.classList.remove('is-visible'));
  }
  function select(node) {
    const id = node.dataset.id;
    const column = node.dataset.column;
    reset();
    node.classList.add('is-selected');
    let childIds = new Set();
    if (column === 'dependency') {
      childIds = new Set(nodes.filter(n => n.dataset.column === 'direct').map(n => n.dataset.id));
    } else if (column === 'direct' || column === 'trans1') {
      childIds = new Set(edges.filter(e => e.dataset.from === id).map(e => e.dataset.to));
    }
    if (!childIds.size) return;
    nodes.forEach(n => {
      if (n === node || childIds.has(n.dataset.id)) n.classList.add('is-related');
      else n.classList.add('is-dimmed');
    });
    edges.forEach(e => {
      if (e.dataset.from === id && childIds.has(e.dataset.to)) e.classList.add('is-visible');
    });
  }
  nodes.forEach(node => {
    node.addEventListener('click', ev => {
      ev.stopPropagation();
      if (node.classList.contains('is-selected')) reset();
      else select(node);
    });
    node.addEventListener('keydown', ev => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        select(node);
      }
    });
  });
  root.addEventListener('dblclick', reset);
})();
</script>
""")
    return "\n".join(parts)


def _render_donut_svg(summary: dict[str, Any]) -> str:
    """Render a donut chart SVG showing impact distribution."""
    total = summary["total_project_files"] or 1
    direct = summary["direct_impacts"]
    ea = summary["expect_actual_impacts"]
    transitive = summary["transitive_impacts"] - ea
    not_impacted = total - direct - transitive - ea

    segments = [
        (direct, "#dc2626", "Direct"),
        (transitive, "#f59e0b", "Transitive"),
        (ea, "#7c3aed", "Expect/Actual"),
        (not_impacted, "#e2e8f0", "Not impacted"),
    ]

    cx, cy, r = 120, 120, 90
    inner_r = 55
    svg = [f"<svg viewBox='0 0 240 300' xmlns='http://www.w3.org/2000/svg' style='width:100%;max-width:400px;font-family:Inter,system-ui,sans-serif;'>"]

    offset = 0
    for value, color, label in segments:
        if value <= 0:
            continue
        pct = value / total
        angle = pct * 360
        large = 1 if angle > 180 else 0
        start_rad = math.radians(offset - 90)
        end_rad = math.radians(offset + angle - 90)

        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)

        ix1 = cx + inner_r * math.cos(start_rad)
        iy1 = cy + inner_r * math.sin(start_rad)
        ix2 = cx + inner_r * math.cos(end_rad)
        iy2 = cy + inner_r * math.sin(end_rad)

        d = f"M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} L {ix2:.1f} {iy2:.1f} A {inner_r} {inner_r} 0 {large} 0 {ix1:.1f} {iy1:.1f} Z"
        svg.append(f"<path d='{d}' fill='{color}'/>")

        # Percentage label
        mid_rad = math.radians(offset + angle / 2 - 90)
        label_r = (r + inner_r) / 2 + 20
        lx = cx + label_r * math.cos(mid_rad)
        ly = cy + label_r * math.sin(mid_rad)
        if pct >= 0.05:
            svg.append(f"<text x='{lx:.1f}' y='{ly:.1f}' text-anchor='middle' fill='#374151' font-size='12' font-weight='600'>{pct:.0%}</text>")

        offset += angle

    # Center text
    impacted_total = summary["total_impacted_files"]
    svg.append(f"<text x='{cx}' y='{cy - 4}' text-anchor='middle' fill='#1e293b' font-size='28' font-weight='700'>{impacted_total}</text>")
    svg.append(f"<text x='{cx}' y='{cy + 16}' text-anchor='middle' fill='#64748b' font-size='11'>impacted</text>")

    # Legend
    ly = 260
    for value, color, label in segments:
        if value <= 0 and label != "Expect/Actual":
            continue
        svg.append(f"<rect x='20' y='{ly - 8}' width='12' height='12' rx='2' fill='{color}'/>")
        svg.append(f"<text x='38' y='{ly + 2}' fill='#374151' font-size='11' font-weight='600'>{html.escape(label)}</text>")
        ly += 20

    svg.append("</svg>")
    return "\n".join(svg)


def _render_bar_charts_svg(consolidated: ConsolidatedResult) -> str:
    """Render horizontal bar charts for RLOC and MCC (top 15)."""
    files_sorted_rloc = sorted(
        consolidated.static_impact.impacted_files,
        key=lambda f: -f.metrics.rloc,
    )[:15]
    files_sorted_mcc = sorted(
        consolidated.static_impact.impacted_files,
        key=lambda f: -f.metrics.mcc,
    )[:15]

    def _bar_chart(files: list, metric: str, title: str, x_label: str) -> str:
        if not files:
            return ""
        max_val = max(getattr(f.metrics, metric) for f in files) or 1
        bar_h = 18
        gap = 6
        label_w = 140
        chart_w = 280
        total_h = 40 + len(files) * (bar_h + gap)
        svg = [f"<svg viewBox='0 0 {label_w + chart_w + 50} {total_h}' xmlns='http://www.w3.org/2000/svg' style='width:100%;font-family:Inter,system-ui,sans-serif;'>"]
        svg.append(f"<text x='{(label_w + chart_w + 50) // 2}' y='16' text-anchor='middle' fill='#374151' font-size='12' font-weight='700'>{html.escape(title)}</text>")
        y = 34
        for fi in files:
            val = getattr(fi.metrics, metric)
            w = (val / max_val) * chart_w if max_val > 0 else 0
            short = Path(fi.file_path).name
            if len(short) > 18:
                short = short[:16] + ".."
            is_direct = fi.relation == ImpactRelation.DIRECT
            color = "#dc2626" if is_direct else "#f59e0b"
            svg.append(f"<text x='{label_w - 4}' y='{y + bar_h // 2 + 4}' text-anchor='end' fill='#374151' font-size='10'>{html.escape(short)}</text>")
            svg.append(f"<rect x='{label_w}' y='{y}' width='{w:.1f}' height='{bar_h}' rx='3' fill='{color}'/>")
            svg.append(f"<text x='{label_w + w + 4:.1f}' y='{y + bar_h // 2 + 4}' fill='#374151' font-size='10' font-weight='600'>{val}</text>")
            y += bar_h + gap

        # X-axis label
        svg.append(f"<text x='{label_w + chart_w // 2}' y='{total_h - 2}' text-anchor='middle' fill='#94a3b8' font-size='9'>{html.escape(x_label)}</text>")
        svg.append("</svg>")
        return "\n".join(svg)

    rloc_svg = _bar_chart(files_sorted_rloc, "rloc", "Real lines of code (top 15)", "Lines of code (RLOC)")
    # Label reflects whether Detekt or heuristic was used for complexity
    has_detekt = any(
        fi.metrics.metrics_source == "detekt"
        for fi in consolidated.static_impact.impacted_files
    )
    mcc_title = "Cyclomatic complexity — Detekt (top 15)" if has_detekt else "Heuristic complexity (top 15)"
    mcc_svg = _bar_chart(files_sorted_mcc, "mcc", mcc_title, "Cyclomatic complexity (MCC)")

    return f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>{rloc_svg}{mcc_svg}</div>"


def _build_html(
    summary: dict[str, Any],
    consolidated: ConsolidatedResult,
    manifest: ShadowManifest,
    output_root: Path,
) -> str:
    dep_group = html.escape(summary['dependency_group'])
    ver_before = html.escape(summary['version_before'])
    ver_after = html.escape(summary['version_after'])
    ea_count = summary['expect_actual_impacts']

    # Phase status
    phase_status = _phase_status(consolidated)

    # Pipeline steps
    pipe_steps = ""
    for idx, (key, data) in enumerate(phase_status.items(), start=1):
        status_cls = "green" if data["status"] == "completed" else ("amber" if data["status"] == "blocked" else "gray")
        status_prefix = "✓ " if data["status"] == "completed" else ""
        skip_cls = " skip" if data["status"] == "skipped" else ""
        pipe_steps += f'<div class="pipe-step"><div class="dot {status_cls}">{idx}</div><div class="title">{html.escape(data["title"])}</div><div class="status{skip_cls}">{status_prefix}{html.escape(data["detail"])}</div></div>\n'

    # Shadow build: load toml content
    before_toml = _load_toml_content(output_root, "before")
    after_toml = _load_toml_content(output_root, "after")

    version_key = manifest.version_change.version_key

    def _highlight_toml(content: str) -> str:
        """Highlight lines containing the version key."""
        if not content:
            return "<em>libs.versions.toml not found</em>"
        lines = content.split("\n")
        result = []
        for line in lines:
            if version_key.lower() in line.lower():
                result.append(f'<span class="hl">{html.escape(line)}</span>')
            else:
                result.append(html.escape(line))
        return "\n".join(result)

    # Phase 2: Propagation graph SVG (the donut and bar charts were removed at
    # the user's request — the propagation diagram already conveys the same
    # signal more directly).
    propagation_svg = _render_propagation_graph_svg(consolidated)

    # Phase 3: Dynamic analysis — embed the real DroidBot Cytoscape viewer.
    # The HTML is patched in-place by `utg_decorate.colorize_droidbot_html` to
    # add red / amber / purple borders to nodes whose screen names match the
    # static-impact relations.
    dynamic = consolidated.dynamic_regressions
    impact_iframe = output_root / 'phase3' / 'impact-utg' / 'index.html'

    dynamic_section = ""
    if impact_iframe.exists():
        dynamic_section += """
<div style="background:white;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05);margin-bottom:14px;">
  <iframe src="phase3/impact-utg/index.html" style="width:100%;height:640px;border:none;border-radius:12px;"></iframe>
</div>
<div style="text-align:center;margin-bottom:14px;">
  <a href="phase3/impact-utg/index.html" target="_blank" style="display:inline-block;padding:10px 22px;background:#1e293b;color:white;border-radius:8px;font-weight:600;font-size:12px;text-decoration:none;">
    Open DroidBot UTG full-screen
  </a>
</div>"""
    else:
        reason = dynamic.blocked_reason or "No DroidBot artifacts were generated in this run."
        status_label = "SKIPPED" if dynamic.status == DynamicStatus.SKIPPED else "BLOCKED"
        dynamic_section += f"""
<div style="background:#f8fafc;border-radius:12px;border:1px dashed #cbd5e1;padding:40px 24px;text-align:center;margin-bottom:16px;">
  <div style="font-size:16px;font-weight:700;color:#94a3b8;margin-bottom:8px;">{status_label}</div>
  <div style="font-size:13px;color:#64748b;">{html.escape(reason)}</div>
</div>"""

    # Compact KPI strip: just the numbers, no explainer paragraphs.
    explored = max(
        len(set(dynamic.before_screens) | set(dynamic.after_screens)),
        dynamic.structures_before + dynamic.structures_after,
    )
    nodes_total = dynamic.nodes_before + dynamic.nodes_after
    dynamic_section += f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
  <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;padding:14px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#1e293b;">{nodes_total}</div>
    <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">UTG nodes</div>
  </div>
  <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;padding:14px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#1e293b;">{explored}</div>
    <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Distinct UI surfaces</div>
  </div>
  <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;padding:14px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#dc2626;">{len(dynamic.diffs)}</div>
    <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Behaviour diffs</div>
  </div>
  <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;padding:14px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#4338ca;">{summary['total_impacted_screens']}</div>
    <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Impacted screens (static)</div>
  </div>
</div>"""

    # Dynamic diffs
    for diff in dynamic.diffs:
        dynamic_section += f"""
<div style="background:white;border-radius:10px;border-left:4px solid #fbbf24;padding:12px 16px;margin-top:8px;">
  <strong style="font-size:13px;color:#1e293b;">{html.escape(diff.screen_name)}</strong>
  <div style="font-size:12px;color:#64748b;margin-top:2px;">{html.escape(diff.details)}</div>
</div>"""

    # Phase 4: Traceability table
    trace_rows = ""
    for i, entry in enumerate(sorted(consolidated.trace, key=lambda item: (item.distance, item.file_path))):
        short_name = Path(entry.file_path).name
        alt_cls = ' class="row-alt"' if i % 2 == 1 else ''
        if entry.relation == ImpactRelation.DIRECT:
            badge = '<span class="badge badge-red">Direct</span>'
        elif entry.relation == ImpactRelation.EXPECT_ACTUAL:
            badge = '<span class="badge badge-purple">Expect/Actual</span>'
        else:
            badge = '<span class="badge badge-yellow">Transitive</span>'
        screens_str = ", ".join(html.escape(s) for s in entry.screens) if entry.screens else "—"
        cov = f"{entry.metrics.test_coverage:.0f}%" if entry.metrics.test_coverage >= 0 else "—"
        src_badge = (
            '<span style="font-size:9px;padding:1px 5px;border-radius:3px;background:#6366f115;color:#6366f1;">Detekt</span>'
            if entry.metrics.metrics_source == "detekt"
            else '<span style="font-size:9px;padding:1px 5px;border-radius:3px;background:#94a3b815;color:#94a3b8;">Heur.</span>'
        )
        trace_rows += f"""<tr{alt_cls}>
  <td class="fname">{html.escape(short_name)}</td>
  <td>{badge}</td>
  <td class="c">{entry.distance}</td>
  <td class="c">{entry.metrics.rloc}</td>
  <td class="c">{entry.metrics.mcc} {src_badge}</td>
  <td class="c">{cov}</td>
  <td>{screens_str}</td>
</tr>\n"""

    # Expect/Actual pairs — only render when at least one *impacted* file is an
    # expect/actual bridge for the bumped dependency. Showing every detected
    # pair (even when none are affected) confused readers in earlier runs.
    ea_section = ""
    impacted_files_set = {fi.file_path for fi in consolidated.static_impact.impacted_files}
    affected_pairs = [
        p for p in consolidated.static_impact.expect_actual_pairs
        if p.expect_file in impacted_files_set or any(af in impacted_files_set for af in p.actual_files)
    ]
    if affected_pairs:
        def _platform_tag(path: str) -> str:
            p = path.lower()
            if "androidmain" in p or "/android/" in p:
                return "android"
            if "iosmain" in p or "/ios/" in p:
                return "ios"
            if "jvmmain" in p or "desktopmain" in p:
                return "jvm"
            if "wasmmain" in p or "jsmain" in p:
                return "js/wasm"
            return "common"

        ea_rows = ""
        for pair in affected_pairs:
            actual_parts = []
            for af in pair.actual_files:
                tag = _platform_tag(af)
                actual_parts.append(
                    f"<code style='font-size:11px;background:#eef2ff;color:#4338ca;"
                    f"padding:1px 6px;border-radius:4px;margin-right:6px;'>"
                    f"{html.escape(tag)}</code>{html.escape(Path(af).name)}"
                )
            ea_rows += f"""<tr>
  <td class="fname">{html.escape(pair.expect_fqcn)}</td>
  <td><code>{html.escape(Path(pair.expect_file).name)}</code></td>
  <td>{"<br>".join(actual_parts)}</td>
</tr>\n"""

        ea_section = f"""
<div class="section">
  <div class="section-header">
    <div class="phase-num" style="background:#7c3aed;">EA</div>
    <div><h2>Affected Expect/Actual Pairs</h2><div class="desc">Multiplatform declarations linking commonMain with platform-specific implementations that intersect the impacted files for this PR</div></div>
  </div>
  <table class="data-table">
    <thead><tr><th>FQCN</th><th>Expect file</th><th>Actual files</th></tr></thead>
    <tbody>{ea_rows}</tbody>
  </table>
</div>"""

    # Phase 5: CodeCharta
    cc_iframe = ""
    cc_viewer_path = output_root / "phase5" / "codecharta-viewer" / "index.html"
    if cc_viewer_path.exists():
        import time
        after_cc = output_root / "phase5" / "after.cc.json"
        ts = int(after_cc.stat().st_mtime) if after_cc.exists() else int(time.time())
        # impact_level (0=no impact, 1=transitive, 2=direct) gives the city a
        # three-stop colour ramp so direct and transitive files no longer share
        # a single red shade.
        cc_src = (
            "phase5/codecharta-viewer/index.html"
            "?file=../after.cc.json"
            "&mode=Single&area=rloc&height=mcc&color=impact_level"
            f"&ts={ts}"
        )
        cc_iframe = f"""
<div style="background:white;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:16px;">
  <iframe id="codecharta-frame" src="{cc_src}" style="width:100%;height:650px;border:none;border-radius:12px;"></iframe>
</div>
<div style="text-align:center;margin-bottom:16px;">
  <a href="{cc_src}" target="_blank" style="display:inline-block;padding:12px 28px;background:#4338ca;color:white;border-radius:8px;font-weight:600;font-size:13px;text-decoration:none;">
    Open CodeCharta fullscreen
  </a>
</div>"""
    else:
        # Fallback: show link to external CodeCharta viewer
        cc_iframe = """
<div style="background:#f8fafc;border-radius:12px;border:1px dashed #cbd5e1;padding:40px 24px;text-align:center;margin-bottom:16px;">
  <div style="font-size:14px;color:#64748b;margin-bottom:12px;">CodeCharta artifacts (.cc.json) are available for external exploration.</div>
  <a href="https://maibornwolff.github.io/codecharta/visualization/app/index.html" target="_blank" style="display:inline-block;padding:12px 28px;background:#4338ca;color:white;border-radius:8px;font-weight:600;font-size:13px;text-decoration:none;">
    Open CodeCharta Visualization
  </a>
</div>"""

    sunburst_block = build_sunburst_html(consolidated)

    gitgraph_index = output_root / "gitgraph" / "arc_diagram.html"
    if gitgraph_index.exists():
        # Pass the bumped dependency group so the diagram opens already focused
        # on it (ringed in yellow + recentred in the viewport).
        from urllib.parse import quote_plus
        focal_qs = f"?focal={quote_plus(consolidated.dependency_group)}"
        gitgraph_block = f"""
<div style="background:white;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:16px;">
  <iframe src="gitgraph/arc_diagram.html{focal_qs}" style="width:100%;height:720px;border:none;border-radius:12px;"></iframe>
</div>
<div style="text-align:center;margin-bottom:16px;">
  <a href="gitgraph/arc_diagram.html{focal_qs}" target="_blank" style="display:inline-block;padding:12px 28px;background:#4338ca;color:white;border-radius:8px;font-weight:600;font-size:13px;text-decoration:none;">
    Open dependency graph fullscreen
  </a>
  <div style="font-size:11px;color:#94a3b8;margin-top:6px;">Pan with click-drag · zoom with mouse wheel · the bumped library is ringed in yellow.</div>
</div>"""
    else:
        gitgraph_block = """
<div style="background:#fff;border-radius:12px;border:1px dashed #cbd5e1;padding:32px 28px;margin-bottom:16px;">
  <div style="font-size:15px;font-weight:700;color:#0f172a;margin-bottom:10px;">Dependency graph not produced for this run</div>
  <div style="font-size:13px;color:#475569;line-height:1.6;margin-bottom:14px;">
    The GitGraph SBOM pipeline did not generate <code style="background:#f1f5f9;padding:2px 6px;border-radius:4px;color:#dc2626;">gitgraph/arc_diagram.html</code> for this report.
    Verify the items below in <strong>Settings</strong>:
  </div>
  <ol style="font-size:13px;color:#334155;line-height:1.7;margin:0 0 0 1.2em;padding:0;">
    <li><strong>Settings &rarr; Security &rarr; Dependency graph</strong> must be <em>Enabled</em>.</li>
    <li><strong>Settings &rarr; Actions &rarr; General &rarr; Workflow permissions</strong> must be set to <em>Read and write permissions</em> (so <code>GITHUB_TOKEN</code> includes <code>dependency_graph: read</code>).</li>
    <li>Optional: provide a <code>DEP_GRAPH_PAT</code> secret (fine-grained PAT with <code>dependency_graph: read</code>) if the default token still gets <code>403</code>.</li>
  </ol>
  <div style="font-size:12px;color:#94a3b8;margin-top:14px;">Once those are set, re-run the workflow on the PR to refresh the report.</div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Impact Report — {dep_group}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',system-ui,sans-serif; background:#f8fafc; color:#1e293b; line-height:1.6; }}

  /* Header */
  .header {{ background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#4338ca 100%); color:white; padding:48px 0 40px; }}
  .header-inner {{ max-width:1000px; margin:0 auto; padding:0 32px; }}
  .header h1 {{ font-size:28px; font-weight:700; margin-bottom:4px; }}
  .header .sub {{ font-size:14px; opacity:0.7; }}
  .version-pill {{ display:inline-block; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25);
    border-radius:20px; padding:6px 18px; margin-top:16px; font-size:15px; font-weight:600; }}
  .version-pill .arrow {{ color:#a5b4fc; margin:0 8px; }}

  /* Container */
  .container {{ max-width:1000px; margin:0 auto; padding:0 32px 60px; }}

  /* KPI cards */
  .kpi-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:-32px 0 40px; position:relative; z-index:2; }}
  .kpi {{ background:white; border-radius:12px; padding:24px; text-align:center;
    box-shadow:0 1px 3px rgba(0,0,0,0.08),0 4px 12px rgba(0,0,0,0.04); border:1px solid #e2e8f0; }}
  .kpi .num {{ font-size:32px; font-weight:700; }}
  .kpi .lbl {{ font-size:12px; color:#64748b; margin-top:4px; text-transform:uppercase; letter-spacing:0.5px; }}
  .kpi .kpi-sub {{ font-size:11px; color:#94a3b8; margin-top:6px; font-weight:500; }}
  .kpi .num.red {{ color:#dc2626; }}
  .kpi .num.amber {{ color:#d97706; }}
  .kpi .num.purple {{ color:#7c3aed; }}
  .kpi .num.blue {{ color:#2563eb; }}

  /* Section */
  .section {{ margin-bottom:40px; }}
  .section-header {{ display:flex; align-items:center; gap:12px; margin-bottom:20px; padding-bottom:12px; border-bottom:2px solid #e2e8f0; }}
  .phase-num {{ background:#4338ca; color:white; width:32px; height:32px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; flex-shrink:0; }}
  .section-header h2 {{ font-size:18px; font-weight:700; color:#1e293b; }}
  .section-header .desc {{ font-size:13px; color:#64748b; }}

  /* Pipeline */
  .pipeline {{ display:flex; gap:0; margin:24px 0 40px; justify-content:center; }}
  .pipe-step {{ text-align:center; flex:1; position:relative; }}
  .pipe-step .dot {{ width:40px; height:40px; border-radius:50%; margin:0 auto 8px;
    display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:700; color:white; }}
  .pipe-step .dot.green {{ background:#16a34a; }}
  .pipe-step .dot.gray {{ background:#9ca3af; }}
  .pipe-step .dot.amber {{ background:#d97706; }}
  .pipe-step .title {{ font-size:12px; font-weight:600; color:#374151; }}
  .pipe-step .status {{ font-size:11px; color:#16a34a; font-weight:500; }}
  .pipe-step .status.skip {{ color:#9ca3af; }}
  .pipe-step:not(:last-child)::after {{ content:''; position:absolute; top:20px; left:calc(50% + 24px);
    width:calc(100% - 48px); height:3px; background:#d1d5db; }}

  /* Diff cards */
  .diff-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  .diff-card {{ background:white; border-radius:10px; border:1px solid #e2e8f0; overflow:hidden;
    box-shadow:0 1px 3px rgba(0,0,0,0.05); }}
  .diff-card .card-head {{ padding:12px 16px; font-size:12px; font-weight:600; text-transform:uppercase;
    letter-spacing:0.5px; }}
  .diff-card.before .card-head {{ background:#fef2f2; color:#991b1b; border-bottom:2px solid #fca5a5; }}
  .diff-card.after .card-head {{ background:#f0fdf4; color:#166534; border-bottom:2px solid #86efac; }}
  .diff-card pre {{ padding:16px; font-size:12px; line-height:1.7; overflow-x:auto; background:#fafafa; margin:0; }}
  .diff-card pre .hl {{ background:#fef08a; font-weight:600; display:inline; padding:1px 4px; border-radius:3px; }}

  /* Chart card */
  .chart-card {{ background:white; border-radius:12px; border:1px solid #e2e8f0; padding:20px;
    box-shadow:0 1px 3px rgba(0,0,0,0.05); margin-bottom:16px; }}
  .chart-card .caption {{ font-size:12px; color:#64748b; margin-top:8px; text-align:center; }}
  .prop-graph-wrap {{ border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; background:#fff; }}
  .prop-graph-help {{ padding:10px 14px; font-size:12px; color:#64748b; background:#f8fafc; border-bottom:1px solid #e2e8f0; }}
  .prop-graph-scroll {{ max-height:620px; overflow-y:auto; overflow-x:hidden; }}
  .prop-graph-svg {{ width:100%; min-height:360px; display:block; font-family:Inter,system-ui,sans-serif; }}
  .prop-node {{ cursor:pointer; transition:opacity .15s, filter .15s; outline:none; }}
  .prop-node rect {{ transition:stroke .15s, stroke-width .15s, filter .15s; }}
  .prop-node:hover rect, .prop-node:focus rect {{ stroke:#0f172a; stroke-width:2; filter:drop-shadow(0 3px 6px rgba(15,23,42,.18)); }}
  .prop-node.is-selected rect {{ stroke:#0f172a; stroke-width:3; filter:drop-shadow(0 4px 8px rgba(15,23,42,.22)); }}
  .prop-node.is-dimmed {{ opacity:.24; }}
  .prop-node.is-related rect {{ stroke:#111827; stroke-width:2.5; filter:drop-shadow(0 3px 8px rgba(15,23,42,.2)); }}
  .prop-edge-real {{ stroke:#64748b; stroke-width:1.2; opacity:.12; pointer-events:none; }}
  .prop-edge-hop {{ stroke-dasharray:4 4; }}
  .prop-edge-real.is-visible {{ opacity:.82; stroke-width:2.3; stroke:#4338ca; }}
  .prop-guide {{ stroke:#f59e0b; stroke-width:2; stroke-dasharray:6 5; opacity:.35; pointer-events:none; }}
  .prop-guide.orange {{ stroke:#f97316; }}
  .prop-guide-label {{ fill:#b45309; font-size:9px; font-weight:700; opacity:.72; pointer-events:none; }}
  .prop-guide-label.orange {{ fill:#9a3412; }}

  /* Table */
  .data-table {{ width:100%; border-collapse:separate; border-spacing:0; background:white;
    border-radius:12px; overflow:hidden; border:1px solid #e2e8f0;
    box-shadow:0 1px 3px rgba(0,0,0,0.05); }}
  .data-table th {{ background:#f8fafc; color:#475569; padding:12px 16px; text-align:left;
    font-size:11px; text-transform:uppercase; letter-spacing:0.5px; font-weight:600; border-bottom:2px solid #e2e8f0; }}
  .data-table td {{ padding:11px 16px; font-size:13px; border-bottom:1px solid #f1f5f9; }}
  .data-table .row-alt td {{ background:#fafbfc; }}
  .data-table .fname {{ font-family:'SF Mono',Consolas,monospace; font-size:12.5px; font-weight:600; color:#1e293b; }}
  .data-table .c {{ text-align:center; }}
  .badge {{ padding:3px 10px; border-radius:10px; font-size:11px; font-weight:600; }}
  .badge-red {{ background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }}
  .badge-yellow {{ background:#fffbeb; color:#d97706; border:1px solid #fde68a; }}
  .badge-purple {{ background:#f5f3ff; color:#7c3aed; border:1px solid #ddd6fe; }}
  .table-scroll {{ max-height:620px; overflow:auto; border-radius:12px; border:1px solid #e2e8f0;
    box-shadow:0 1px 3px rgba(0,0,0,0.05); background:white; }}
  .table-scroll .data-table {{ border:none; border-radius:0; box-shadow:none; }}
  .table-scroll thead th {{ position:sticky; top:0; z-index:2; }}

  /* Info box */
  .info-box {{ background:#eef2ff; border:1px solid #c7d2fe; border-radius:10px; padding:20px 24px; }}
  .info-box h4 {{ color:#4338ca; font-size:14px; margin-bottom:8px; }}
  .info-box p {{ font-size:13px; color:#4338ca; opacity:0.8; }}

  /* Footer */
  .footer {{ text-align:center; color:#94a3b8; font-size:12px; padding:32px 0; border-top:1px solid #e2e8f0; margin-top:20px; }}

  /* Tabs — minimalist text labels separated from the panel content by an
     underline (the active tab takes the indigo accent). */
  .tabs-nav {{ display:flex; gap:24px; margin:24px 0 28px;
    border-bottom:1px solid #e2e8f0;
    position:sticky; top:0; background:#f8fafc; z-index:10; padding:0; }}
  .tab-btn {{ background:none; border:none; padding:14px 4px;
    font-size:13.5px; font-weight:600; color:#64748b; cursor:pointer;
    border-bottom:2px solid transparent; margin-bottom:-1px;
    font-family:inherit; transition:color .15s, border-color .15s;
    letter-spacing:.01em; }}
  .tab-btn:hover {{ color:#4338ca; }}
  .tab-btn.active {{ color:#4338ca; border-bottom-color:#4338ca; }}
  .tab-panel {{ display:none; }}
  .tab-panel.active {{ display:block; }}

  @media print {{
    .header {{ background:#1e1b4b !important; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    .kpi, .chart-card, .diff-card, .data-table {{ break-inside:avoid; }}
    body {{ font-size:11px; }}
  }}
  @media (max-width:700px) {{
    .kpi-row {{ grid-template-columns:repeat(2,1fr); }}
    .diff-grid {{ grid-template-columns:1fr; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <h1>Dependency Impact Report</h1>
    <div class="sub">KMP Impact Analyzer — Static dependency propagation analysis</div>
    <div class="version-pill">
      {dep_group} &nbsp;<code>{ver_before}</code>
      <span class="arrow">→</span>
      <code>{ver_after}</code>
    </div>
  </div>
</div>

<div class="container">

<!-- KPIs -->
<div class="kpi-row">
  <div class="kpi">
    <div class="num red">{summary['total_impacted_files']}</div>
    <div class="lbl">Impacted files</div>
    <div class="kpi-sub">{_kpi_ratio(summary['total_impacted_files'], summary['total_project_files'])}</div>
  </div>
  <div class="kpi">
    <div class="num amber">{summary['total_project_files']}</div>
    <div class="lbl">Total files</div>
    <div class="kpi-sub">{summary['direct_impacts']} direct · {summary['transitive_impacts']} transitive</div>
  </div>
  <div class="kpi">
    <div class="num purple">{summary['expect_actual_pairs_total']}</div>
    <div class="lbl">Expect/actual pairs</div>
    <div class="kpi-sub">{_expect_actual_caption(summary)}</div>
  </div>
  <div class="kpi">
    <div class="num blue">{summary['total_impacted_screens']}</div>
    <div class="lbl">Impacted screens</div>
    <div class="kpi-sub">{summary.get('after_screens', 0)} surfaces explored</div>
  </div>
</div>

<!-- Stack-compatibility warnings (compilation badge removed per feedback) -->
{_render_compat_warnings(summary)}

<!-- Tabs navigation -->
<div class="tabs-nav" role="tablist">
  <button class="tab-btn active" data-tab="pipeline" role="tab">Pipeline</button>
  <button class="tab-btn" data-tab="sunburst" role="tab">Source-set Sunburst</button>
  <button class="tab-btn" data-tab="gitgraph" role="tab">Dependency Graph</button>
</div>

<div class="tab-panel active" id="tab-pipeline" role="tabpanel">

<!-- Pipeline overview -->
<div class="section">
  <div class="section-header">
    <div class="phase-num">P</div>
    <div><h2>Pipeline Execution</h2><div class="desc">Summary of the 5 analysis phases</div></div>
  </div>
  <div class="pipeline">
    {pipe_steps}
  </div>
</div>

<!-- Phase 1: Shadow Build -->
<div class="section">
  <div class="section-header">
    <div class="phase-num">1</div>
    <div><h2>Shadow Build</h2><div class="desc">BEFORE and AFTER copies of the project were created, modifying the dependency version</div></div>
  </div>
  <div class="diff-grid">
    <div class="diff-card before">
      <div class="card-head">Before — libs.versions.toml</div>
      <pre>{_highlight_toml(before_toml)}</pre>
    </div>
    <div class="diff-card after">
      <div class="card-head">After — libs.versions.toml</div>
      <pre>{_highlight_toml(after_toml)}</pre>
    </div>
  </div>
</div>

<!-- Phase 2: Static Analysis -->
<div class="section">
  <div class="section-header">
    <div class="phase-num">2</div>
    <div><h2>Static Analysis — Propagation Graph</h2><div class="desc">How the change in <strong>{dep_group}</strong> propagates through the source code</div></div>
  </div>
  <div class="chart-card">
    {propagation_svg}
    <details style="margin:14px 0 0 0;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px 14px;">
      <summary style="cursor:pointer;font-size:12.5px;font-weight:700;color:#0f172a;">How to read this graph</summary>
      <div style="margin-top:10px;font-size:12.5px;line-height:1.7;color:#334155;">
        <ul style="margin:0 0 0 1.2em;padding:0;">
          <li>The <span style="color:#4338ca;font-weight:600">violet box</span> is the bumped dependency.</li>
          <li><span style="color:#dc2626;font-weight:600">Red boxes</span> are files that directly <code>import</code> a symbol from the bumped library.</li>
          <li><span style="color:#f59e0b;font-weight:600">Amber boxes</span> are files that depend transitively at distance 1 (they import a red file).</li>
          <li><span style="color:#f97316;font-weight:600">Orange boxes</span> are files at distance 2+ (further transitive hops).</li>
          <li><strong>Click any box</strong> to dim the rest of the graph and highlight only the files reached in the next column.</li>
          <li><strong>Faint lines</strong> are real propagation edges captured during BFS; selected edges become darker when a box is active.</li>
          <li><strong>Dashed amber/orange guide lines</strong> show the general direction of propagation across columns.</li>
        </ul>
      </div>
    </details>
    <div class="caption">
      Each box is a <code>.kt</code> file. Colour = relation to the bumped dependency.
      Scroll vertically when a column has many files; click a box to inspect its next-hop impact.
    </div>
  </div>
</div>

<!-- Phase 3: Dynamic Analysis -->
<div class="section">
  <div class="section-header">
    <div class="phase-num">3</div>
    <div><h2>Dynamic Analysis — UI Exploration with DroidBot</h2><div class="desc">Screen interaction flow with change-affected screens highlighted in red</div></div>
  </div>
  {dynamic_section}

  <!-- Traceability table sits below the DroidBot iframe so the same screens
       are listed with the file/relation/distance/metrics that drive the
       colouring of the UTG nodes. -->
  <div style="margin-top:24px;">
    <div style="font-size:14px;font-weight:700;color:#1e293b;margin-bottom:6px;">
      Traceability — File → Screen
    </div>
    <div style="font-size:12.5px;color:#64748b;margin-bottom:14px;">
      Each impacted file with its relation, distance to the change, metrics, and associated UI screen.
    </div>
    <div class="table-scroll">
      <table class="data-table">
        <thead>
          <tr><th>File</th><th>Relation</th><th>Dist.</th><th>RLOC</th><th>MCC</th><th>Coverage</th><th>Screen</th></tr>
        </thead>
        <tbody>
        {trace_rows}
        </tbody>
      </table>
    </div>
  </div>
</div>

{ea_section}

<!-- Phase 5: CodeCharta -->
<div class="section">
  <div class="section-header">
    <div class="phase-num">5</div>
    <div><h2>CodeCharta Visualization — 3D Impact Map</h2><div class="desc">Each file is a building: area represents lines of code, height represents complexity, and red color indicates impact</div></div>
  </div>
  {cc_iframe}
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;">
    <div style="background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;padding:14px 16px;">
      <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Area (size)</div>
      <div style="font-size:14px;font-weight:600;color:#1e293b;">rloc — Real lines of code</div>
    </div>
    <div style="background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;padding:14px 16px;">
      <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Height</div>
      <div style="font-size:14px;font-weight:600;color:#1e293b;">mcc — Cyclomatic complexity</div>
    </div>
    <div style="background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;padding:14px 16px;">
      <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Color</div>
      <div style="font-size:14px;font-weight:600;color:#1e293b;">impact_level: <span style="color:#94a3b8;">grey</span> none · <span style="color:#f59e0b;">amber</span> transitive · <span style="color:#dc2626;">red</span> direct</div>
    </div>
  </div>
</div>

</div><!-- /#tab-pipeline -->

<div class="tab-panel" id="tab-sunburst" role="tabpanel">
<div class="section">
  <div class="section-header">
    <div class="phase-num" style="background:#B91C1C;">&#9737;</div>
    <div><h2>Source-set Impact Sunburst</h2><div class="desc">Interactive ring: source-set &rarr; package &rarr; file. Click any ring to zoom; click center to zoom out.</div></div>
  </div>
  {sunburst_block}
</div>
</div><!-- /#tab-sunburst -->

<div class="tab-panel" id="tab-gitgraph" role="tabpanel">
<div class="section">
  <div class="section-header">
    <div class="phase-num" style="background:#059669;">G</div>
    <div><h2>Transitive Dependency Graph (GitGraph)</h2><div class="desc">SBOM-derived arc diagram showing every library and its dependents. Use the sidebar to filter or focus a library.</div></div>
  </div>
  {gitgraph_block}
</div>
</div><!-- /#tab-gitgraph -->

<div class="footer">
  Generated by <strong>kmp-impact-analyzer</strong><br>
  Thesis: KMP Code Contextualization and Visualization Pipeline — Universidad de los Andes
</div>

</div>
<script>
(function() {{
  var btns = document.querySelectorAll('.tab-btn');
  var panels = document.querySelectorAll('.tab-panel');
  function activate(name) {{
    btns.forEach(function(b) {{ b.classList.toggle('active', b.dataset.tab === name); }});
    panels.forEach(function(p) {{ p.classList.toggle('active', p.id === 'tab-' + name); }});
    try {{ history.replaceState(null, '', '#' + name); }} catch (e) {{}}
  }}
  btns.forEach(function(b) {{ b.addEventListener('click', function() {{ activate(b.dataset.tab); }}); }});
  var hash = (location.hash || '').replace('#', '');
  if (hash && document.getElementById('tab-' + hash)) activate(hash);
}})();
</script>
</body>
</html>"""


def generate_report_site(
    consolidated: ConsolidatedResult,
    manifest: ShadowManifest,
    output_dir: str | Path,
    report_url: str = "",
) -> dict[str, Path]:
    output_root = Path(output_dir)
    report_dir = output_root / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    summary = build_summary_payload(consolidated, manifest, report_url=report_url)
    summary_json_path = report_dir / "summary.json"
    summary_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    summary_md_path = report_dir / "summary.md"
    summary_md_path.write_text(build_summary_markdown(summary), encoding="utf-8")

    html_path = report_dir / "index.html"
    html_path.write_text(_build_html(summary, consolidated, manifest, output_root), encoding="utf-8")

    log.info(f"Generated HTML report site → {html_path}")
    return {
        "html": html_path,
        "summary_json": summary_json_path,
        "summary_md": summary_md_path,
        "report_dir": report_dir,
    }
