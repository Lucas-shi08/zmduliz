# -*- coding: utf-8 -*-
"""Point every page at a dark-background logo that keeps the brand blue.

The old build whitened the whole mark with `filter: brightness(0) invert(1)` on
the dark nav and footer. Brand rule is the opposite: the ZM mark keeps its
original blue, only the wordmark is lightened. So the nav carries two files and
swaps them by CSS — dark variant over ink, original over bone.

Idempotent: safe to re-run. Also patches tools/gen_catalog.py so regenerating
the catalogue pages does not revert the change.

    python tools/patch_logo.py
"""
import glob
import re

DARK = ('      <img class="logo-d" src="assets/img/logo-header-dark.png" alt="ZEMING" '
        'width="1172" height="240">')

NAV_RE = re.compile(r'^[ \t]*<img src="assets/img/logo-header\.png" alt="ZEMING" '
                    r'width="1172" height="240">$', re.M)
# collapse an earlier two-file build down to the single dark asset
PAIR_RE = re.compile(r'[ \t]*<img class="logo-d"[^\n]*\n[ \t]*<img class="logo-l"[^\n]*', re.M)
FOOT_RE = re.compile(r'(class="foot__logo"><img src="assets/img/logo-)footer\.png')


def patch(path):
    s = open(path, encoding='utf-8').read()
    before = s
    s, p = PAIR_RE.subn(DARK, s)
    s, n = NAV_RE.subn(DARK, s)
    s, m = FOOT_RE.subn(r'\1footer-dark.png', s)
    if s != before:
        open(path, 'w', encoding='utf-8').write(s)
    return n + p, m


if __name__ == '__main__':
    files = sorted(glob.glob('*.html')) + ['tools/gen_catalog.py']
    for f in files:
        if f.startswith('_'):
            continue
        n, m = patch(f)
        print('%-28s nav:%d footer:%d' % (f, n, m))
