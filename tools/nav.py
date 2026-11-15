# -*- coding: utf-8 -*-
"""Rewrite the primary navigation (desktop dropdowns + drawer groups) on every page.

Idempotent: replaces the whole <nav class="nav__links"> block, the nav CTA and the
drawer link list, so it can be re-run after any page edits.
"""
import glob
import re
import sys

CARET = ('<svg class="navm__caret" width="9" height="5" viewBox="0 0 8 5" fill="none" aria-hidden="true">'
         '<path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.2"/></svg>')

ARROW = ('<svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true">'
         '<path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg>')

# family key, label, count (None = offered, but no platform count published)
# Order is the visual order of the mega panel read row by row, two columns:
#   component | subwoofer
#   coaxial   | activebass
#   midrange  | amp
#   tweeter   | damping
FAMILIES = [
    ('component', 'Component speakers', 10),
    ('subwoofer', 'Subwoofers', 8),
    ('coaxial', 'Coaxial speakers', 6),
    ('activebass', 'Underseat subwoofers', 2),
    ('midrange', 'Mid &amp; full-range', 2),
    ('amp', 'DSP &amp; amplifiers', 1),
    ('tweeter', 'Tweeters', 1),
    ('damping', 'Damping &amp; insulation', None),
]

# the damping line is a request, not a catalogue family
FAMILY_HREF = {'damping': 'contact.html?topic=damping'}

TOTAL = sum(f[2] for f in FAMILIES if f[2])
CATEGORIES = len(FAMILIES)


def fam_href(key):
    return FAMILY_HREF.get(key, 'products.html#%s' % key)


def nav_links(current):
    """current: 'products' | 'oem' | 'about' | 'news' | 'contact' | None"""
    fam_items = ''.join(
        '                  <a class="mega__item" href="%s"><span>%s</span><em>%s</em></a>\n'
        % (fam_href(k), label, n if n else '&mdash;')
        for k, label, n in FAMILIES)
    # quoting a specific platform is not useful on the contact page itself —
    # there the sheet request should land on the brief form instead
    sheet_href = '#brief' if current == 'contact' else 'contact.html'
    # same rule for the OEM panel: the quote CTA is the brief form on contact
    quote_href = sheet_href

    def cur(key):
        return ' data-current="page"' if current == key else ''

    return f'''    <nav class="nav__links" aria-label="Primary">
      <div class="navm" data-navm>
        <a class="navm__btn" href="products.html#catalogue" aria-expanded="false" aria-haspopup="true" aria-controls="navm-products"{cur('products')}>Products {CARET}</a>
        <div class="navm__panel navm__panel--mega" id="navm-products">
          <div class="mega">
            <div class="mega__head">
              <span class="mega__kicker">Product catalogue</span>
              <span class="mega__count">{TOTAL} platforms &middot; {CATEGORIES} categories</span>
            </div>
            <div class="mega__body">
              <div class="mega__left">
                <p class="mega__label">By family</p>
                <div class="mega__cols">
{fam_items}                </div>
                <p class="mega__note">Sizes, finishes and configurations are confirmed per model.</p>
              </div>
              <a class="mega__feat" href="product-zm-m65k.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-m65k.webp" alt="ZM-M65K 2-way + 3-way component platform" width="520" height="341"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Featured platform</span>
                  <b>ZM-M65K</b>
                  <small>6.5&Prime; &middot; 2-way + 3-way platform</small>
                </span>
                <span class="mega__go">View platform {ARROW}</span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="products.html#catalogue">All {TOTAL} platforms {ARROW}</a>
              <a href="{sheet_href}">Request a data sheet {ARROW}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="navm" data-navm>
        <a class="navm__btn" href="oem-odm.html" aria-expanded="false" aria-haspopup="true" aria-controls="navm-oem"{cur('oem')}>OEM / ODM {CARET}</a>
        <div class="navm__panel navm__panel--mega" id="navm-oem">
          <div class="mega">
            <div class="mega__head">
              <span class="mega__kicker">Development &amp; manufacturing</span>
              <span class="mega__count">7 steps &middot; 5 changeable areas</span>
            </div>
            <div class="mega__body">
              <div class="mega__left">
                <div class="mega__cols">
                  <a class="mega__item" href="oem-odm.html"><span><b>OEM / ODM overview</b><small>Define &rarr; produce</small></span><em>01</em></a>
                  <a class="mega__item" href="capabilities.html#production"><span><b>Manufacturing</b><small>Four production stages</small></span><em>02</em></a>
                  <a class="mega__item" href="oem-odm.html#process"><span><b>The seven steps</b><small>One gate per step</small></span><em>03</em></a>
                  <a class="mega__item" href="capabilities.html#quality"><span><b>Quality control</b><small>Checked before release</small></span><em>04</em></a>
                  <a class="mega__item" href="oem-odm.html#change"><span><b>What can change</b><small>Five areas per project</small></span><em>05</em></a>
                  <a class="mega__item" href="capabilities.html#certification"><span><b>Certifications</b><small>CE &middot; RoHS &middot; REACH &middot; MSDS</small></span><em>06</em></a>
                  <a class="mega__item" href="brand-studio.html"><span><b>Brand &amp; packaging</b><small>Logo, finish, artwork</small></span><em>07</em></a>
                  <a class="mega__item" href="{quote_href}"><span><b>Start a project</b><small>Three lines, one reply</small></span><em>08</em></a>
                </div>
              </div>
              <a class="mega__feat" href="capabilities.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-oem.webp" alt="Operators assembling and inspecting speakers at the Foshan plant" width="560" height="373"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Inside the plant</span>
                  <b>Foshan facility</b>
                  <small>Assembly &middot; QC &middot; final release</small>
                </span>
                <span class="mega__go">View capabilities {ARROW}</span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="capabilities.html">Manufacturing &amp; quality {ARROW}</a>
              <a href="{quote_href}">Start a project {ARROW}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="navm" data-navm>
        <a class="navm__btn" href="company.html" aria-expanded="false" aria-haspopup="true" aria-controls="navm-about"{cur('about')}>About Us {CARET}</a>
        <div class="navm__panel navm__panel--mega navm__panel--mega-end" id="navm-about">
          <div class="mega">
            <div class="mega__head">
              <span class="mega__kicker">The company</span>
              <span class="mega__count">Est. 2012 &middot; Foshan, Guangdong</span>
            </div>
            <div class="mega__body">
              <div class="mega__left">
                <div class="mega__cols mega__cols--rows3">
                  <a class="mega__item" href="company.html"><span><b>Company profile</b><small>R&amp;D to production</small></span><em>01</em></a>
                  <a class="mega__item" href="capabilities.html#production"><span><b>Manufacturing</b><small>Assembly, Foshan</small></span><em>02</em></a>
                  <a class="mega__item" href="company.html#facility"><span><b>Facility &amp; visit</b><small>Jinhai Center, Lecong</small></span><em>03</em></a>
                  <a class="mega__item" href="news.html"><span><b>Blog / News</b><small>Notes from the floor</small></span><em>04</em></a>
                  <a class="mega__item" href="capabilities.html#certification"><span><b>Certifications</b><small>CE &middot; RoHS &middot; REACH &middot; MSDS</small></span><em>05</em></a>
                  <a class="mega__item" href="contact.html"><span><b>Contact</b><small>Foshan, Guangdong</small></span><em>06</em></a>
                </div>
                <p class="mega__note">10,000 m&sup2; facility &middot; 8 product categories &middot; global aftermarket</p>
              </div>
              <a class="mega__feat" href="company.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-about.webp" alt="ZEMING engineers working on a driver design and simulations" width="560" height="373"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Since 2012</span>
                  <b>Your brand.</b>
                  <small>Our manufacturing.</small>
                </span>
                <span class="mega__go">Company profile {ARROW}</span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="company.html">About ZEMING {ARROW}</a>
              <a href="contact.html">Contact us {ARROW}</a>
            </div>
          </div>
        </div>
      </div>

      <a class="nav__link" href="news.html"{cur('news')}>Blog / News</a>
      <a class="nav__link" href="contact.html"{cur('contact')}>Contact</a>
    </nav>'''


DRAWER = '''<div class="drawer__nav">
  <details class="dacc">
    <summary><span>Products</span><span class="dacc__n">01</span></summary>
    <div class="dacc__body">
%s      <a href="products.html#catalogue" class="drawer__all"><span>All %d platforms</span><i>&rarr;</i></a>
    </div>
  </details>
  <details class="dacc">
    <summary><span>OEM / ODM</span><span class="dacc__n">02</span></summary>
    <div class="dacc__body">
      <a href="oem-odm.html"><span>OEM / ODM overview</span></a>
      <a href="oem-odm.html#process"><span>The seven steps</span></a>
      <a href="oem-odm.html#change"><span>What can change</span></a>
      <a href="capabilities.html#production"><span>Manufacturing</span></a>
      <a href="capabilities.html#quality"><span>Quality control</span></a>
      <a href="brand-studio.html"><span>Brand &amp; packaging</span></a>
    </div>
  </details>
  <details class="dacc">
    <summary><span>About Us</span><span class="dacc__n">03</span></summary>
    <div class="dacc__body">
      <a href="company.html"><span>Company profile</span></a>
      <a href="company.html#facility"><span>Facility &amp; visit</span></a>
      <a href="capabilities.html#certification"><span>Certifications</span></a>
      <a href="contact.html"><span>Contact</span></a>
    </div>
  </details>
  <a href="news.html" class="drawer__top" style="border-bottom:1px solid var(--line-d-2)">Blog / News <span>04</span></a>
  <a href="contact.html" class="drawer__top">Contact <span>05</span></a>
  <div class="drawer__cta"><a class="btn btn--brand" href="contact.html">Get an OEM/ODM Quote</a></div>
</div>
'''


def drawer_html():
    items = ''.join(
        '      <a href="%s"><span>%s</span><i>%s</i></a>\n'
        % (fam_href(k), label, n if n else '&mdash;')
        for k, label, n in FAMILIES)
    return DRAWER % (items, TOTAL)


def current_for(path):
    name = path.split('/')[-1]
    if name == 'products.html' or name.startswith('product-'):
        return 'products'
    if name in ('oem-odm.html', 'capabilities.html', 'brand-studio.html'):
        return 'oem'
    if name == 'company.html':
        return 'about'
    if name == 'news.html':
        return 'news'
    if name == 'contact.html':
        return 'contact'
    return None


def patch(path, current=None):
    s = open(path, encoding='utf-8').read()
    if current is None:
        current = current_for(path)

    # 1) desktop links
    s2, n1 = re.subn(r'    <nav class="nav__links" aria-label="Primary">.*?</nav>\n',
                     nav_links(current) + '\n', s, count=1, flags=re.S)
    if not n1:
        print('  ! nav not found:', path)
        return False

    # 2) CTA — on the contact page itself it jumps to the brief form
    cta = ('<div class="nav__cta"><a class="btn btn--brand" href="#brief">Get an OEM/ODM Quote</a></div>'
           if current == 'contact' else
           '<div class="nav__cta"><a class="btn btn--brand" href="contact.html">Get an OEM/ODM Quote</a></div>')
    s2 = re.sub(r'<div class="nav__cta"><a class="btn btn--brand" href="[^"]*"[^>]*>.*?</a></div>',
                cta, s2, count=1)

    # 3) drawer
    s2, n3 = re.subn(r'(<div class="drawer" id="drawer">\n).*?(\n\s*<div class="drawer__lang">)',
                     r'\1' + drawer_html().rstrip('\n') + r'\2', s2, count=1, flags=re.S)
    if not n3:
        print('  ! drawer not found:', path)

    open(path, 'w', encoding='utf-8').write(s2)
    return True


if __name__ == '__main__':
    files = sorted(glob.glob('*.html'))
    ok = 0
    for f in files:
        if patch(f):
            ok += 1
    print('pages patched: %d/%d' % (ok, len(files)))

    # keep the generator in sync so `python gen_catalog.py` does not revert the nav
    g = 'tools/gen_catalog.py'
    src = open(g, encoding='utf-8').read()
    src2, n1 = re.subn(r'    <nav class="nav__links" aria-label="Primary">.*?</nav>\n',
                       nav_links('products') + '\n', src, count=1, flags=re.S)
    src2 = re.sub(r'<div class="nav__cta"><a class="btn btn--brand" href="[^"]*"[^>]*>.*?</a></div>',
                  '<div class="nav__cta"><a class="btn btn--brand" href="contact.html">Get an OEM/ODM Quote</a></div>',
                  src2, count=1)
    src2, n3 = re.subn(r'(<div class="drawer" id="drawer">\n).*?(\n\s*<div class="drawer__lang">)',
                       lambda m: m.group(1) + drawer_html().rstrip('\n') + m.group(2),
                       src2, count=1, flags=re.S)
    open(g, 'w', encoding='utf-8').write(src2)
    print('generator: nav %s drawer %s' % ('ok' if n1 else 'FAIL', 'ok' if n3 else 'FAIL'))
