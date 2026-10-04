#!/usr/bin/env python3
"""
tools/check_svg.py
Usage: python tools/check_svg.py <file.svg>

Checks:
  a) font-size < 8.5 units (except data-caption="1" which may be 7.1)
  b) any <text> with a rotation transform
  c) text box not inside nearest enclosing shape or within 3 mm of edge
     (exempt: data-free="1")
  d) two text boxes overlap
  e) any element extends outside the viewBox
  f) saves PNG to tools/shots/<name>.png

Exits 0 (PASS) or 1 (FAIL).
1 unit = 1 mm (SVGs built with mm viewBox per CONTEXT.md rule 2)
"""

import sys
import os
import re
import math
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).parent
SHOTS_DIR = SCRIPT_DIR / "shots"
SHOTS_DIR.mkdir(parents=True, exist_ok=True)

CARLITO_PATH = Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts\Carlito-Regular.ttf"))

MIN_FONT_SIZE = 8.5
MIN_CAPTION_FONT_SIZE = 7.1
EDGE_MARGIN = 3.0


def rects_overlap(a, b):
    ax2 = a["x"] + a["width"]
    ay2 = a["y"] + a["height"]
    bx2 = b["x"] + b["width"]
    by2 = b["y"] + b["height"]
    return not (ax2 <= b["x"] or bx2 <= a["x"] or ay2 <= b["y"] or by2 <= a["y"])


def rect_fully_inside(inner, outer, margin=0):
    return (
        inner["x"] >= outer["x"] + margin
        and inner["y"] >= outer["y"] + margin
        and inner["x"] + inner["width"] <= outer["x"] + outer["width"] - margin
        and inner["y"] + inner["height"] <= outer["y"] + outer["height"] - margin
    )


EXTRACT_JS = """
() => {
    const svg = document.querySelector('svg');
    if (!svg) return {error: 'no svg found'};
    const vb = svg.viewBox.baseVal;
    const viewBox = {x: vb.x, y: vb.y, width: vb.width, height: vb.height};
    const svgRect = svg.getBoundingClientRect();
    const scaleX = vb.width > 0 ? svgRect.width / vb.width : 1;
    const scaleY = vb.height > 0 ? svgRect.height / vb.height : 1;

    function toVB(r) {
        return {
            x: (r.left - svgRect.left) / scaleX + vb.x,
            y: (r.top  - svgRect.top)  / scaleY + vb.y,
            width:  r.width  / scaleX,
            height: r.height / scaleY,
        };
    }

    const texts = [];
    svg.querySelectorAll('text').forEach((el, idx) => {
        const cr = el.getBoundingClientRect();
        const box = toVB(cr);
        const style = window.getComputedStyle(el);
        const fsPx = parseFloat(style.fontSize) || 0;
        const fsUnits = fsPx / scaleY;
        let combinedTransform = el.getAttribute('transform') || '';
        let p = el.parentElement;
        while (p && p !== svg) {
            const t = p.getAttribute('transform') || '';
            if (t) combinedTransform += ' ' + t;
            p = p.parentElement;
        }
        texts.push({
            idx,
            content: el.textContent.trim(),
            box,
            fsUnits,
            transform: combinedTransform,
            isCaption: el.getAttribute('data-caption') === '1',
            isFree:    el.getAttribute('data-free')    === '1',
        });
    });

    const shapes = [];
    svg.querySelectorAll('rect, circle, ellipse, path').forEach((el) => {
        const cr = el.getBoundingClientRect();
        if (cr.width === 0 && cr.height === 0) return;
        shapes.push({tag: el.tagName.toLowerCase(), box: toVB(cr)});
    });

    const allBoxes = [];
    svg.querySelectorAll('*').forEach(el => {
        try {
            const cr = el.getBoundingClientRect();
            if (cr.width === 0 && cr.height === 0) return;
            allBoxes.push({tag: el.tagName.toLowerCase(), id: el.id || '', box: toVB(cr)});
        } catch(e) {}
    });

    return {viewBox, texts, shapes, allBoxes};
}
"""


def fmt(b):
    return f"x={b['x']:.1f} y={b['y']:.1f} w={b['width']:.1f} h={b['height']:.1f}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/check_svg.py <file.svg>")
        sys.exit(2)

    svg_path = Path(sys.argv[1]).resolve()
    if not svg_path.exists():
        print(f"File not found: {svg_path}")
        sys.exit(2)

    shot_name = SHOTS_DIR / (svg_path.stem + ".png")
    failures = []

    carlito_b64 = ""
    if CARLITO_PATH.exists():
        import base64
        carlito_b64 = base64.b64encode(CARLITO_PATH.read_bytes()).decode()

    svg_content = svg_path.read_text(encoding="utf-8")
    carlito_face = ""
    if carlito_b64:
        carlito_face = (
            "@font-face {"
            "font-family:'Carlito';"
            f"src:url('data:font/truetype;base64,{carlito_b64}') format('truetype');"
            "font-weight:normal;font-style:normal;}"
        )

    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{carlito_face} body{{margin:0;padding:0;background:#fff;}}"
        "svg{display:block;max-width:100%;height:auto;}</style>"
        f"</head><body>{svg_content}</body></html>"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 1200})
        page = ctx.new_page()
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=str(shot_name))
        data = page.evaluate(EXTRACT_JS)
        browser.close()

    if "error" in data:
        print(f"FAIL: {data['error']}")
        sys.exit(1)

    vb = data["viewBox"]
    texts = data["texts"]
    shapes = data["shapes"]
    all_boxes = data["allBoxes"]
    vb_rect = {"x": vb["x"], "y": vb["y"], "width": vb["width"], "height": vb["height"]}

    # (a) font-size
    for t in texts:
        min_sz = MIN_CAPTION_FONT_SIZE if t["isCaption"] else MIN_FONT_SIZE
        if t["fsUnits"] < min_sz - 0.05:
            failures.append(
                f"[font-size] '{t['content'][:40]}' size={t['fsUnits']:.2f} < {min_sz} "
                f"({fmt(t['box'])})"
            )

    # (b) rotation
    ROT_RE = re.compile(r"rotate\s*\(", re.I)
    MAT_RE = re.compile(r"matrix\s*\(\s*([0-9eE.+\-]+)\s*,\s*([0-9eE.+\-]+)", re.I)
    for t in texts:
        tr = t["transform"]
        if ROT_RE.search(tr):
            failures.append(f"[rotation] '{t['content'][:40]}' has rotate() transform")
            continue
        m = MAT_RE.search(tr)
        if m:
            a_v = float(m.group(1))
            b_v = float(m.group(2))
            if abs(b_v) > 0.01 or abs(a_v - 1.0) > 0.01:
                failures.append(f"[rotation] '{t['content'][:40]}' has non-trivial matrix")

    # (c) containment with 3 mm margin
    for t in texts:
        if t["isFree"]:
            continue
        tb = t["box"]
        if tb["width"] <= 0 or tb["height"] <= 0:
            continue
        best = None
        best_area = math.inf
        for s in shapes:
            sb = s["box"]
            if rect_fully_inside(tb, sb, margin=0):
                area = sb["width"] * sb["height"]
                if area < best_area:
                    best_area = area
                    best = s
        if best is None:
            failures.append(
                f"[containment] '{t['content'][:40]}' not inside any shape ({fmt(tb)})"
            )
        elif not rect_fully_inside(tb, best["box"], margin=EDGE_MARGIN):
            failures.append(
                f"[margin] '{t['content'][:40]}' within {EDGE_MARGIN}mm of container edge "
                f"(text={fmt(tb)}, container={fmt(best['box'])})"
            )

    # (d) overlapping text boxes
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            ta = texts[i]
            tb_item = texts[j]
            if ta["box"]["width"] <= 0 or tb_item["box"]["width"] <= 0:
                continue
            if rects_overlap(ta["box"], tb_item["box"]):
                failures.append(
                    f"[overlap] '{ta['content'][:30]}' overlaps '{tb_item['content'][:30]}'"
                )

    # (e) elements outside viewBox
    TOL = 0.5
    for el in all_boxes:
        eb = el["box"]
        if eb["width"] <= 0 or eb["height"] <= 0:
            continue
        if (
            eb["x"] < vb_rect["x"] - TOL
            or eb["y"] < vb_rect["y"] - TOL
            or eb["x"] + eb["width"]  > vb_rect["x"] + vb_rect["width"]  + TOL
            or eb["y"] + eb["height"] > vb_rect["y"] + vb_rect["height"] + TOL
        ):
            label = el.get("id") or el["tag"]
            failures.append(
                f"[viewBox] <{el['tag']} id='{label}'> outside viewBox "
                f"({fmt(eb)}, vb={fmt(vb_rect)})"
            )

    if failures:
        print(f"FAIL ({len(failures)} violation(s)) — screenshot: {shot_name}")
        for msg in failures:
            print(f"  • {msg}")
        sys.exit(1)
    else:
        print(f"PASS — screenshot saved to {shot_name}")
        sys.exit(0)


if __name__ == "__main__":
    main()
