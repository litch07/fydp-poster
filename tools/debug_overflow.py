"""Debug which elements overflow in dataset and metrics cards."""
from playwright.sync_api import sync_playwright
from pathlib import Path

JS = """
(name) => {
    const mm2px = 3.7795275591;
    const card = document.querySelector('[data-card="' + name + '"]');
    const cr = card.getBoundingClientRect();
    const cs = window.getComputedStyle(card);
    const pt = parseFloat(cs.paddingTop);
    const pb = parseFloat(cs.paddingBottom);
    const pl = parseFloat(cs.paddingLeft);
    const pr = parseFloat(cs.paddingRight);
    const innerTop = cr.top + pt;
    const innerBot = cr.bottom - pb;
    const innerLeft = cr.left + pl;
    const innerRight = cr.right - pr;
    
    let issues = [];
    const children = card.querySelectorAll(':scope > *, :scope > * > *');
    children.forEach(child => {
        const ccr = child.getBoundingClientRect();
        if (ccr.width === 0 && ccr.height === 0) return;
        if (child.closest('svg') && child.tagName !== 'svg') return;
        if (ccr.bottom > innerBot + 2) {
            issues.push({
                tag: child.tagName,
                cls: child.className,
                bottom_mm: (ccr.bottom / mm2px).toFixed(1),
                innerBot_mm: (innerBot / mm2px).toFixed(1),
                overflow_mm: ((ccr.bottom - innerBot) / mm2px).toFixed(1)
            });
        }
    });
    return {
        card_h: (cr.height / mm2px).toFixed(1),
        pad_t: (pt / mm2px).toFixed(1),
        pad_b: (pb / mm2px).toFixed(1),
        inner_h: ((innerBot - innerTop) / mm2px).toFixed(1),
        issues: issues
    };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 3179, "height": 4494})
    page.goto(Path("poster.html").resolve().as_uri(), wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    for card_name in ["motivation", "objectives"]:
        result = page.evaluate(JS, card_name)
        print(f"\n{card_name}:")
        print(f"  card_h={result['card_h']}mm pad_t={result['pad_t']}mm pad_b={result['pad_b']}mm inner_h={result['inner_h']}mm")
        for iss in result["issues"]:
            print(f"  OVERFLOW: <{iss['tag']} class='{iss['cls']}'> bottom={iss['bottom_mm']}mm innerBot={iss['innerBot_mm']}mm overflow={iss['overflow_mm']}mm")
    
    b.close()
