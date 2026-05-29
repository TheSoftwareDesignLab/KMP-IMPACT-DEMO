"""Decorate the *original* DroidBot UTG HTML with relation-coloured borders.

Earlier iterations replaced DroidBot's HTML with a custom Cytoscape viewer.
That fixed the colours but lost DroidBot's signature feature: every node
displays a real screenshot of the corresponding Android screen. Reviewers
asked us to keep the original viewer 100%, so this module instead patches
DroidBot's stock ``index.html`` in place by appending a script that runs
once vis.js has finished initialising.

DroidBot's stock viewer renders the UI Transition Graph with **vis.js**
(``vis.Network`` exposed as the global ``network``), not Cytoscape, so the
script targets the vis.js DataSet API:

1. ``network.body.data.nodes.update([...])`` reapplies per-node ``color`` and
   ``borderWidth`` overrides; vis.js merges them into the existing config so
   the screenshot inside each node stays intact.
2. We poll for ``network`` for up to ~15 s because vis.js bootstraps inside
   ``body onload="draw()"`` and may run after our script.

The same script is also evaluated by Playwright before taking the PR-comment
screenshot, so the rasterised image always shows the borders even when the
iframe coloring is racy in a particular browser.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..contracts import ConsolidatedResult, ImpactRelation
from ..utils.log import get_logger

log = get_logger(__name__)


_RELATION_PRIORITY = {
    ImpactRelation.DIRECT: 3,
    ImpactRelation.EXPECT_ACTUAL: 2,
    ImpactRelation.TRANSITIVE: 1,
}


def build_relation_map(consolidated: ConsolidatedResult) -> dict[str, str]:
    """Map lowercased screen-name (or activity-fragment) -> worst relation.

    The keys are matched as substrings against each UTG node's label,
    activity, foreground_activity and content fields. Highest severity wins
    when the same key receives several relations across the trace.

    In addition to ``screen_name`` from the static mapper we also feed in
    ``screen_name`` from any dynamic ``ScreenDiff`` so that screens that are
    only visible at runtime (e.g. error states, deep links) still receive a
    coloured border. Diff-only screens fall back to TRANSITIVE because they
    are evidence of behaviour change without a static-graph anchor.
    """
    out: dict[str, str] = {}

    def _bump(key: str, relation: ImpactRelation) -> None:
        key = (key or "").strip().lower()
        if not key or len(key) < 3:
            return
        current = out.get(key)
        if current is None or _RELATION_PRIORITY[relation] > _RELATION_PRIORITY[
            ImpactRelation(current)
        ]:
            out[key] = relation.value

    for entry in consolidated.trace:
        for screen in entry.screens:
            _bump(screen, entry.relation)

    # Dynamic-only screens (regression diffs that did not match a static file)
    # still belong on the UTG with at least a transitive border so the user
    # can spot them.
    dynamic = consolidated.dynamic_regressions
    if dynamic and dynamic.diffs:
        for diff in dynamic.diffs:
            _bump(diff.screen_name, ImpactRelation.TRANSITIVE)

    return out


# Public so screenshots.py can run the same logic via page.evaluate().
DECORATE_JS_TEMPLATE = r"""
(function () {
  const RELATION_MAP = __RELATION_JSON__;
  const COLOURS = {
    direct: '#dc2626',
    transitive: '#f59e0b',
    expect_actual: '#7c3aed',
  };
  const SEVERITY = { direct: 3, expect_actual: 2, transitive: 1 };

  function pickRelation(text) {
    const haystack = (text || '').toString().toLowerCase();
    if (!haystack) return null;
    let best = null;
    for (const name of Object.keys(RELATION_MAP)) {
      if (name.length < 3) continue;
      if (haystack.indexOf(name) === -1) continue;
      const rel = RELATION_MAP[name];
      if (!best || SEVERITY[rel] > SEVERITY[best]) best = rel;
    }
    return best;
  }

  function nodeHaystack(node) {
    if (!node) return '';
    return [
      node.label, node.id, node.title,
      node.activity, node.foreground_activity,
      node.name, node.content
    ].filter(Boolean).join(' ');
  }

  function applyDecoration() {
    // The DroidBot viewer uses vis.js: `network = new vis.Network(...)` and
    // `utg.nodes` is the raw payload. We need both to update node styles.
    if (typeof network === 'undefined' || !network || !network.body) return false;
    if (typeof utg === 'undefined' || !utg || !utg.nodes) return false;
    if (!network.body.data || !network.body.data.nodes) return false;

    const updates = [];
    let coloured = 0, total = 0;
    utg.nodes.forEach(function (node) {
      total++;
      const rel = pickRelation(nodeHaystack(node));
      if (!rel) return;
      coloured++;
      updates.push({
        id: node.id,
        borderWidth: 8,
        borderWidthSelected: 8,
        color: {
          border: COLOURS[rel],
          background: '#FFFFFF',
          highlight: { border: COLOURS[rel], background: '#FFFFFF' },
          hover:     { border: COLOURS[rel], background: '#FFFFFF' }
        },
        shapeProperties: { useBorderWithImage: true }
      });
    });

    try {
      if (updates.length) {
        network.body.data.nodes.update(updates);
        if (typeof network.redraw === 'function') network.redraw();
      }
      console.log('[impact-decorator] coloured', coloured, '/', total, 'nodes');
      return coloured > 0 || total > 0;  // success if we processed any node
    } catch (e) {
      console.warn('[impact-decorator] failed:', e);
      return false;
    }
  }

  function whenReady() {
    let attempts = 0;
    function tick() {
      attempts++;
      if (applyDecoration()) return;
      if (attempts < 60) setTimeout(tick, 250);  // ~15 s budget
    }
    tick();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', whenReady);
  } else {
    // body onload="draw()" runs after DOMContentLoaded, so always poll.
    whenReady();
  }
  window.__impactDecorate = applyDecoration;
})();
"""


_LEGEND_HTML = r"""
<style>
  #impact-legend {
    position: fixed; right: 18px; bottom: 18px; z-index: 9999;
    background: rgba(13,17,23,0.92); color: #e6edf3;
    padding: 12px 16px; border-radius: 10px;
    font: 12px/1.55 -apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif;
    border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.32);
  }
  #impact-legend .title { font-size: 10px; letter-spacing: 1.5px;
    text-transform: uppercase; color: #7d8590; margin-bottom: 6px; }
  #impact-legend .row { display: flex; align-items: center; gap: 9px; padding: 1px 0; }
  #impact-legend .sw { width: 14px; height: 14px; border-radius: 50%;
    background: transparent; border: 3px solid currentColor; }
</style>
<div id="impact-legend">
  <div class="title">Impact relation</div>
  <div class="row" style="color:#dc2626"><span class="sw"></span><span>Direct</span></div>
  <div class="row" style="color:#f59e0b"><span class="sw"></span><span>Transitive</span></div>
  <div class="row" style="color:#7c3aed"><span class="sw"></span><span>Expect/Actual</span></div>
  <div class="row" style="color:#475569"><span class="sw"></span><span>No impact</span></div>
</div>
"""


def colorize_droidbot_html(
    impact_utg_dir: Path,
    consolidated: ConsolidatedResult,
) -> bool:
    """Append our decorate script to ``impact_utg_dir/index.html`` in place.

    Idempotent — if the script is already present, the file is left alone.
    """
    html_path = impact_utg_dir / "index.html"
    if not html_path.exists():
        return False
    relation_map = build_relation_map(consolidated)
    if not relation_map:
        log.info("No impacted screens to colour — skipping UTG decoration")
        return False

    original = html_path.read_text(encoding="utf-8", errors="replace")
    if "[impact-decorator]" in original:
        return True

    script = "<script>" + DECORATE_JS_TEMPLATE.replace(
        "__RELATION_JSON__", json.dumps(relation_map, ensure_ascii=False)
    ) + "</script>"
    snippet = _LEGEND_HTML + script
    if "</body>" in original:
        patched = original.replace("</body>", snippet + "</body>", 1)
    else:
        patched = original + snippet
    html_path.write_text(patched, encoding="utf-8")
    log.info(f"Decorated DroidBot UTG with {len(relation_map)} relation entries")
    return True


def build_decorate_js(consolidated: ConsolidatedResult) -> str:
    """Same script Playwright runs via page.evaluate to colour the screenshot."""
    relation_map = build_relation_map(consolidated)
    return DECORATE_JS_TEMPLATE.replace(
        "__RELATION_JSON__", json.dumps(relation_map, ensure_ascii=False)
    )
