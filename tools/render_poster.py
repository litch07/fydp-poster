"""Render poster.html to poster.pdf and poster-preview.png using Playwright."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJ = Path(__file__).resolve().parent.parent
POSTER_HTML = PROJ / "poster.html"
POSTER_PDF = PROJ / "poster.pdf"
POSTER_PNG = PROJ / "poster-preview.png"

MM2PX = 3.7795275591
PAGE_W_MM = 841
PAGE_H_MM = 1189

def main():
    if not POSTER_HTML.exists():
        print(f"ERROR: {POSTER_HTML} not found")
        return 1

    url = POSTER_HTML.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": int(PAGE_W_MM * MM2PX), "height": int(PAGE_H_MM * MM2PX)}
        )
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)

        # Render PDF - A0 size, no margins, print background
        page.pdf(
            path=str(POSTER_PDF),
            width=f"{PAGE_W_MM}mm",
            height=f"{PAGE_H_MM}mm",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            scale=1.0
        )
        print(f"PDF saved: {POSTER_PDF}")

        # Render PNG preview (full page screenshot)
        page.screenshot(
            path=str(POSTER_PNG),
            full_page=True
        )
        print(f"PNG preview saved: {POSTER_PNG}")

        browser.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
