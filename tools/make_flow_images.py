# -*- coding: utf-8 -*-
"""Build the 4:5 crops used by the seven-step OEM/ODM band (.flow).

Source: assets/img/pic/scene-*.jpg (1200x1200, from the original site)
Output: assets/img/opt/flow-*.webp (560x700, q82)

Run: python tools/make_flow_images.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, 'assets', 'img', 'pic')
OUT = os.path.join(HERE, 'assets', 'img', 'opt')

# slug -> (source file, vertical focus 0..1 — 0.5 = centre)
STEPS = [
    ('define',    'scene-define.jpg',    0.50),
    ('engineer',  'scene-engineer.jpg',  0.46),
    ('tune',      'scene-tune.jpg',      0.50),
    ('prototype', 'scene-prototype.jpg', 0.50),
    ('brand',     'scene-brand.jpg',     0.50),
    ('package',   'scene-package.jpg',   0.50),
    ('produce',   'scene-produce.jpg',   0.46),
]

TW, TH = 560, 700          # 4:5, ~3x the widest rendered column
RATIO = TW / TH


def crop_45(im, focus=0.5):
    w, h = im.size
    if w / h > RATIO:                       # too wide -> trim sides
        nw = int(round(h * RATIO))
        x = (w - nw) // 2
        box = (x, 0, x + nw, h)
    else:                                   # too tall -> trim top/bottom
        nh = int(round(w / RATIO))
        y = int(round((h - nh) * focus))
        box = (0, y, w, y + nh)
    return im.crop(box)


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, name, focus in STEPS:
        p = os.path.join(SRC, name)
        im = Image.open(p).convert('RGB')
        im = crop_45(im, focus).resize((TW, TH), Image.LANCZOS)
        dst = os.path.join(OUT, 'flow-%s.webp' % slug)
        im.save(dst, 'WEBP', quality=82, method=6)
        print('%-10s %-22s -> %s  %d KB' % (slug, name, os.path.basename(dst),
                                           os.path.getsize(dst) // 1024))


if __name__ == '__main__':
    main()
