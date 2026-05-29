"""Render the propagation graph as a markdown tree for the PR comment.

GitHub markdown does not support inline colours, but it renders Unicode block
characters and the box-drawing set crisply, which is enough to keep the
``DEPENDENCY → DIRECT → TRANSITIVE`` story readable next to the rasterised
images. Each row is prefixed with a coloured square (``🟥`` direct, ``🟧``
transitive d1, ``🟨`` transitive d≥2, ``🟪`` expect/actual) so the reader sees
the same colour palette that the SVGs use.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ..contracts import ConsolidatedResult, ImpactRelation


_DEP_BADGE = "🟦"
_DIRECT_BADGE = "🟥"
_TRANS1_BADGE = "🟧"
_TRANS2_BADGE = "🟨"
_EA_BADGE = "🟪"


def _badge(relation: ImpactRelation, distance: int) -> str:
    if relation == ImpactRelation.DIRECT:
        return _DIRECT_BADGE
    if relation == ImpactRelation.EXPECT_ACTUAL:
        return _EA_BADGE
    return _TRANS1_BADGE if distance <= 1 else _TRANS2_BADGE


def build_propagation_tree_markdown(
    consolidated: ConsolidatedResult,
    max_per_bucket: int = 8,
) -> str:
    """Return a fenced markdown tree summarising the propagation."""
    dep = consolidated.dependency_group
    before = consolidated.version_before
    after = consolidated.version_after

    files = sorted(
        consolidated.static_impact.impacted_files,
        key=lambda fi: (
            0 if fi.relation == ImpactRelation.DIRECT else 1,
            fi.distance,
            -fi.metrics.rloc,
            fi.file_path,
        ),
    )

    direct = [fi for fi in files if fi.relation == ImpactRelation.DIRECT]
    trans1 = [fi for fi in files if fi.relation != ImpactRelation.DIRECT and fi.distance <= 1]
    trans2 = [fi for fi in files if fi.relation != ImpactRelation.DIRECT and fi.distance >= 2]
    ea = [fi for fi in files if fi.relation == ImpactRelation.EXPECT_ACTUAL]

    lines: list[str] = []
    lines.append(f"{_DEP_BADGE} **{dep}** `{before}` → `{after}` "
                 f"({consolidated.total_impacted_files}/"
                 f"{consolidated.static_impact.total_project_files} files)")
    lines.append("│")

    def emit_bucket(title: str, badge: str, bucket: list, indent_last: bool) -> None:
        if not bucket:
            return
        prefix = "└──" if indent_last else "├──"
        lines.append(f"{prefix} {badge} **{title}** ({len(bucket)})")
        connector = "    " if indent_last else "│   "
        shown = bucket[:max_per_bucket]
        for i, fi in enumerate(shown):
            leaf = "└──" if i == len(shown) - 1 and len(bucket) <= max_per_bucket else "├──"
            file_name = Path(fi.file_path).name
            lines.append(
                f"{connector}{leaf} {_badge(fi.relation, fi.distance)} `{file_name}` "
                f"· d{fi.distance} · {fi.metrics.rloc} loc"
            )
        if len(bucket) > max_per_bucket:
            lines.append(f"{connector}└── … {len(bucket) - max_per_bucket} more")

    has_trans1 = bool(trans1)
    has_trans2 = bool(trans2)
    has_ea = bool(ea)

    emit_bucket("Direct", _DIRECT_BADGE, direct, indent_last=not (has_trans1 or has_trans2 or has_ea))
    emit_bucket("Transitive (distance 1)", _TRANS1_BADGE, trans1, indent_last=not (has_trans2 or has_ea))
    emit_bucket("Transitive (distance ≥ 2)", _TRANS2_BADGE, trans2, indent_last=not has_ea)
    emit_bucket("Expect/Actual bridges", _EA_BADGE, ea, indent_last=True)

    if not (direct or trans1 or trans2 or ea):
        lines.append("└── _No files matched this dependency in the static graph_")

    return "```text\n" + "\n".join(lines) + "\n```"
