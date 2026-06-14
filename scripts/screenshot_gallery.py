"""Capture screenshots of the running reflex-rosencharts gallery.

Uses the system Chrome (Playwright's bundled Chromium is unsupported on this OS).
Run with the app already serving at http://localhost:3000 :

    .venv/bin/python scripts/screenshot_gallery.py
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

import reflex_rosencharts as rxc

OUT = pathlib.Path("docs/screenshots")
URL = "http://localhost:3000/"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    names = sorted(rxc.__all__)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=60_000)
        # Charts are NoSSR/client-side; give D3 + Tailwind a moment to paint.
        page.wait_for_timeout(2500)

        # Full gallery (long screenshot).
        page.screenshot(path=str(OUT / "_gallery_full.png"), full_page=True)
        print(f"saved {OUT/'_gallery_full.png'}")

        captured, missing = 0, []
        for name in names:
            card = page.locator(f"#{name}")
            try:
                card.scroll_into_view_if_needed(timeout=5_000)
                page.wait_for_timeout(150)
                card.screenshot(path=str(OUT / f"{name}.png"))
                captured += 1
            except Exception as exc:  # noqa: BLE001 - report, do not abort the run
                missing.append(f"{name}: {exc!r}")

        browser.close()

    print(f"captured {captured}/{len(names)} chart cards into {OUT}/")
    if missing:
        print("MISSING:")
        for m in missing:
            print(" -", m)
    return 0 if captured == len(names) else 1


if __name__ == "__main__":
    sys.exit(main())
