"""Render the UTG into an SVG decorated with static-impact colours.

The DroidBot HTML viewer paints nodes inside a Cytoscape canvas, so DOM/CSS
overlays cannot recolour them reliably. Instead, we render our own SVG view of
the UTG using a simple BFS hierarchical layout. Each node's border is coloured
by whichever static-impact relation we can match (Direct → red, Transitive →
amber, Expect/Actual → purple), giving a single picture that ties the dynamic
graph to the static analysis.
"""

from __future__ import annotations

import html
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from ..contracts import ConsolidatedResult, ImpactRelation


_RELATION_BORDER = {
    ImpactRelation.DIRECT: "#dc2626",
    ImpactRelation.TRANSITIVE: "#f59e0b",
    ImpactRelation.EXPECT_ACTUAL: "#7c3aed",
}
_NEUTRAL_BORDER = "#94a3b8"


def _load_utg(droidbot_dir: Path) -> dict[str, Any] | None:
    for name in ("utg.js", "utg.json"):
        path = droidbot_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if text.lstrip().startswith("var "):
            text = text[text.index("=") + 1 :].strip().rstrip(";")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            continue
    return None


def _build_impacted_screen_lookup(
    consolidated: ConsolidatedResult,
) -> dict[str, ImpactRelation]:
    """Map lowercased screen-name → worst relation."""
    lookup: dict[str, ImpactRelation] = {}
    severity = {
        ImpactRelation.DIRECT: 3,
        ImpactRelation.EXPECT_ACTUAL: 2,
        ImpactRelation.TRANSITIVE: 1,
    }
    for entry in consolidated.trace:
        for screen in entry.screens:
            key = screen.lower()
            current = lookup.get(key)
            if current is None or severity[entry.relation] > severity[current]:
                lookup[key] = entry.relation
    return lookup


def _node_relation(
    node_label: str,
    node_activity: str,
    node_text: str,
    impacted: dict[str, ImpactRelation],
) -> ImpactRelation | None:
    """Best-effort: match a UTG node to an impacted screen by substring lookup."""
    haystack = " ".join(filter(None, (node_label, node_activity, node_text))).lower()
    if not haystack:
        return None
    matched: ImpactRelation | None = None
    severity = {
        ImpactRelation.DIRECT: 3,
        ImpactRelation.EXPECT_ACTUAL: 2,
        ImpactRelation.TRANSITIVE: 1,
    }
    for screen_lower, relation in impacted.items():
        if not screen_lower or len(screen_lower) < 3:
            continue
        if screen_lower in haystack:
            if matched is None or severity[relation] > severity[matched]:
                matched = relation
    return matched


def _bfs_levels(
    nodes: list[dict[str, Any]], edges: list[dict[str, Any]]
) -> dict[str, int]:
    """Assign a hierarchical level (distance from the launch state) to each node."""
    if not nodes:
        return {}
    adjacency: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        src = str(e.get("from", ""))
        dst = str(e.get("to", ""))
        if src and dst:
            adjacency[src].append(dst)

    initial = str(nodes[0].get("id", nodes[0].get("state_str", "")))
    levels: dict[str, int] = {initial: 0}
    queue: deque[str] = deque([initial])
    while queue:
        current = queue.popleft()
        for nxt in adjacency.get(current, []):
            if nxt not in levels:
                levels[nxt] = levels[current] + 1
                queue.append(nxt)
    # Anything DroidBot logged but never reached from the initial state goes
    # into a separate column at the right.
    for n in nodes:
        node_id = str(n.get("id", n.get("state_str", "")))
        levels.setdefault(node_id, max(levels.values(), default=0) + 1)
    return levels


def build_utg_svg(
    consolidated: ConsolidatedResult,
    droidbot_dir: Path,
    width: int = 880,
) -> str:
    """Return an SVG visualization of the UTG with impact-coloured borders."""
    payload = _load_utg(droidbot_dir)
    if not payload:
        return _empty_svg("No UTG data available")

    raw_nodes = [n for n in payload.get("nodes", []) if isinstance(n, dict)]
    raw_edges = [e for e in payload.get("edges", []) if isinstance(e, dict)]
    if not raw_nodes:
        return _empty_svg("UTG is empty")

    impacted_screens = _build_impacted_screen_lookup(consolidated)

    levels = _bfs_levels(raw_nodes, raw_edges)
    max_level = max(levels.values()) if levels else 0
    nodes_per_level: dict[int, list[str]] = defaultdict(list)
    for node in raw_nodes:
        node_id = str(node.get("id", node.get("state_str", "")))
        lvl = levels.get(node_id, 0)
        nodes_per_level[lvl].append(node_id)

    col_w = max(160, width // max(max_level + 1, 1))
    radius = 28
    row_gap = 90
    max_col = max((len(v) for v in nodes_per_level.values()), default=1)
    height = max(280, row_gap * max_col + 80)

    pos: dict[str, tuple[int, int]] = {}
    for lvl, ids in nodes_per_level.items():
        x = 80 + lvl * col_w
        spacing = (height - 80) / max(len(ids), 1)
        for i, node_id in enumerate(ids):
            y = 60 + int(spacing * (i + 0.5))
            pos[node_id] = (x, y)

    # Decorate nodes with relation derived from screen-name overlap.
    decorated_borders: dict[str, str] = {}
    decorated_relations: dict[str, ImpactRelation] = {}
    for node in raw_nodes:
        node_id = str(node.get("id", node.get("state_str", "")))
        label = str(node.get("label", "")).strip()
        activity = str(node.get("activity", node.get("foreground_activity", "")))
        # Pull text from views to widen substring matching.
        views = node.get("views") or []
        view_texts = " ".join(
            str(v.get("text", "")) for v in views if isinstance(v, dict)
        )
        relation = _node_relation(label, activity, view_texts, impacted_screens)
        decorated_borders[node_id] = (
            _RELATION_BORDER.get(relation, _NEUTRAL_BORDER) if relation else _NEUTRAL_BORDER
        )
        if relation:
            decorated_relations[node_id] = relation

    parts: list[str] = []
    parts.append(
        f"<svg viewBox='0 0 {width} {height}' xmlns='http://www.w3.org/2000/svg' "
        "style='width:100%;font-family:Inter,system-ui,sans-serif;background:#fafafa'>"
    )

    # Edges (drawn first so nodes paint over them).
    for e in raw_edges:
        src = str(e.get("from", ""))
        dst = str(e.get("to", ""))
        if src in pos and dst in pos:
            x1, y1 = pos[src]
            x2, y2 = pos[dst]
            parts.append(
                f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' "
                "stroke='#cbd5e1' stroke-width='1' opacity='0.55'/>"
            )

    # Nodes.
    for node in raw_nodes:
        node_id = str(node.get("id", node.get("state_str", "")))
        if node_id not in pos:
            continue
        x, y = pos[node_id]
        border = decorated_borders.get(node_id, _NEUTRAL_BORDER)
        relation = decorated_relations.get(node_id)
        fill = "#fff7f7" if relation == ImpactRelation.DIRECT else (
            "#fffbeb" if relation == ImpactRelation.TRANSITIVE else (
                "#f5f3ff" if relation == ImpactRelation.EXPECT_ACTUAL else "white"
            )
        )
        stroke_w = 4 if relation else 2
        label = str(node.get("label", "")).strip() or "screen"
        short_label = label[:14] + ("…" if len(label) > 14 else "")
        parts.append(
            f"<circle cx='{x}' cy='{y}' r='{radius}' fill='{fill}' "
            f"stroke='{border}' stroke-width='{stroke_w}'/>"
        )
        parts.append(
            f"<text x='{x}' y='{y + radius + 14}' text-anchor='middle' fill='#334155' "
            f"font-size='11' font-weight='600'>{html.escape(short_label)}</text>"
        )

    # Legend.
    legend_x = 24
    legend_y = height - 30
    legend_items = [
        ("Direct", _RELATION_BORDER[ImpactRelation.DIRECT]),
        ("Transitive", _RELATION_BORDER[ImpactRelation.TRANSITIVE]),
        ("Expect/Actual", _RELATION_BORDER[ImpactRelation.EXPECT_ACTUAL]),
        ("Not impacted", _NEUTRAL_BORDER),
    ]
    for i, (label, color) in enumerate(legend_items):
        cx = legend_x + i * 170
        parts.append(
            f"<circle cx='{cx}' cy='{legend_y}' r='7' fill='white' stroke='{color}' "
            "stroke-width='3'/>"
        )
        parts.append(
            f"<text x='{cx + 14}' y='{legend_y + 4}' fill='#475569' font-size='11' "
            f"font-weight='600'>{html.escape(label)}</text>"
        )

    parts.append("</svg>")
    return "\n".join(parts)


def _empty_svg(message: str) -> str:
    return (
        "<svg viewBox='0 0 600 200' xmlns='http://www.w3.org/2000/svg' "
        "style='width:100%;font-family:Inter,system-ui,sans-serif;background:#f8fafc;'>"
        f"<text x='300' y='105' text-anchor='middle' fill='#94a3b8' "
        f"font-size='14'>{html.escape(message)}</text></svg>"
    )
