import re, os
for f in sorted(os.listdir('diagrams/fit')):
    if f.endswith('.svg'):
        with open(os.path.join('diagrams/fit', f)) as fh:
            head = fh.read(500)
        w = re.search(r'width=["\']([^"\']+)', head)
        h = re.search(r'height=["\']([^"\']+)', head)
        vb = re.search(r'viewBox=["\']([^"\']+)', head)
        print(f'{f}: w={w.group(1) if w else "?"} h={h.group(1) if h else "?"} vb={vb.group(1) if vb else "?"}')
