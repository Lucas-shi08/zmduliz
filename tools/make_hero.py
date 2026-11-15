"""Re-export the hero banner from the 1920x800 source.

The previous export was 1200x500, which forced the browser to upscale it ~70%
on a 1440-wide screen (hero is 94svh tall, so cover-fit scales by height).
This writes a native-size 1920 webp plus a 1200 fallback for narrow screens.

    python tools/make_hero.py
"""
import os
from PIL import Image

SRC = '_source-images/m65k-hero.webp'
OUT = 'assets/img/opt'

jobs = [
    ('hero-1920.webp', 1920, 84),
    ('hero-1200.webp', 1200, 82),
]

src = Image.open(SRC).convert('RGB')
print('source', src.size)

for name, width, q in jobs:
    h = round(width * src.size[1] / src.size[0])
    im = src if width == src.size[0] else src.resize((width, h), Image.LANCZOS)
    dst = os.path.join(OUT, name)
    im.save(dst, 'WEBP', quality=q, method=6)
    print('%-18s %-10s %4d KB' % (dst, '%dx%d' % im.size, os.path.getsize(dst) // 1024))
