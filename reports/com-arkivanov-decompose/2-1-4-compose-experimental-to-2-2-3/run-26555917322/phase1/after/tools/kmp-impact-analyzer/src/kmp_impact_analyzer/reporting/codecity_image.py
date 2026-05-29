"""Render a 2D treemap "city" view of the impact graph for the PR comment.

The full CodeCharta city is WebGL and cannot be rasterised inside a CI runner.
For the PR comment we generate a flat treemap that uses the same metric
encoding (area = RLOC, height/intensity proxied by colour) and the same
three-level palette as the embedded 3D viewer (no impact / transitive / direct),
so the dependency-impact intuition transfers.
"""

from __future__ import annotations

import html
import math
from collections import defaultdict
from pathlib import Path

from ..contracts import ConsolidatedResult, ImpactRelation


_PALETTE = {
    "direct": "#dc2626",
    "transitive": "#f59e0b",
    "ea": "#7c3aed",
    "none": "#e2e8f0",
}


def _classify(relation: ImpactRelation | None) -> str:
    if relation == ImpactRelation.DIRECT:
        return "direct"
    if relation == ImpactRelation.TRANSITIVE:
        return "transitive"
    if relation == ImpactRelation.EXPECT_ACTUAL:
        return "ea"
    return "none"


def _source_set(file_path: str) -> str:
    p = file_path.replace("\\", "/")
    for marker in ("commonMain", "androidMain", "iosMain", "jvmMain", "desktopMain", "wasmMain", "jsMain", "commonTest"):
        if f"/{marker}/" in p or p.endswith(f"/{marker}"):
            return marker
    return "other"


def _short_name(file_path: str, limit: int = 18) -> str:
    name = Path(file_path).name
    if len(name) <= limit:
        return name
    return name[: limit - 1] + "…"


# ---------------------------------------------------------------------------
# Squarified treemap layout (Bruls et al., 2000)
# ---------------------------------------------------------------------------

def _squarify(items: list[tuple[float, dict]], x: float, y: float, w: float, h: float) -> list[dict]:
    """Layout `items` (sorted desc by area) into rectangles inside (x, y, w, h)."""
    items = [it for it in items if it[0] > 0]
    if not items:
        return []
    total = sum(area for area, _ in items)
    if total <= 0:
        return []
    # Scale areas to the available pixel area.
    scale = (w * h) / total
    scaled = [(area * scale, payload) for area, payload in items]
    return _layout(scaled, x, y, w, h)


def _layout(items: list[tuple[float, dict]], x: float, y: float, w: float, h: float) -> list[dict]:
    rects: list[dict] = []
    while items:
        row, remaining = _build_row(items, min(w, h))
        rects.extend(_emit_row(row, x, y, w, h))
        used = sum(area for area, _ in row) / min(w, h) if min(w, h) > 0 else 0
        if w >= h:
            x += used
            w -= used
        else:
            y += used
            h -= used
        items = remaining
        if not items or w <= 0 or h <= 0:
            break
    return rects


def _build_row(items: list[tuple[float, dict]], side: float) -> tuple[list[tuple[float, dict]], list[tuple[float, dict]]]:
    row: list[tuple[float, dict]] = []
    best_ratio = float("inf")
    for i, item in enumerate(items):
        candidate = row + [item]
        ratio = _worst_ratio(candidate, side)
        if ratio > best_ratio:
            return row, items[i:]
        row = candidate
        best_ratio = ratio
    return row, []


def _worst_ratio(row: list[tuple[float, dict]], side: float) -> float:
    if not row or side <= 0:
        return float("inf")
    s = sum(area for area, _ in row)
    if s <= 0:
        return float("inf")
    a_max = max(area for area, _ in row)
    a_min = min(area for area, _ in row)
    return max((side * side * a_max) / (s * s), (s * s) / (side * side * a_min))


def _emit_row(row: list[tuple[float, dict]], x: float, y: float, w: float, h: float) -> list[dict]:
    if not row:
        return []
    s = sum(area for area, _ in row)
    if s <= 0 or w <= 0 or h <= 0:
        return []
    rects: list[dict] = []
    if w >= h:
        col_w = s / h
        cy = y
        for area, payload in row:
            rh = area / col_w if col_w else 0
            rects.append({"x": x, "y": cy, "w": col_w, "h": rh, "payload": payload})
            cy += rh
    else:
        row_h = s / w
        cx = x
        for area, payload in row:
            rw = area / row_h if row_h else 0
            rects.append({"x": cx, "y": y, "w": rw, "h": row_h, "payload": payload})
            cx += rw
    return rects


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_codecity_svg(consolidated: ConsolidatedResult, width: int = 880, height: int = 540) -> str:
    """Return an SVG treemap of all impacted (and a sample of non-impacted) files."""
    impacted_lookup = {fi.file_path: fi for fi in consolidated.static_impact.impacted_files}

    # Group by source set.
    groups: dict[str, list[tuple[float, dict]]] = defaultdict(list)
    for fi in consolidated.static_impact.impacted_files:
        area = math.sqrt(max(fi.metrics.rloc, 1)) ** 2  # RLOC area
        groups[_source_set(fi.file_path)].append(
            (
                area,
                {
                    "name": _short_name(fi.file_path),
                    "klass": _classify(fi.relation),
                    "rloc": fi.metrics.rloc,
                    "mcc": fi.metrics.mcc,
                    "tooltip": fi.file_path,
                },
            )
        )

    # If no impacted files, fall back to a placeholder.
    if not groups:
        return _empty_svg("No impacted files to draw")

    # Layout source sets as horizontal bands proportional to total impact.
    set_totals = {k: sum(area for area, _ in v) for k, v in groups.items()}
    grand = sum(set_totals.values()) or 1.0

    title_h = 36
    legend_h = 36
    canvas_top = title_h
    canvas_bottom = height - legend_h
    canvas_h = canvas_bottom - canvas_top
    parts: list[str] = []
    parts.append(
        f"<svg viewBox='0 0 {width} {height}' xmlns='http://www.w3.org/2000/svg' "
        "style='width:100%;font-family:Inter,system-ui,sans-serif;background:#ffffff;'>"
    )
    parts.append(
        f"<text x='{width // 2}' y='22' text-anchor='middle' fill='#1e293b' font-size='13' "
        f"font-weight='700'>Code city — area = RLOC, colour = impact level</text>"
    )

    # Vertical bands per source set.
    cursor_y = canvas_top
    for source_set in sorted(set_totals, key=lambda k: -set_totals[k]):
        portion = set_totals[source_set] / grand
        band_h = max(60.0, canvas_h * portion)
        if cursor_y + band_h > canvas_bottom:
            band_h = canvas_bottom - cursor_y
        if band_h <= 0:
            break
        parts.append(
            f"<rect x='2' y='{cursor_y:.1f}' width='{width - 4}' height='{band_h:.1f}' "
            "fill='#f8fafc' stroke='#e2e8f0' stroke-width='1'/>"
        )
        parts.append(
            f"<text x='14' y='{cursor_y + 16:.1f}' fill='#475569' font-size='11' "
            f"font-weight='700' text-transform='uppercase'>{html.escape(source_set)} "
            f"({len(groups[source_set])} files)</text>"
        )
        items = sorted(groups[source_set], key=lambda it: -it[0])
        rects = _squarify(items, x=8.0, y=cursor_y + 24.0, w=float(width - 16), h=band_h - 32.0)
        for r in rects:
            payload = r["payload"]
            colour = _PALETTE[payload["klass"]]
            parts.append(
                f"<rect x='{r['x']:.1f}' y='{r['y']:.1f}' width='{r['w']:.1f}' "
                f"height='{r['h']:.1f}' fill='{colour}' stroke='white' stroke-width='1.5'/>"
            )
            if r["w"] > 60 and r["h"] > 18:
                cx = r["x"] + r["w"] / 2
                cy = r["y"] + r["h"] / 2 + 3
                parts.append(
                    f"<text x='{cx:.1f}' y='{cy:.1f}' text-anchor='middle' "
                    f"fill='white' font-size='10' font-weight='600'>"
                    f"{html.escape(payload['name'])}</text>"
                )
        cursor_y += band_h

    # Legend.
    ly = height - 14
    legend_items = [
        ("Direct", _PALETTE["direct"]),
        ("Transitive", _PALETTE["transitive"]),
        ("Expect/Actual", _PALETTE["ea"]),
    ]
    for i, (label, colour) in enumerate(legend_items):
        x = 24 + i * 200
        parts.append(
            f"<rect x='{x}' y='{ly - 12}' width='14' height='14' fill='{colour}' rx='2'/>"
        )
        parts.append(
            f"<text x='{x + 22}' y='{ly}' fill='#475569' font-size='12' font-weight='600'>"
            f"{html.escape(label)}</text>"
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
