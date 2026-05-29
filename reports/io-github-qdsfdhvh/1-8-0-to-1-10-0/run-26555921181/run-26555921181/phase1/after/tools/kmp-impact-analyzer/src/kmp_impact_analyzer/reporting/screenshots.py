"""Headless screenshots of the live report viewers.

Captures three PNGs that the PR comment embeds:

* **DroidBot UTG** — DroidBot's own ``index.html`` (so each node still shows
  the real Android screenshot). We evaluate the impact-decorator JS via
  ``page.evaluate`` *before* taking the snapshot, which guarantees the
  rasterised image has the relation-coloured borders even if the iframe's
  inline script is racy in some browsers.
* **CodeCharta city** — official viewer if bundled, otherwise skipped (the
  PR comment then falls back to the cairosvg-rendered code city).
* **Sunburst** — the report's own sunburst tab. We click the tab through JS
  so the panel is visible before we screenshot.

Crucially, we check that each target HTML actually exists before navigating.
Without that check, Playwright would screenshot Python's ``http.server`` 404
page and embed *that* as the PR-comment image.
"""

from __future__ import annotations

import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

from ..contracts import ConsolidatedResult
from .utg_decorate import build_decorate_js


def _start_static_server(root: Path) -> tuple[socketserver.TCPServer, int]:
    """Serve `root` over HTTP on a free ephemeral port.

    The previous implementation built a subclass via ``type(...)`` with a
    class-level ``directory`` attribute, which is silently ignored by
    ``SimpleHTTPRequestHandler``: that class accepts ``directory`` only as a
    constructor keyword. The result was a server that served from the
    current working directory instead of the requested root, so every URL
    inside the report tree returned a 404 page — and Playwright happily
    rasterised that 404 page into the PR-comment images. We use
    ``functools.partial`` here so the directory is bound to the actual
    handler ``__init__`` and the document root is correct.
    """
    handler_cls = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(root)
    )
    server = socketserver.TCPServer(("127.0.0.1", 0), handler_cls)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


def _file_exists(site_root: Path, relative: str) -> bool:
    rel = relative.split("?", 1)[0].split("#", 1)[0]
    return (site_root / rel).exists()


def _screenshot(
    page,
    url: str,
    settle_ms: int,
    out_path: Path,
    pre_screenshot_js: str | None = None,
) -> bool:
    try:
        page.goto(url, wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(settle_ms)
        if pre_screenshot_js:
            try:
                page.evaluate(pre_screenshot_js)
                # Re-trigger the same logic in case the original ran before
                # cytoscape was ready.
                page.evaluate("if (window.__impactDecorate) window.__impactDecorate()")
                page.wait_for_timeout(900)
            except Exception as e:  # noqa: BLE001
                print(f"[screenshots] pre-screenshot eval warned: {e}")
        page.screenshot(path=str(out_path), full_page=False)
        size = out_path.stat().st_size
        print(f"[screenshots] OK {out_path.name} ({size} bytes)")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"[screenshots] FAIL {out_path.name}: {e}")
        try:
            out_path.unlink()
        except FileNotFoundError:
            pass
        return False


def take_screenshots(
    site_root: Path,
    consolidated: ConsolidatedResult | None = None,
    out_dir: Path | None = None,
    viewport: tuple[int, int] = (1280, 820),
) -> dict[str, Path]:
    """Capture DroidBot, CodeCharta and Sunburst PNGs."""
    out_dir = out_dir or (site_root / "report")
    out_dir.mkdir(parents=True, exist_ok=True)

    decorate_js = build_decorate_js(consolidated) if consolidated else None

    # Only DroidBot and CodeCharta need a real browser screenshot — they are
    # canvas/WebGL views that can't be captured server-side. The Sunburst,
    # Legend and Propagation Tree are all rasterised by cairosvg from
    # Python-built SVG strings (see sunburst.build_*_svg), which keeps them
    # deterministic and removes any race with D3's rendering inside Playwright.
    targets = [
        # (key, relative URL, settle ms, output filename, pre-screenshot JS)
        (
            "droidbot",
            "phase3/impact-utg/index.html",
            3_500,
            "droidbot-real.png",
            decorate_js,
        ),
        (
            "codecharta",
            "phase5/codecharta-viewer/index.html?file=../after.cc.json"
            "&mode=Single&area=rloc&height=mcc&color=impact_level",
            9_000,
            "codecharta-real.png",
            None,
        ),
    ]

    server, port = _start_static_server(site_root)
    base = f"http://127.0.0.1:{port}"
    saved: dict[str, Path] = {}
    try:
        from playwright.sync_api import sync_playwright  # type: ignore

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--use-gl=swiftshader", "--no-sandbox"])
            try:
                for key, rel, settle, fname, pre_js in targets:
                    if not _file_exists(site_root, rel):
                        print(f"[screenshots] skip {key}: {rel} not on disk")
                        continue
                    page = browser.new_page(
                        viewport={"width": viewport[0], "height": viewport[1]},
                        device_scale_factor=2,
                    )
                    out_path = out_dir / fname
                    if _screenshot(page, f"{base}/{rel}", settle, out_path, pre_js):
                        saved[key] = out_path
                    page.close()
            finally:
                browser.close()
    except ImportError:
        print("[screenshots] playwright not installed — skipping real screenshots")
    finally:
        server.shutdown()
        server.server_close()

    summary = {k: str(v) for k, v in saved.items()}
    print(f"[screenshots] saved={json.dumps(summary)}")
    return saved


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("site_root")
    parser.add_argument("--consolidated", help="Path to consolidated.json", default=None)
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()
    cons = None
    if args.consolidated:
        from ..contracts import ConsolidatedResult as _CR
        cons = _CR.model_validate_json(Path(args.consolidated).read_text())
    take_screenshots(
        Path(args.site_root),
        cons,
        out_dir=Path(args.out_dir) if args.out_dir else None,
    )
