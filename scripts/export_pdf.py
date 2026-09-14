"""Export remark slide decks to PDF.

    uv run --no-project --with playwright python scripts/export_pdf.py lecture4.md [course-syllabus.md ...]

Each deck is served from the repository root, laid out for printing, and saved once every web
font has loaded. Plain headless Chrome prints before the KaTeX fonts arrive and leaves formulas
blank. If a font cannot be loaded (e.g., Google Fonts while offline), the export fails rather than
printing with fallback fonts. `lectureN.md` is written to `pdf/lecN.pdf`, any other `name.md` to
`pdf/name.pdf`, and the output paths are printed to stdout, one per line. The installed Google
Chrome is used, or Playwright's own Chromium when Chrome is missing.
"""

import functools
import http.server
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

ROOT = Path(__file__).resolve().parent.parent

LOAD_FONTS = """async () => {
    await Promise.all([...document.fonts].map(f => f.load().catch(() => null)));
    await document.fonts.ready;
    return [...new Set([...document.fonts].filter(f => f.status === "error").map(f => f.family))];
}"""

VIDEO_THUMBNAILS = r"""() => {
    for (const frame of document.querySelectorAll("iframe")) {
        const youtube = frame.src.match(/youtube\.com\/embed\/([\w-]+)/);
        const dailymotion = frame.src.match(/dailymotion\.com\/embed\/video\/(\w+)/);
        if (!youtube && !dailymotion) continue;
        const img = document.createElement("img");
        img.src = youtube ? `https://img.youtube.com/vi/${youtube[1]}/hqdefault.jpg`
                          : `https://www.dailymotion.com/thumbnail/video/${dailymotion[1]}`;
        img.style.width = `${frame.getAttribute("width")}px`;
        img.style.height = `${frame.getAttribute("height")}px`;
        img.style.objectFit = "cover";
        frame.replaceWith(img);
    }
}"""

WAIT_FOR_IMAGES = """async () => {
    await Promise.all([...document.images].filter(img => !img.complete)
        .map(img => new Promise(done => { img.onload = img.onerror = done; })));
}"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        if not isinstance(sys.exc_info()[1], ConnectionError):  # the browser drops media requests it no longer needs
            super().handle_error(request, client_address)


def pdf_path(deck):
    return Path("pdf") / (re.sub(r"^lecture(\d+)$", r"lec\1", Path(deck).stem) + ".pdf")


def main(decks):
    for deck in decks:
        if not (ROOT / deck).is_file():
            sys.exit(f"export_pdf: no such deck: {deck}")

    server = QuietServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=ROOT))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            browser = p.chromium.launch()
        for deck in decks:
            page = browser.new_page()
            page.goto(f"{base}/?p={Path(deck).name}")
            page.wait_for_selector(".remark-slide-content")
            page.evaluate(VIDEO_THUMBNAILS)  # an embedded player prints as an empty frame
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                pass  # embedded videos can keep the network busy; images are awaited below
            page.emulate_media(media="print")  # lay out every slide, so that all their fonts get requested
            failed = page.evaluate(LOAD_FONTS)
            if failed:
                sys.exit(f"export_pdf: fonts failed to load for {deck}: {', '.join(failed)}")
            page.evaluate(WAIT_FOR_IMAGES)
            page.pdf(path=ROOT / pdf_path(deck), prefer_css_page_size=True, print_background=True)
            page.close()
            print(pdf_path(deck))
        browser.close()
    server.shutdown()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
