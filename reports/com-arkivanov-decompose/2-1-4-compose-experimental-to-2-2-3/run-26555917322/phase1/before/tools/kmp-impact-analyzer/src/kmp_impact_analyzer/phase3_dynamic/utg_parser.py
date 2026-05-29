"""Parse DroidBot UTG (UI Transition Graph) output.

DroidBot's ``utg.js`` represents each visited screen as a node identified by a
``state_str`` hash. The legacy parser used the Activity class name to label every
node, which collapses every Compose state into a single screen because Compose
apps run on a single Activity. This parser instead derives a stable screen
identity from the **view structure** (``structure_str``) and the visible text in
the dump, so a single-Activity app yields one screen per unique UI surface.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from ..contracts import UTGEdge, UTGGraph, UTGNode
from ..utils.log import get_logger

log = get_logger(__name__)


_NON_WORD = re.compile(r"[^A-Za-z0-9]+")


def _short_activity(activity: str) -> str:
    if not activity:
        return ""
    parts = activity.rsplit(".", 1)
    name = parts[-1] if len(parts) > 1 else activity
    return name.replace("Activity", "").replace("Fragment", "") or name


def _short_hash(value: str, length: int = 6) -> str:
    if not value:
        return ""
    return hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:length]


def _looks_like_title(text: str) -> bool:
    """Heuristic: short, mostly alphabetic, starts with a capital letter."""
    if not text:
        return False
    text = text.strip()
    if not text or len(text) > 40:
        return False
    if text.lower() in {"loading", "ok", "cancel", "back", "yes", "no"}:
        return False
    if not any(ch.isalpha() for ch in text):
        return False
    return text[0].isupper() or text.isupper()


def _extract_title_hint(node_data: dict[str, Any]) -> str:
    """Best-effort screen title from the views dump captured by DroidBot."""
    views = node_data.get("views") or []
    candidates: list[str] = []
    for v in views:
        if not isinstance(v, dict):
            continue
        text = (v.get("text") or "").strip()
        cdesc = (v.get("content_description") or v.get("content_desc") or "").strip()
        for s in (text, cdesc):
            if _looks_like_title(s):
                candidates.append(s)
    # Prefer the shortest meaningful title — usually the top-app-bar caption.
    candidates.sort(key=lambda s: (len(s), s))
    return candidates[0] if candidates else ""


def _structure_id(node_data: dict[str, Any]) -> str:
    """Stable identifier for the view-tree shape of a screen."""
    structure = node_data.get("structure_str")
    if structure:
        return _short_hash(str(structure), length=8)
    # Fallback: hash the bag of view classes when DroidBot omitted structure_str.
    views = node_data.get("views") or []
    if isinstance(views, list):
        bag = sorted(
            ((v.get("class") or "") + ":" + (v.get("resource_id") or ""))
            for v in views
            if isinstance(v, dict)
        )
        if bag:
            return _short_hash("|".join(bag), length=8)
    return _short_hash(node_data.get("state_str", ""), length=8)


def _build_screen_name(activity: str, title_hint: str, structure: str) -> str:
    """Friendly base name for a UTG state. Sequential numbering happens in the
    parser so duplicate Activities become ``Main #1``/``Main #2`` instead of
    the opaque hash suffix that earlier versions emitted."""
    short = _short_activity(activity) or "Screen"
    if title_hint:
        slug = _NON_WORD.sub(" ", title_hint).strip()
        return f"{short} · {slug[:32]}" if slug else short
    return short


def _load_utg_payload(droidbot_output_dir: Path) -> dict[str, Any] | None:
    candidates = [
        droidbot_output_dir / "utg.js",
        droidbot_output_dir / "utg.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if content.lstrip().startswith("var "):
            eq_idx = content.index("=")
            content = content[eq_idx + 1 :].strip().rstrip(";")
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            log.error(f"Failed to parse {path}: {e}")
    return None


def parse_utg(droidbot_output_dir: Path) -> UTGGraph:
    """Parse the UTG from a DroidBot output directory."""
    data = _load_utg_payload(droidbot_output_dir)
    if data is None:
        log.warning(f"No UTG file found in {droidbot_output_dir}")
        return UTGGraph()

    nodes: list[UTGNode] = []
    edges: list[UTGEdge] = []

    raw_nodes = data.get("nodes", [])
    initial_state_id = ""
    if raw_nodes:
        # DroidBot marks the first node with id === state_str of the launch screen.
        first = raw_nodes[0]
        if isinstance(first, dict):
            initial_state_id = str(first.get("id", first.get("state_str", "")))

    # Sequential counter per activity — same structure_id always gets the
    # same screen name across the file so the diff stage can match them up.
    activity_counter: dict[str, int] = {}
    structure_to_name: dict[str, str] = {}

    for node_data in raw_nodes:
        if not isinstance(node_data, dict):
            continue
        activity = node_data.get("activity") or node_data.get("foreground_activity") or ""
        state_str = str(node_data.get("state_str", ""))
        state_id = str(node_data.get("id", state_str))
        structure = _structure_id(node_data)
        title_hint = _extract_title_hint(node_data)

        if structure in structure_to_name:
            screen_name = structure_to_name[structure]
        else:
            base = _build_screen_name(activity, title_hint, structure)
            if title_hint:
                screen_name = base
            else:
                count = activity_counter.get(base, 0) + 1
                activity_counter[base] = count
                screen_name = base if count == 1 else f"{base} #{count}"
            structure_to_name[structure] = screen_name

        nodes.append(
            UTGNode(
                state_id=state_id,
                activity=activity,
                state_str=state_str,
                screen_name=screen_name,
                structure_id=structure,
                title_hint=title_hint,
                is_initial=(state_id == initial_state_id and bool(state_id)),
            )
        )

    for edge_data in data.get("edges", []):
        if not isinstance(edge_data, dict):
            continue
        edges.append(
            UTGEdge(
                source=str(edge_data.get("from", "")),
                target=str(edge_data.get("to", "")),
                action=str(edge_data.get("label", edge_data.get("action", ""))),
            )
        )

    log.info(f"Parsed UTG: {len(nodes)} nodes, {len(edges)} edges")
    return UTGGraph(nodes=nodes, edges=edges)
