# -*- coding: utf-8 -*-
"""Build dark-background logo variants from the original brand files.

The original artwork is a blue ZM mark (#066EB7) plus a near-black wordmark
(#231916) on transparency. Brand rule: the mark keeps its original blue
everywhere; only the wordmark is lightened so it stays legible on ink. This
recolours neutral (non-blue) ink to the site's on-ink cream and leaves every
blue pixel untouched — no filter hack, no invented artwork.

    python tools/make_logo_dark.py

Writes  assets/img/logo-header-dark.png  and  assets/img/logo-footer-dark.png
"""
import struct
import zlib

CREAM = (237, 234, 228)      # --on-ink
SAT_MIN = 40                 # above this a pixel counts as "blue", left alone


def read_png(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', path
    i, idat = 8, b''
    w = h = ct = None
    while i < len(d):
        ln = struct.unpack('>I', d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        data = d[i + 8:i + 8 + ln]
        i += 12 + ln
        if typ == b'IHDR':
            w, h, bd, ct, comp, filt, inter = struct.unpack('>IIBBBBB', data)
            assert (bd, ct, inter) == (8, 6, 0), 'expected 8-bit RGBA, non-interlaced'
        elif typ == b'IDAT':
            idat += data
    raw = zlib.decompress(idat)
    stride = w * 4
    out = bytearray(stride * h)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if f == 1:
            for x in range(4, stride):
                line[x] = (line[x] + line[x - 4]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - 4] if x >= 4 else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - 4] if x >= 4 else 0
                c = prev[x - 4] if x >= 4 else 0
                b = prev[x]
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, out


def write_png(path, w, h, px):
    stride = w * 4
    raw = bytearray()
    for y in range(h):
        raw.append(0)                                   # filter: none
        raw += px[y * stride:(y + 1) * stride]

    def chunk(typ, data):
        return (struct.pack('>I', len(data)) + typ + data
                + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff))

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(png)


def recolour(src, dst):
    w, h, px = read_png(src)
    blue = neutral = 0
    for i in range(0, len(px), 4):
        a = px[i + 3]
        if not a:
            continue
        r, g, b = px[i], px[i + 1], px[i + 2]
        if max(r, g, b) - min(r, g, b) >= SAT_MIN:
            blue += 1
            continue
        px[i], px[i + 1], px[i + 2] = CREAM
        neutral += 1
    write_png(dst, w, h, px)
    print('%s -> %s  %dx%d  blue kept %d  wordmark recoloured %d'
          % (src, dst, w, h, blue, neutral))


if __name__ == '__main__':
    recolour('assets/img/logo-header.png', 'assets/img/logo-header-dark.png')
    recolour('assets/img/logo-footer.png', 'assets/img/logo-footer-dark.png')
