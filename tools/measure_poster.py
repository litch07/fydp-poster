"""
measure_poster.py - Playwright-based poster measurement tool.

For every card reports:
  - Overflow (any child outside card padding)
  - Content height as % of card height
  - Smallest font size in pt (excluding SVG internal text)
  - Whether all inner strips have equal width and equal left alignment
Also checks:
  - Cards tile 781x1129 mm with no gap >12 mm between adjacent cards
  - Computed font-family is Carlito
Prints a table and saves screenshot to tools/shots/poster.png.
"""

import json, os, sys, math
from pathlib import Path
from playwright.sync_api import sync_playwright

POSTER_FILE = Path(__file__).resolve().parent.parent / "poster.html"
SHOT_DIR = Path(__file__).resolve().parent / "shots"
SHOT_DIR.mkdir(exist_ok=True)

MM2PX = 3.7795275591
PAGE_W_MM = 841
PAGE_H_MM = 1189
CONTENT_W_MM = 781
CONTENT_H_MM = 1129
MAX_GAP_MM = 12.5

CARD_SPECS = {
    "header":          {"w": 781,   "h": 150},
    "hero":            {"w": 781,   "h": 180},
    "motivation":      {"w": 384.5, "h": 150},
    "objectives":      {"w": 384.5, "h": 150},
    "methodology":     {"w": 781,   "h": 150},
    "dataset":         {"w": 270,   "h": 192},
    "outcome-buckets": {"w": 240,   "h": 192},
    "metrics":         {"w": 247,   "h": 192},
    "research-gap":    {"w": 400,   "h": 135},
    "pilot-system":    {"w": 369,   "h": 135},
    "status":          {"w": 384.5, "h": 100},
    "references":      {"w": 384.5, "h": 100},
}

# Rows define which cards should be adjacent vertically
ROWS = [
    ["header"],
    ["hero"],
    ["motivation", "objectives"],
    ["methodology"],
    ["dataset", "outcome-buckets", "metrics"],
    ["research-gap", "pilot-system"],
    ["status", "references"],
]

JS_MEASURE = """
() => {
    const mm2px = 3.7795275591;
    const results = {};

    const cards = document.querySelectorAll('[data-card]');
    cards.forEach(card => {
        const name = card.getAttribute('data-card');
        const cardRect = card.getBoundingClientRect();
        const cardStyle = window.getComputedStyle(card);
        const padTop = parseFloat(cardStyle.paddingTop) || 0;
        const padRight = parseFloat(cardStyle.paddingRight) || 0;
        const padBottom = parseFloat(cardStyle.paddingBottom) || 0;
        const padLeft = parseFloat(cardStyle.paddingLeft) || 0;

        const innerTop = cardRect.top + padTop;
        const innerLeft = cardRect.left + padLeft;
        const innerRight = cardRect.right - padRight;
        const innerBottom = cardRect.bottom - padBottom;

        // Check overflow: any DIRECT child or important element outside the card padding box
        let overflow = false;
        let overflowDetails = [];
        const directChildren = card.querySelectorAll(':scope > *, :scope > * > *');
        directChildren.forEach(child => {
            const cr = child.getBoundingClientRect();
            if (cr.width === 0 && cr.height === 0) return;
            // Skip SVG internals
            if (child.closest('svg') && child.tagName !== 'svg') return;
            if (cr.top < innerTop - 2 || cr.left < innerLeft - 2 ||
                cr.bottom > innerBottom + 2 || cr.right > innerRight + 2) {
                overflow = true;
                let issue = child.tagName + '.' + child.className;
                if (cr.bottom > innerBottom + 2) issue += ` (Bottom: ${cr.bottom} > ${innerBottom})`;
                if (cr.right > innerRight + 2) issue += ` (Right: ${cr.right} > ${innerRight})`;
                if (cr.left < innerLeft - 2) issue += ` (Left: ${cr.left} < ${innerLeft})`;
                overflowDetails.push(issue);
            }
        });

        // Content height: find bounding box of direct children (not SVG internals)
        let minChildTop = Infinity, maxChildBottom = -Infinity;
        const contentChildren = card.querySelectorAll(':scope > *');
        contentChildren.forEach(child => {
            const cr = child.getBoundingClientRect();
            if (cr.width === 0 && cr.height === 0) return;
            if (cr.top < minChildTop) minChildTop = cr.top;
            if (cr.bottom > maxChildBottom) maxChildBottom = cr.bottom;
        });
        const contentHeight = maxChildBottom - minChildTop;
        const cardInnerHeight = innerBottom - innerTop;
        const fillPct = cardInnerHeight > 0 ? (contentHeight / cardInnerHeight) * 100 : 0;

        // Smallest font size in pt - only HTML text elements, NOT SVG internals
        let smallestFont = Infinity;
        const textElements = card.querySelectorAll('div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th');
        textElements.forEach(el => {
            // Skip if inside SVG
            if (el.closest('svg')) return;
            // Must have actual text content
            const hasText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
            if (!hasText) return;
            const fs = parseFloat(window.getComputedStyle(el).fontSize);
            if (fs > 0 && fs < smallestFont) {
                smallestFont = fs;
            }
        });
        const smallestFontPt = smallestFont === Infinity ? 0 : smallestFont / 1.3333;

        // Check strips
        const strips = card.querySelectorAll('.strip');
        let stripsEqual = true;
        if (strips.length > 1) {
            const firstRect = strips[0].getBoundingClientRect();
            const refWidth = Math.round(firstRect.width);
            const refLeft = Math.round(firstRect.left);
            strips.forEach(s => {
                const sr = s.getBoundingClientRect();
                if (Math.abs(Math.round(sr.width) - refWidth) > 2) stripsEqual = false;
                if (Math.abs(Math.round(sr.left) - refLeft) > 2) stripsEqual = false;
            });
        }

        const ff = window.getComputedStyle(card).fontFamily;
        let headerIssues = [];
        if (name === 'header') {
            const mm2px = 3.7795275591;
            
            // Check authors
            const authorRows = card.querySelectorAll('.author-row');
            if (authorRows.length === 5) {
                let firstLeft = null;
                let yPositions = [];
                let heights = [];
                authorRows.forEach((row, idx) => {
                    const rect = row.getBoundingClientRect();
                    // Wrap check: a single line author row shouldn't be taller than 40px (approx 30pt line height)
                    if (rect.height > 60) headerIssues.push(`Author row ${idx+1} wrapped (height ${rect.height}px)`);
                    
                    if (firstLeft === null) firstLeft = rect.left;
                    else if (Math.abs(rect.left - firstLeft) > 1) headerIssues.push(`Author row ${idx+1} not left-aligned`);
                    
                    yPositions.push(rect.top);
                });
                
                // Check even spacing
                if (yPositions.length === 5) {
                    let gaps = [];
                    for(let i=0; i<4; i++) {
                        gaps.push(yPositions[i+1] - yPositions[i]);
                    }
                    const avgGap = gaps.reduce((a,b)=>a+b, 0) / gaps.length;
                    gaps.forEach((g, i) => {
                        if(Math.abs(g - avgGap) > 2) headerIssues.push(`Author rows not evenly spaced (gap ${i} is ${g}, avg ${avgGap})`);
                    });
                }
            } else {
                headerIssues.push(`Found ${authorRows.length} author rows instead of 5`);
            }
            
            // Check Title lines
            const titleEl = card.querySelector('.header-title');
            if (titleEl) {
                const titleRect = titleEl.getBoundingClientRect();
                const lhStr = window.getComputedStyle(titleEl).lineHeight;
                const lh = lhStr === 'normal' ? 1.1 * parseFloat(window.getComputedStyle(titleEl).fontSize) : parseFloat(lhStr);
                const lines = Math.round(titleRect.height / lh);
                if (lines !== 2) headerIssues.push(`Title has ${lines} lines instead of 2 (height: ${titleRect.height}, lh: ${lh})`);
            }
            
            // Check Pill and Tile padding
            const pill = card.querySelector('.team-pill');
            if (pill) {
                const pstyle = window.getComputedStyle(pill);
                const pt = parseFloat(pstyle.paddingTop)/mm2px, pb = parseFloat(pstyle.paddingBottom)/mm2px;
                const pl = parseFloat(pstyle.paddingLeft)/mm2px, pr = parseFloat(pstyle.paddingRight)/mm2px;
                if (pt < 2.9 || pb < 2.9 || pl < 2.9 || pr < 2.9) headerIssues.push(`Team pill padding < 3mm`);
            }
            const tiles = card.querySelectorAll('.faculty-tile');
            tiles.forEach((tile, idx) => {
                const pstyle = window.getComputedStyle(tile);
                const pt = parseFloat(pstyle.paddingTop)/mm2px, pb = parseFloat(pstyle.paddingBottom)/mm2px;
                const pl = parseFloat(pstyle.paddingLeft)/mm2px, pr = parseFloat(pstyle.paddingRight)/mm2px;
                if (pt < 2.9 || pb < 2.9 || pl < 2.9 || pr < 2.9) headerIssues.push(`Faculty tile ${idx+1} padding < 3mm`);
            });
        }

        results[name] = {
            overflow: overflow,
            overflowDetails: overflowDetails.slice(0, 3),
            fillPct: Math.round(fillPct * 10) / 10,
            smallestFontPt: Math.round(smallestFontPt * 10) / 10,
            stripsEqual: stripsEqual,
            fontFamily: ff,
            cardRect: {
                x: cardRect.x / mm2px,
                y: cardRect.y / mm2px,
                w: cardRect.width / mm2px,
                h: cardRect.height / mm2px
            },
            headerIssues: headerIssues
        };
    });

    return results;
}
"""


def check_tiling(cards_data):
    """Check that cards tile correctly: only adjacent rows and columns checked."""
    issues = []
    if not cards_data:
        return ["No cards found"]

    rects = {}
    for name, data in cards_data.items():
        r = data["cardRect"]
        rects[name] = (r["x"], r["y"], r["w"], r["h"])

    # Check bounding box
    all_rects = list(rects.values())
    min_x = min(r[0] for r in all_rects)
    min_y = min(r[1] for r in all_rects)
    max_x = max(r[0] + r[2] for r in all_rects)
    max_y = max(r[1] + r[3] for r in all_rects)

    total_w = max_x - min_x
    total_h = max_y - min_y

    if abs(min_x - 30) > 0.5:
        issues.append(f"Left edge at {min_x:.1f}mm (expected 30mm)")
    if abs(max_x - (30 + CONTENT_W_MM)) > 0.5:
        issues.append(f"Right edge at {max_x:.1f}mm (expected {30 + CONTENT_W_MM}mm)")

    if abs(total_w - CONTENT_W_MM) > 0.5:
        issues.append(f"Total width {total_w:.1f}mm != {CONTENT_W_MM}mm")
    if abs(total_h - CONTENT_H_MM) > 0.5:
        issues.append(f"Total height {total_h:.1f}mm != {CONTENT_H_MM}mm")

    # Check horizontal gaps within each row
    for row in ROWS:
        if len(row) <= 1:
            continue
        for i in range(len(row) - 1):
            n1, n2 = row[i], row[i + 1]
            if n1 not in rects or n2 not in rects:
                continue
            r1 = rects[n1]
            r2 = rects[n2]
            gap = r2[0] - (r1[0] + r1[2])
            if abs(gap - 6) > 0.5:
                issues.append(f"H-gap {n1}->{n2}: {gap:.1f}mm (expected 6mm)")

    # Check vertical gaps between adjacent rows
    for i in range(len(ROWS) - 1):
        top_row = ROWS[i]
        bot_row = ROWS[i + 1]
        # Use first card in each row to check vertical gap
        n1 = top_row[0]
        n2 = bot_row[0]
        if n1 not in rects or n2 not in rects:
            continue
        r1 = rects[n1]
        r2 = rects[n2]
        gap = r2[1] - (r1[1] + r1[3])
        if abs(gap - 6) > 0.5:
            issues.append(f"V-gap row({n1})->row({n2}): {gap:.1f}mm (expected 6mm)")

    # Check no empty band at bottom
    bottom_edge = max_y
    expected_bottom = 30 + CONTENT_H_MM  # 30mm margin + content
    if abs(bottom_edge - expected_bottom) > 0.5:
        issues.append(f"Bottom edge at {bottom_edge:.1f}mm (expected {expected_bottom:.0f}mm)")

    return issues


def main():
    if not POSTER_FILE.exists():
        print(f"ERROR: {POSTER_FILE} not found")
        sys.exit(1)

    url = POSTER_FILE.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": int(PAGE_W_MM * MM2PX), "height": int(PAGE_H_MM * MM2PX)}
        )
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        shot_path = str(SHOT_DIR / "poster.png")
        page.screenshot(path=shot_path, full_page=True)
        print(f"Screenshot saved: {shot_path}")

        data = page.evaluate(JS_MEASURE)
        browser.close()

    if not data:
        print("ERROR: No cards found")
        sys.exit(1)

    print()
    print(f"{'Card':<18} {'Overflow':<10} {'Fill%':<8} {'MinFont':<10} {'Strips':<10} {'Font':<20}")
    print("-" * 76)

    all_pass = True
    for name in CARD_SPECS:
        if name not in data:
            print(f"{name:<18} {'MISSING':<10}")
            all_pass = False
            continue
        d = data[name]
        ov = "FAIL" if d["overflow"] else "OK"
        fill = f"{d['fillPct']:.1f}%"
        font_size = f"{d['smallestFontPt']:.1f}pt"
        strips = "OK" if d["stripsEqual"] else "FAIL"
        ff = d["fontFamily"][:18]

        min_font = 20.0 if name in ("references", "header", "pilot-system") else 24.0
        font_ok = d["smallestFontPt"] >= min_font - 0.5

        if d["overflow"] or d["fillPct"] < 88 or not font_ok or not d["stripsEqual"]:
            all_pass = False

        has_carlito = "Carlito" in ff or "carlito" in ff
        if not has_carlito:
            all_pass = False
            ff = ff + " !!!"

        print(f"{name:<18} {ov:<10} {fill:<8} {font_size:<10} {strips:<10} {ff:<20}")
        if d["overflow"]:
            for detail in d["overflowDetails"]:
                print(f"    - {detail}")

    print()
    if data.get("header") and data["header"].get("headerIssues"):
        print("HEADER ISSUES:")
        for hi in data["header"]["headerIssues"]:
            print(f"  X {hi}")
            all_pass = False
        print()

    tiling_issues = check_tiling(data)
    if tiling_issues:
        print("TILING ISSUES:")
        for issue in tiling_issues:
            print(f"  X {issue}")
        all_pass = False
    else:
        print("TILING: OK All cards tile 781x1129mm correctly")

    print()
    if all_pass:
        print("=== ALL CHECKS PASSED ===")
    else:
        print("=== SOME CHECKS FAILED ===")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
