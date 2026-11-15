# -*- coding: utf-8 -*-
"""
[已归档] 超级菜单预览页生成器 —— 方案已于 2026-11-15 正式落地，
结构进了 tools/nav.py、样式进了 assets/site.css，预览页 _preview-megamenu.html 已删除。
保留本文件仅作历史记录；再跑会生成一份过期的独立预览页，请勿用于验收。
用法: python tools/preview_megamenu.py
"""
import re
import io

SRC = 'index.html'
OUT = '_preview-megamenu.html'

ITEMS = [
    ('component',  'Component speakers',   '10'),
    ('subwoofer',  'Subwoofers',           '8'),
    ('coaxial',    'Coaxial speakers',     '6'),
    ('activebass', 'Underseat subwoofers', '2'),
    ('midrange',   'Mid &amp; full-range', '2'),
    ('amp',        'DSP &amp; amplifiers', '1'),
    ('tweeter',    'Tweeters',             '1'),
]
PROJ = ('contact.html?topic=damping', 'Damping &amp; insulation', '&mdash;')


def row(href, label, num):
    return ('<a class="mega__item" href="%s"><span>%s</span><em>%s</em></a>'
            % (href, label, num))


CELLS = [row('products.html#%s' % k, lab, n) for k, lab, n in ITEMS]
CELLS.append(row(*PROJ))
COLS = '\n                  '.join(CELLS)

MEGA = '''<div class="navm__panel navm__panel--mega" id="navm-products" data-open="true">
          <div class="mega">
            <div class="mega__head">
              <span class="mega__kicker">Product catalogue</span>
              <span class="mega__count">30 platforms &middot; 8 categories</span>
            </div>
            <div class="mega__body">
              <div class="mega__left">
                <p class="mega__label">By family</p>
                <div class="mega__cols">
                  ''' + COLS + '''
                </div>
                <p class="mega__note">Sizes, finishes and configurations are confirmed per model.</p>
              </div>
              <a class="mega__feat" href="product-zm-m65k.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-m65k.webp" alt="ZEMING 6.5-inch component speaker set" width="520" height="341"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Featured platform</span>
                  <b>ZM-M65K</b>
                  <small>6.5&Prime; &middot; 2-way component system</small>
                </span>
                <span class="mega__go">View platform
                  <svg width="13" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg>
                </span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="products.html#catalogue">All 30 platforms
                <svg width="13" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg>
              </a>
              <a href="contact.html">Request a data sheet
                <svg width="13" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg>
              </a>
            </div>
          </div>
        </div>'''

CSS = '''
<style id="mega-preview-css">
/* ===== mega menu preview only (not part of site.css) ===== */
/* pinned open: site.js closes the panel on mouseleave, so lock it in the preview */
.navm__panel--mega {
  width: 774px; left: -20px; padding: 0; background: #101215;
  opacity: 1 !important; visibility: visible !important;
  pointer-events: auto !important; transform: none !important;
}

.mega__head {
  display: flex; align-items: baseline; justify-content: space-between; gap: 20px;
  padding: 15px 22px 11px; border-bottom: 1px solid rgba(237,234,228,.10);
}
.mega__kicker {
  font-family: var(--f-mono); font-size: 9px; letter-spacing: .2em;
  text-transform: uppercase; color: var(--brand-lt);
}
.mega__count {
  font-family: var(--f-mono); font-size: 9px; letter-spacing: .14em;
  text-transform: uppercase; color: #6E767B;
}

.mega__body { display: grid; grid-template-columns: minmax(0,1fr) 268px; }
.mega__left { padding: 13px 10px 14px 14px; display: flex; flex-direction: column; }
.mega__label {
  font-family: var(--f-mono); font-size: 8.5px; letter-spacing: .2em; text-transform: uppercase;
  color: #6E767B; margin: 0 0 6px 9px;
}
.mega__cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 30px; }
.mega__item:nth-child(even) { border-left: 1px solid rgba(237,234,228,.055); padding-left: 20px; }
.mega__note {
  font-family: var(--f-mono); font-size: 8.5px; letter-spacing: .1em; line-height: 1.6;
  text-transform: uppercase; color: #5A6368; margin: auto 9px 0; padding-top: 12px;
}
.mega__item {
  display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
  padding: 11px 9px; text-decoration: none; color: var(--on-ink-mut);
  border-bottom: 1px solid rgba(237,234,228,.055);
  transition: background .18s, color .18s;
}
.mega__item span { font-size: 13.2px; letter-spacing: -.005em; white-space: nowrap; }
.mega__item em {
  font-style: normal; font-family: var(--f-mono); font-size: 9px;
  letter-spacing: .1em; color: #6E767B; flex: none;
}
.mega__item:nth-child(n+7) { border-bottom: 0; }
.mega__item:hover { background: rgba(243,240,234,.06); color: var(--on-ink); }
.mega__item:hover em { color: var(--brand-lt); }

/* featured platform — light "photo paper" inside the dark panel */
.mega__feat {
  border-left: 1px solid rgba(237,234,228,.10);
  padding: 13px 16px 4px; display: flex; flex-direction: column; gap: 10px;
  text-decoration: none; color: var(--on-ink);
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,0));
  transition: background .25s;
}
.mega__feat:hover { background: linear-gradient(180deg, rgba(255,255,255,.055), rgba(255,255,255,.012)); }
.mega__shot {
  display: block; aspect-ratio: 3 / 2; overflow: hidden;
  background: linear-gradient(170deg, #E9F1FA 0%, var(--paper-2) 100%);
}
.mega__shot img {
  width: 100%; height: 100%; object-fit: contain; mix-blend-mode: multiply;
  transform: scale(1.02); transition: transform .7s var(--e-out);
}
.mega__feat:hover .mega__shot img { transform: scale(1.07); }
.mega__tag {
  font-family: var(--f-mono); font-size: 8px; letter-spacing: .2em; text-transform: uppercase;
  color: var(--brand-lt);
}
.mega__meta b {
  display: block; font-family: var(--f-display); font-weight: 650; font-size: 16px;
  letter-spacing: -.01em; margin-top: 3px;
}
.mega__meta small {
  display: block; font-family: var(--f-mono); font-size: 9px; letter-spacing: .1em;
  color: #7C858A; margin-top: 4px; text-transform: uppercase;
}
.mega__go {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  margin-top: auto; padding: 12px 0 14px;
  font-family: var(--f-mono); font-size: 9px; letter-spacing: .16em; text-transform: uppercase;
  color: var(--on-ink-mut);
}
.mega__feat:hover .mega__go { color: var(--on-ink); }
.mega__go svg { transition: transform .3s var(--e-out); }
.mega__feat:hover .mega__go svg { transform: translateX(3px); }

.mega__foot { display: flex; border-top: 1px solid rgba(237,234,228,.10); background: rgba(255,255,255,.016); }
.mega__foot a {
  flex: 1; padding: 12px 22px; text-decoration: none;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  font-family: var(--f-mono); font-size: 9.5px; letter-spacing: .16em; text-transform: uppercase;
  color: var(--on-ink-mut); transition: background .2s, color .2s;
}
.mega__foot a + a { border-left: 1px solid rgba(237,234,228,.10); }
.mega__foot a:hover { color: var(--on-ink); background: rgba(243,240,234,.05); }
.mega__foot a svg { transition: transform .3s var(--e-out); }
.mega__foot a:hover svg { transform: translateX(3px); }

@media (max-width: 1180px) {
  .navm__panel--mega { width: auto; min-width: 470px; }
  .mega__body { grid-template-columns: 1fr; }
  .mega__feat { display: none; }
  .mega__foot a { padding: 12px 18px; }
}
</style>
'''


def main():
    src = io.open(SRC, encoding='utf-8').read()

    pat = re.compile(r'<div class="navm__panel navm__panel--wide" id="navm-products">[\s\S]*?\n        </div>')
    hits = pat.findall(src)
    assert len(hits) == 1, 'panel match: %d' % len(hits)
    src = pat.sub(lambda m: MEGA, src, count=1)

    old_btn = 'aria-expanded="false" aria-haspopup="true" aria-controls="navm-products"'
    assert src.count(old_btn) == 1, 'btn match: %d' % src.count(old_btn)
    src = src.replace(old_btn, 'aria-expanded="true" aria-haspopup="true" aria-controls="navm-products"')

    assert src.count('</head>') == 1
    src = src.replace('</head>', CSS + '</head>', 1)
    src = src.replace('<title>', '<title>[PREVIEW] ', 1)
    src = src.replace('</head>', '<style>.reveal{opacity:1!important;transform:none!important}</style></head>', 1)

    io.open(OUT, 'w', encoding='utf-8').write(src)
    print('wrote', OUT, len(src), 'chars')


if __name__ == '__main__':
    main()
