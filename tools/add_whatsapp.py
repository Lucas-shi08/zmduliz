# -*- coding: utf-8 -*-
"""Inject (or refresh) the WhatsApp floating button on every page.

Idempotent: the block is delimited by a marker comment, so re-running replaces
it instead of stacking another copy. Number and prefilled message match the
ones already used in the footer / contact card — do not invent new ones.

usage: python tools/add_whatsapp.py
"""
import glob
import re

NUMBER = '8618824897798'          # from _FACTS.md: +86 188 2489 7798
DISPLAY = '+86 188 2489 7798'
TEXT = ('Hello%20ZEMING%2C%20I%20would%20like%20to%20discuss%20a%20car%20audio%20project.')

# simple-icons "whatsapp" glyph, viewBox 0 0 24 24 (CC0)
GLYPH = ('M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164'
         '-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059'
         '-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371'
         '-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01'
         '-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074'
         '.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118'
         '.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347'
         'm-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374'
         'a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898'
         'a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884')
GLYPH += ('m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945'
          'L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893'
          'a11.821 11.821 0 00-3.48-8.413Z')

BLOCK = f'''<!-- WhatsApp floating contact -->
<a class="wafab" href="https://wa.me/{NUMBER}?text={TEXT}" target="_blank" rel="noopener" aria-label="Chat with ZEMING on WhatsApp, {DISPLAY} (opens in a new tab)">
  <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{GLYPH}" fill="currentColor"/></svg>
  <span class="wafab__tip" aria-hidden="true"><b>WhatsApp</b><small>{DISPLAY}</small></span>
</a>
'''

MARK = '<!-- WhatsApp floating contact -->'


def patch(path):
    s = open(path, encoding='utf-8').read()
    # drop any earlier copy, wherever it sits — position matters, so re-insert
    s = re.sub(re.escape(MARK) + r'.*?</a>\n', '', s, count=1, flags=re.S)

    # the button has to be in the DOM before site.js runs (it wires the label
    # teaser and the compare-bar offset), so land in front of the script tag
    m = re.search(r'<script src="assets/site\.js"></script>', s)
    if m:
        s2 = s[:m.start()] + BLOCK + s[m.start():]
    elif '</body>' in s:
        s2 = s.replace('</body>', BLOCK + '</body>', 1)
    else:
        print('  ! no insertion point:', path)
        return False

    open(path, 'w', encoding='utf-8').write(s2)
    return True


if __name__ == '__main__':
    files = [f for f in sorted(glob.glob('*.html')) if not f.startswith('_')]
    ok = sum(1 for f in files if patch(f))
    print('pages patched: %d/%d' % (ok, len(files)))
