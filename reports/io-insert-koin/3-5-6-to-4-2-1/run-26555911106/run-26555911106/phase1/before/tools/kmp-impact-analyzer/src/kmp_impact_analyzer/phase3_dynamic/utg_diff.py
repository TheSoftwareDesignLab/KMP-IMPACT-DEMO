"""Compare two UTGs to find screen-level differences.

Diffing now operates on the *view structure id* rather than the Activity class
name. For Compose single-Activity apps that means we no longer collapse every
screen into one node, and additions/removals/changed transitions are detected
per screen.
"""

from __future__ import annotations

from collections import defaultdict

from ..contracts import ScreenDiff, UTGGraph


def _index_by_structure(utg: UTGGraph) -> dict[str, list]:
    grouped: dict[str, list] = defaultdict(list)
    for node in utg.nodes:
        key = node.structure_id or node.state_id
        if not key:
            continue
        grouped[key].append(node)
    return grouped


def _representative_name(nodes: list) -> str:
    """Choose the nicest name for a structure cluster."""
    if not nodes:
        return ""
    # Prefer entries with a non-fallback title (no '#hash' suffix).
    titled = [n for n in nodes if "#" not in (n.screen_name or "")]
    chosen = titled[0] if titled else nodes[0]
    return chosen.screen_name or chosen.activity or "screen"


def _outgoing_actions(utg: UTGGraph, state_ids: set[str]) -> set[tuple[str, str]]:
    by_id = {n.state_id: (n.structure_id or n.state_id) for n in utg.nodes}
    edges: set[tuple[str, str]] = set()
    for edge in utg.edges:
        if edge.source in state_ids:
            edges.add((edge.action, by_id.get(edge.target, edge.target)))
    return edges


def compare_utgs(before: UTGGraph, after: UTGGraph) -> list[ScreenDiff]:
    """Compare BEFORE/AFTER UTGs and return per-screen differences."""
    before_groups = _index_by_structure(before)
    after_groups = _index_by_structure(after)

    diffs: list[ScreenDiff] = []
    seen_keys = sorted(set(before_groups) | set(after_groups))

    for key in seen_keys:
        b_nodes = before_groups.get(key, [])
        a_nodes = after_groups.get(key, [])
        name = _representative_name(a_nodes or b_nodes)

        if b_nodes and not a_nodes:
            diffs.append(
                ScreenDiff(
                    screen_name=name,
                    status="missing",
                    details=f"Screen '{name}' present in before but missing after",
                )
            )
            continue
        if a_nodes and not b_nodes:
            diffs.append(
                ScreenDiff(
                    screen_name=name,
                    status="new",
                    details=f"Screen '{name}' is new in the after version",
                )
            )
            continue

        b_ids = {n.state_id for n in b_nodes}
        a_ids = {n.state_id for n in a_nodes}
        b_edges = _outgoing_actions(before, b_ids)
        a_edges = _outgoing_actions(after, a_ids)
        if b_edges != a_edges:
            diffs.append(
                ScreenDiff(
                    screen_name=name,
                    status="changed",
                    details=(
                        f"Screen '{name}' has different transitions: "
                        f"before={len(b_edges)}, after={len(a_edges)}"
                    ),
                )
            )

    return diffs
