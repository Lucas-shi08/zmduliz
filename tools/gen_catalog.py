# -*- coding: utf-8 -*-
"""ZEMING catalogue — generated strictly from _FACTS.md (no invented data).

Every model code, size, finish and specification below is copied from
zemingcaraudio.com category pages or product pages. Anything not published
there is simply absent — no dashes filled with guesses.
"""
import json
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = """<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="nav__logo" href="index.html" aria-label="ZEMING CAR AUDIO — home">
      <img class="logo-d" src="assets/img/logo-header-dark.png" alt="ZEMING" width="1172" height="240">
    </a>
    <nav class="nav__links" aria-label="Primary">
      <div class="navm" data-navm>
        <a class="navm__btn" href="products.html#catalogue" aria-expanded="false" aria-haspopup="true" aria-controls="navm-products" data-current="page">Products <svg class="navm__caret" width="9" height="5" viewBox="0 0 8 5" fill="none" aria-hidden="true"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.2"/></svg></a>
        <div class="navm__panel navm__panel--mega" id="navm-products">
          <div class="mega">
            <div class="mega__head">
              <span class="mega__kicker">Product catalogue</span>
              <span class="mega__count">30 platforms &middot; 8 categories</span>
            </div>
            <div class="mega__body">
              <div class="mega__left">
                <p class="mega__label">By family</p>
                <div class="mega__cols">
                  <a class="mega__item" href="products.html#component"><span>Component speakers</span><em>10</em></a>
                  <a class="mega__item" href="products.html#subwoofer"><span>Subwoofers</span><em>8</em></a>
                  <a class="mega__item" href="products.html#coaxial"><span>Coaxial speakers</span><em>6</em></a>
                  <a class="mega__item" href="products.html#activebass"><span>Underseat subwoofers</span><em>2</em></a>
                  <a class="mega__item" href="products.html#midrange"><span>Mid &amp; full-range</span><em>2</em></a>
                  <a class="mega__item" href="products.html#amp"><span>DSP &amp; amplifiers</span><em>1</em></a>
                  <a class="mega__item" href="products.html#tweeter"><span>Tweeters</span><em>1</em></a>
                  <a class="mega__item" href="contact.html?topic=damping"><span>Damping &amp; insulation</span><em>&mdash;</em></a>
                </div>
                <p class="mega__note">Sizes, finishes and configurations are confirmed per model.</p>
              </div>
              <a class="mega__feat" href="product-zm-m65k.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-m65k.webp" alt="ZM-M65K 2-way + 3-way component platform" width="520" height="341"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Featured platform</span>
                  <b>ZM-M65K</b>
                  <small>6.5&Prime; &middot; 2-way + 3-way platform</small>
                </span>
                <span class="mega__go">View platform <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="products.html#catalogue">All 30 platforms <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
              <a href="contact.html">Request a data sheet <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
            </div>
          </div>
        </div>
      </div>

      <div class="navm" data-navm>
        <a class="navm__btn" href="oem-odm.html" aria-expanded="false" aria-haspopup="true" aria-controls="navm-oem">OEM / ODM <svg class="navm__caret" width="9" height="5" viewBox="0 0 8 5" fill="none" aria-hidden="true"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.2"/></svg></a>
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
                  <a class="mega__item" href="contact.html"><span><b>Start a project</b><small>Three lines, one reply</small></span><em>08</em></a>
                </div>
              </div>
              <a class="mega__feat" href="capabilities.html">
                <span class="mega__shot"><img src="assets/img/opt/nav-oem.webp" alt="Operators assembling and inspecting speakers at the Foshan plant" width="560" height="373"></span>
                <span class="mega__meta">
                  <span class="mega__tag">Inside the plant</span>
                  <b>Foshan facility</b>
                  <small>Assembly &middot; QC &middot; final release</small>
                </span>
                <span class="mega__go">View capabilities <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="capabilities.html">Manufacturing &amp; quality <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
              <a href="contact.html">Start a project <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
            </div>
          </div>
        </div>
      </div>

      <div class="navm" data-navm>
        <a class="navm__btn" href="company.html" aria-expanded="false" aria-haspopup="true" aria-controls="navm-about">About Us <svg class="navm__caret" width="9" height="5" viewBox="0 0 8 5" fill="none" aria-hidden="true"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.2"/></svg></a>
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
                <span class="mega__go">Company profile <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></span>
              </a>
            </div>
            <div class="mega__foot">
              <a href="company.html">About ZEMING <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
              <a href="contact.html">Contact us <svg width="13" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.3"/></svg></a>
            </div>
          </div>
        </div>
      </div>

      <a class="nav__link" href="news.html">Blog / News</a>
      <a class="nav__link" href="contact.html">Contact</a>
    </nav>
    <div class="lang" data-lang>
      <button class="lang__btn" type="button" aria-expanded="false" aria-controls="langPanel" aria-label="Language: English">
        <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="6.4" stroke="currentColor" stroke-width="1.1"/><path d="M1.6 8h12.8M8 1.6c1.75 1.8 2.7 4 2.7 6.4S9.75 12.6 8 14.4C6.25 12.6 5.3 10.4 5.3 8S6.25 3.4 8 1.6z" stroke="currentColor" stroke-width="1.1"/></svg>
        <span class="lang__code">EN</span>
        <svg class="lang__caret" width="8" height="5" viewBox="0 0 8 5" fill="none" aria-hidden="true"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.2"/></svg>
      </button>
      <div class="lang__panel" id="langPanel" role="group" aria-label="Select language" hidden>
        <button class="lang__opt is-active" type="button" data-lang-code="en"><span class="lang__native">English</span><span class="lang__check" aria-hidden="true">\u2713</span></button>
        <button class="lang__opt" type="button" data-lang-code="zh"><span class="lang__native">\u4e2d\u6587</span><span class="lang__tag">Soon</span></button>
        <button class="lang__opt" type="button" data-lang-code="es"><span class="lang__native">Espa\u00f1ol</span><span class="lang__tag">Soon</span></button>
        <button class="lang__opt" type="button" data-lang-code="de"><span class="lang__native">Deutsch</span><span class="lang__tag">Soon</span></button>
        <button class="lang__opt" type="button" data-lang-code="fr"><span class="lang__native">Fran\u00e7ais</span><span class="lang__tag">Soon</span></button>
        <p class="lang__note" hidden></p>
      </div>
    </div>
    <div class="nav__cta"><a class="btn btn--brand" href="contact.html">Get an OEM/ODM Quote</a></div>
    <button class="nav__burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
  </div>
</header>

<div class="drawer" id="drawer">
<div class="drawer__nav">
  <details class="dacc">
    <summary><span>Products</span><span class="dacc__n">01</span></summary>
    <div class="dacc__body">
      <a href="products.html#component"><span>Component speakers</span><i>10</i></a>
      <a href="products.html#subwoofer"><span>Subwoofers</span><i>8</i></a>
      <a href="products.html#coaxial"><span>Coaxial speakers</span><i>6</i></a>
      <a href="products.html#activebass"><span>Underseat subwoofers</span><i>2</i></a>
      <a href="products.html#midrange"><span>Mid &amp; full-range</span><i>2</i></a>
      <a href="products.html#amp"><span>DSP &amp; amplifiers</span><i>1</i></a>
      <a href="products.html#tweeter"><span>Tweeters</span><i>1</i></a>
      <a href="contact.html?topic=damping"><span>Damping &amp; insulation</span><i>&mdash;</i></a>
      <a href="products.html#catalogue" class="drawer__all"><span>All 30 platforms</span><i>&rarr;</i></a>
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
  <div class="drawer__lang">
    <span class="mono">Language</span>
    <div class="lang-row">
      <button class="lang-chip is-active" type="button" data-lang-code="en">English</button>
      <button class="lang-chip" type="button" data-lang-code="zh">\u4e2d\u6587<span class="lang__tag">Soon</span></button>
      <button class="lang-chip" type="button" data-lang-code="es">Espa\u00f1ol<span class="lang__tag">Soon</span></button>
      <button class="lang-chip" type="button" data-lang-code="de">Deutsch<span class="lang__tag">Soon</span></button>
      <button class="lang-chip" type="button" data-lang-code="fr">Fran\u00e7ais<span class="lang__tag">Soon</span></button>
    </div>
    <p class="lang__note" hidden></p>
  </div>
  <div class="drawer__foot">
    <span class="mono">inquiry@zemingcaraudio.com</span>
    <span class="mono">+86 188 2489 7798 · WhatsApp</span>
    <span class="mono">Foshan, Guangdong, China</span>
  </div>
</div>"""

FOOT = """<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <div class="foot__logo"><img src="assets/img/logo-footer-dark.png" alt="ZEMING" width="1220" height="240"></div>
        <p class="foot__blurb">Guangdong Zeming Technology Co., Ltd. Car audio OEM / ODM development and manufacturing. Foshan, Guangdong, China.</p>
        <p class="mono mt-4" style="color:#7FA8E8">Your brand. Our manufacturing.</p>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
          <li><a href="products.html#component">Component speakers</a></li>
          <li><a href="products.html#coaxial">Coaxial speakers</a></li>
          <li><a href="products.html#subwoofer">Subwoofers</a></li>
          <li><a href="products.html#activebass">Underseat subwoofers</a></li>
          <li><a href="products.html#amp">DSP &amp; amplifiers</a></li>
          <li><a href="products.html">Damping materials</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="capabilities.html">Manufacturing &amp; quality</a></li>
          <li><a href="oem-odm.html">OEM / ODM</a></li>
          <li><a href="brand-studio.html">Brand &amp; packaging</a></li>
          <li><a href="company.html">About ZEMING</a></li>
          <li><a href="news.html">Blog &amp; News</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Talk to us</h4>
        <ul>
          <li><a href="mailto:inquiry@zemingcaraudio.com">inquiry@zemingcaraudio.com</a></li>
          <li><a href="https://wa.me/8618824897798" target="_blank" rel="noopener">WhatsApp +86 188 2489 7798</a></li>
          <li><a href="contact.html">Request a quotation</a></li>
        </ul>
        <p class="small-note mt-4" style="color:#6E767B">Jinhai Center, No. 110 Yuhe Road,<br>Lecong Town, Shunde District,<br>Foshan, Guangdong, China</p>
      </div>
    </div>
    <div class="foot__bottom">
      <span>© 2026 Guangdong Zeming Technology Co., Ltd.</span>
      <div>
        <a href="company.html">Certifications</a>
        <a href="contact.html">Privacy</a>
        <a href="index.html">EN</a>
      </div>
    </div>
  </div>
</footer>"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/catalog.css">
<link rel="icon" href="assets/img/logo-header.png">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

FAMILIES = [
    ('all', 'All platforms'),
    ('component', 'Component'),
    ('coaxial', 'Coaxial'),
    ('tweeter', 'Tweeter'),
    ('midrange', 'Mid &amp; full-range'),
    ('subwoofer', 'Subwoofer'),
    ('activebass', 'Underseat'),
    ('amp', 'DSP &amp; amp'),
]

FAM_LABEL = {
    'component': 'Component speaker', 'coaxial': 'Coaxial speaker', 'tweeter': 'Tweeter',
    'midrange': 'Mid &amp; full-range', 'subwoofer': 'Subwoofer', 'activebass': 'Underseat subwoofer',
    'amp': 'DSP &amp; amplifier',
}

PIC_DIR = os.path.join(OUT, 'assets', 'img', 'pic')


def imgfile(n):
    base = os.path.splitext(n)[0]
    for ext in ('.jpg', '.png'):
        if os.path.exists(os.path.join(PIC_DIR, base + ext)):
            return base + ext
    return n


def slug(m):
    return m.lower().replace('.', '-').replace(' ', '-').replace('/', '-').replace('+', 'and')


# ---------------------------------------------------------------- models
# card rows only contain attributes published on zemingcaraudio.com
M = []


def add(**kw):
    M.append(kw)


# Component speakers — /products/component-speaker (10 platforms)
add(model='ZM-E65G', fam='component', name='6.5″ two-way component system',
    card=[('Size', '6.5″'), ('System', '2-way component')], img='p-component',
    blurb='6.5-inch 2-way component system. Source-backed platform for distribution and private-label programmes.')
add(model='ZM-C65A', fam='component', name='6.5″ two-way component system',
    card=[('Size', '6.5″'), ('System', '2-way component')], img='p-component',
    blurb='6.5-inch 2-way component system listed by ZEMING as a component speaker platform.')
add(model='ZM-C65CR + ZM-C69CR', fam='component', name='6.5″ + 6×9″ component series',
    card=[('Sizes', '6.5″ · 6×9″'), ('System', 'Component series')], img='p-component',
    blurb='Two component sizes offered as one series, for programmes that need a matching 6.5-inch and 6×9-inch pair.')
add(model='ZM-M65P', fam='component', name='6.5″ two-way component system',
    card=[('Size', '6.5″'), ('System', '2-way component')], img='m65k-2way',
    blurb='6.5-inch 2-way component system; the same platform code appears in the coaxial range with a blue PP cone.')
add(model='ZM-M65C', fam='component', name='6.5″ two-way component system',
    card=[('Size', '6.5″'), ('System', '2-way component')], img='m65k-2way',
    blurb='6.5-inch 2-way component system; the coaxial version of this platform uses a carbon-fibre cone.')
add(model='ZM-M65K', fam='component', name='2-way + 3-way component platform', flagship=True,
    detail='m65k', img='p-component',
    card=[('Size', '6.5″'), ('AES power', '90 / 120 W'), ('Sensitivity', '90 dB'), ('Impedance', '4 Ω')],
    blurb='One platform, two confirmed configurations: a 2-way set and a 3-way set, each with its own supplied parts and published data.')
add(model='ZM-X65W', fam='component', name='2-way + 3-way component platform',
    card=[('Size', '6.5″'), ('System', '2-way / 3-way')], img='m65k-3way',
    blurb='Component platform offered in 2-way and 3-way configurations.')
add(model='ZM-X65W V2', fam='component', name='2-way + 3-way component platform',
    card=[('Size', '6.5″'), ('System', '2-way / 3-way'), ('Version', 'V2')], img='m65k-3way',
    blurb='The V2 revision of the X65W component platform.')
add(model='ZM-X65C-3W', fam='component', name='6.5″ three-way component system',
    card=[('Size', '6.5″'), ('System', '3-way component')], img='m65k-3way',
    blurb='6.5-inch three-way component system for programmes that need a dedicated midrange.')
add(model='ZM-X65UC-3W', fam='component', name='6.5″ three-way component system',
    card=[('Size', '6.5″'), ('System', '3-way component'), ('Variant', 'UC')], img='m65k-3way',
    blurb='6.5-inch three-way component system, UC variant of the X65 series.')

# Coaxial — /products/coaxial-speaker (6 models)
add(model='ZM-E525P', fam='coaxial', name='5.25″ two-way coaxial',
    card=[('Size', '5.25″'), ('System', '2-way coaxial')], img='p-coaxial',
    blurb='5.25-inch 2-way coaxial speaker.')
add(model='ZM-C65A', fam='coaxial', name='6.5″ coaxial · gold aluminium',
    card=[('Size', '6.5″'), ('Finish', 'Gold aluminium')], img='p-coaxial',
    blurb='6.5-inch coaxial with a gold aluminium cone finish.')
add(model='ZM-C65CR', fam='coaxial', name='6.5″ coaxial · red &amp; black carbon fibre',
    card=[('Size', '6.5″'), ('Finish', 'Red &amp; black carbon fibre')], img='p-coaxial',
    blurb='6.5-inch coaxial in the red and black carbon-fibre finish.')
add(model='ZM-C69CR', fam='coaxial', name='6×9″ coaxial · red &amp; black carbon fibre',
    card=[('Size', '6×9″'), ('Finish', 'Red &amp; black carbon fibre')], img='p-coaxial',
    blurb='6×9-inch coaxial in the red and black carbon-fibre finish.')
add(model='ZM-M65P', fam='coaxial', name='6.5″ coaxial · blue PP cone',
    card=[('Size', '6.5″'), ('Cone', 'Blue PP')], img='p-coaxial',
    blurb='6.5-inch coaxial with a blue polypropylene cone.')
add(model='ZM-M65C', fam='coaxial', name='6.5″ coaxial · carbon fibre',
    card=[('Size', '6.5″'), ('Cone', 'Carbon fibre')], img='p-coaxial',
    blurb='6.5-inch coaxial with a carbon-fibre cone.')

# Tweeter
add(model='ZM-CT28', fam='tweeter', name='car tweeter',
    card=[('Model', 'ZM-CT28'), ('Type', 'Tweeter')], img='cat-tweeter',
    blurb='Tweeter platform listed in the current ZEMING catalogue.')

# Mid & full-range
add(model='ZM-CF35-P-AL', fam='midrange', name='3.5″ aluminium full-range',
    card=[('Size', '3.5″'), ('Type', 'Full-range'), ('Cone', 'Aluminium')], img='cat-midrange',
    blurb='3.5-inch panoramic super aluminium full-range speaker.')
add(model='ZM-PM65-NB / ZM-PM80-NB', fam='midrange', name='6.5″ / 8″ mid-range',
    card=[('Sizes', '6.5″ · 8″'), ('Type', 'Mid-range'), ('Cone', 'Carbon fibre · neo')], img='cat-midrange',
    blurb='Carbon-fibre cone mid-range with neodymium motor, offered in 6.5-inch and 8-inch.')

# Subwoofers
add(model='ZM-CB10C', fam='subwoofer', name='10″ chrome-plated DVC subwoofer',
    card=[('Size', '10″'), ('Series', 'Chrome-plated DVC')], img='sub-chrome',
    blurb='Chrome-plated dual voice coil subwoofer series.')
add(model='ZM-CB12C', fam='subwoofer', name='12″ chrome-plated DVC subwoofer',
    card=[('Size', '12″'), ('Series', 'Chrome-plated DVC')], img='sub-chrome',
    blurb='Chrome-plated dual voice coil subwoofer series.')
add(model='ZM-CB15C', fam='subwoofer', name='15″ chrome-plated DVC subwoofer',
    card=[('Size', '15″'), ('Series', 'Chrome-plated DVC')], img='sub-chrome',
    blurb='Chrome-plated dual voice coil subwoofer series.')
add(model='ZM-ES140-SQ', fam='subwoofer', name='square subwoofer · 140',
    card=[('Model', 'ZM-ES140-SQ'), ('Series', 'Square subwoofer')], img='sub-square',
    blurb='Square car subwoofer series.')
add(model='ZM-ES170-SQ', fam='subwoofer', name='square subwoofer · 170',
    card=[('Model', 'ZM-ES170-SQ'), ('Series', 'Square subwoofer')], img='sub-square',
    blurb='Square car subwoofer series.')
add(model='ZM-CB10P', fam='subwoofer', name='10″ high-output subwoofer',
    card=[('Size', '10″'), ('Series', 'High-output')], img='p-subwoofer',
    blurb='High-output subwoofer platform.')
add(model='ZM-CB12P', fam='subwoofer', name='12″ high-output subwoofer',
    card=[('Size', '12″'), ('Series', 'High-output')], img='p-subwoofer',
    blurb='High-output subwoofer platform.')
add(model='ZM-CB15P', fam='subwoofer', name='15″ high-output subwoofer',
    card=[('Size', '15″'), ('Series', 'High-output')], img='p-subwoofer',
    blurb='High-output subwoofer platform.')

# Underseat
add(model='ZM-6.5C01-P', fam='activebass', name='6.5″ active underseat subwoofer',
    card=[('Driver', '6.5″'), ('Type', 'Active, built-in amplifier')], img='cat-activebass',
    blurb='6.5-inch active underseat subwoofer with a built-in amplifier, flexible signal inputs and a slim format.')
add(model='ZM-SL8C', fam='activebass', name='8″ active underseat subwoofer', detail='sl8c', img='cat-activebass',
    card=[('Driver', '8″'), ('Power', '180 W RMS'), ('Response', '20–150 Hz'), ('Enclosure', '33 × 22 × 8 cm')],
    blurb='8-inch active underseat subwoofer with 180 W RMS power, 20 Hz–150 Hz response and a 33 × 22 × 8 cm enclosure.')

# Amplifier
add(model='ZM-D8000.1', fam='amp', name='8000 W monoblock amplifier', detail='d8000', img='amp-d8000',
    card=[('Type', 'Monoblock'), ('Max power', '8000 W'), ('Min impedance', '1 Ω'), ('Cooling', 'Dual fan')],
    blurb='8000 W high-power monoblock car amplifier with 1 Ω minimum impedance, adjustable controls and dual-fan cooling.')


def card_rows(rows):
    return ''.join('<div class="pcard__spec"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in rows)


def prow(rows):
    return ''.join('<div class="prow"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in rows)


CMP_UI = """
<div class="cmpbar" id="cmpbar" hidden>
  <div class="wrap cmpbar__in">
    <span class="cmpbar__label">Compare</span>
    <div class="cmpbar__slots" id="cmpslots"></div>
    <div class="cmpbar__actions">
      <button class="btn btn--ghost" type="button" id="cmpclear">Clear</button>
      <button class="btn btn--brand" type="button" id="cmpopen" disabled>Select one more</button>
    </div>
  </div>
</div>

<div class="cmptoast" id="cmptoast" role="status" aria-live="polite"></div>

<div class="cmpmodal" id="cmpmodal" hidden>
  <div class="cmpmodal__scrim" data-close></div>
  <div class="cmpmodal__panel" role="dialog" aria-modal="true" aria-labelledby="cmptitle">
    <div class="cmpmodal__head">
      <h2 id="cmptitle">Compare platforms</h2>
      <label class="cmponly">
        <input type="checkbox" id="cmpdiff">
        <span class="cmponly__box" aria-hidden="true"></span>
        <span>Only show differences</span>
      </label>
      <button class="cmpmodal__close" type="button" data-close aria-label="Close comparison">Close</button>
    </div>
    <div class="cmpmodal__body" id="cmpbody"></div>
  </div>
</div>
"""


# ---------------------------------------------------------------- listing
def build_listing():
    chips = []
    for key, label in FAMILIES:
        n = len(M) if key == 'all' else len([p for p in M if p['fam'] == key])
        chips.append('<button class="cf-chip" data-fam="%s" aria-pressed="%s">%s <b>%d</b></button>'
                     % (key, 'true' if key == 'all' else 'false', label, n))

    cards = []
    for p in M:
        has_page = 'detail' in p
        cta = ('<span class="pcard__more">Datasheet'
               '<svg width="12" height="9" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg></span>'
               if has_page else '<span class="pcard__more pcard__more--req">Request data</span>')
        href = 'product-%s.html' % slug(p['model']) if has_page else 'contact.html?model=%s' % p['model']
        cards.append("""<div class="pcard" data-fam="{fam}" data-search="{model} {name} {famlabel}">
        <a class="pcard__hit" href="{href}" aria-label="{model} {name}"></a>
        <div class="pcard__img"><span class="pcard__fam">{famlabel}</span>
          <button class="pcard__cmp" type="button" data-model="{model}" aria-pressed="false" aria-label="Add {model} to comparison">
            <span class="pcard__cmp-box" aria-hidden="true"></span>
          </button>
          <img src="assets/img/pic/{img}" alt="{model} {name}" loading="lazy" width="1200" height="1200"></div>
        <div class="pcard__code">{model}</div>
        <div class="pcard__name">{name}</div>
        <dl class="pcard__specs">{rows}</dl>
        <div class="pcard__foot">
          {cta}
          <a class="pcard__quote" href="contact.html?model={model}">Quote</a>
        </div>
      </div>""".format(fam=p['fam'], model=p['model'], name=p['name'], href=href,
                       famlabel=FAM_LABEL[p['fam']], img=imgfile(p['img']),
                       rows=card_rows(p['card']), cta=cta))

    html = HEAD.format(
        title='Products — ZEMING car audio platforms',
        desc='ZEMING car audio platforms: component and coaxial speakers, tweeters, mid and full-range, subwoofers, underseat subwoofers and DSP amplifiers. Parameters are confirmed against the selected model before quotation.'
    ) + NAV + """
<main id="main">

<section class="phero">
  <div class="wrap">
    <div class="phero__grid">
      <div>
        <p class="phero__crumb"><a href="index.html">Home</a> <span>/</span> Products</p>
        <h1 class="phero__h reveal">Platforms ready<br>for your <em>market.</em></h1>
        <p class="phero__sub reveal" style="--i:1">Thirty platforms across seven families. Filter by family or search a model code. Final specifications, fitment and packaging are confirmed against the selected model before quotation.</p>
      </div>
      <div class="phero__aside reveal" style="--i:2">
        <div class="hero__note">
          <b>Only published values are shown</b>
          Where a parameter is not confirmed for a platform it is left out rather than estimated. Ask us and we will send the current data sheet for that model.
        </div>
      </div>
    </div>
  </div>
</section>

<div class="filterbar" id="catalogue">
  <div class="wrap filterbar__in">
    <div class="cf-chips" role="group" aria-label="Filter by product family">
      %s
    </div>
    <div class="cf-search">
      <label class="sr-only" for="cf-q">Search a model or product name</label>
      <input id="cf-q" type="search" placeholder="Search model…" autocomplete="off">
      <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="5" stroke="#9BA3A7" stroke-width="1.3"/><path d="M11 11l4 4" stroke="#9BA3A7" stroke-width="1.3"/></svg>
    </div>
  </div>
</div>

<section class="section section--tight">
  <div class="wrap">
    <span class="cf-count">30 of 30 platforms shown</span>
    <div class="catgrid">
      %s
    </div>
    <p class="noresult">No platform matches that filter. Try another family, or <a href="contact.html" style="color:#7FA8E8">ask us directly</a>.</p>

    <p class="small-note mt-6">No unverified parameter is treated as an approved specification. Damping and insulation materials are handled as a project category — ask us for the current range.</p>
  </div>
</section>

<section class="cta-band">
  <img class="cta-band__bg" src="assets/img/pic/scene-package.jpg" alt="" loading="lazy" aria-hidden="true">
  <div class="wrap cta-band__in">
    <p class="eyebrow reveal">Next step</p>
    <h2 class="h-1 mt-4 reveal" style="--i:1">Need a platform<br>that is <em>not here?</em></h2>
    <p class="lead mt-5 reveal" style="--i:2">Send the market, price position and configuration you need. We will tell you which platform fits and what can be changed.</p>
    <div class="btn-row mt-6 reveal" style="--i:3">
      <a class="btn btn--brand btn--lg" href="contact.html">Start a project
        <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg>
      </a>
      <a class="btn btn--ghost btn--lg" href="oem-odm.html">How customisation works</a>
    </div>
  </div>
</section>

</main>
""" % ('\n      '.join(chips), '\n      '.join(cards))

    html = html.replace('</main>', '</main>\n' + CMP_UI)

    data = []
    for p in M:
        data.append({
            'm': p['model'], 'f': p['fam'], 'fl': FAM_LABEL[p['fam']].replace('&amp;', '&'),
            'n': p['name'], 'img': imgfile(p['img']),
            'u': 'product-%s.html' % slug(p['model']) if 'detail' in p else 'contact.html?model=%s' % p['model'],
            'rows': [list(r) for r in p['card']],
        })
    cmp_script = '<script type="application/json" id="cmpdata">%s</script>\n' % json.dumps(data, ensure_ascii=False)

    html = html + FOOT + cmp_script + '<script src="assets/site.js"></script>\n<script src="assets/catalog.js"></script>\n</body>\n</html>\n'
    open(os.path.join(OUT, 'products.html'), 'w', encoding='utf-8').write(html)


# ---------------------------------------------------------------- datasheets
DETAIL = {
    'm65k': dict(
        model='ZM-M65K',
        title='ZM-M65K — 2-way + 3-way component platform | ZEMING',
        desc='ZM-M65K component platform: 2-way and 3-way configurations with AES power, program power, impedance and sensitivity as published by ZEMING.',
        eyebrow='Component speaker · 6.5″ platform',
        name='2-way + 3-way component platform',
        blurb='One platform, two confirmed configurations. Each keeps its own supplied parts and its own published performance data — the 2-way set and the 3-way set are quoted as separate positions, not as options on one specification.',
        gallery=['p-component', 'm65k-2way', 'm65k-3way', 'm65k-crossover'],
        cfg=[
            ('Model', 'ZM-M65K Comp', 'ZM-M65K 3W Comp'),
            ('System architecture', '6.5-inch 2-way component system', '6.5-inch 3-way component system'),
            ('Supplied components', 'Woofer pair + tweeter pair + 2-way crossover pair', 'Woofer pair + midrange pair + tweeter pair + 3-way crossover pair'),
            ('AES power handling', '90 W', '120 W'),
            ('Continuous program power', '180 W', '240 W'),
            ('Nominal impedance', '4 Ω', '4 Ω'),
            ('Sensitivity', '90 dB', '90 dB'),
            ('Woofer cone', 'Yellow Kevlar fibre', 'Yellow Kevlar fibre'),
            ('Woofer magnet', 'Ferrite · 90 mm', 'Ferrite · 90 mm'),
            ('Tweeter', '25 mm silk diaphragm · neodymium', '25 mm silk diaphragm · neodymium'),
        ],
        note='Frequency-response and frame descriptions are not published for this platform: the current source files are not fully consistent across configurations. Final production follows the approved sample.',
    ),
    'sl8c': dict(
        model='ZM-SL8C',
        title='ZM-SL8C — 8″ active underseat subwoofer | ZEMING',
        desc='ZM-SL8C active underseat subwoofer: 180 W RMS, 20–150 Hz, 95 dB sensitivity, 33 × 22 × 8 cm enclosure.',
        eyebrow='Underseat subwoofer · active',
        name='8″ active underseat subwoofer',
        blurb='An 8-inch active underseat subwoofer with a built-in amplifier, flexible signal inputs and a slim format. The values below follow the current ZEMING product catalogue.',
        gallery=['cat-activebass'],
        rows=[('Power', '180 W RMS / 360 W PMPO'), ('Frequency response', '20 Hz – 150 Hz'),
              ('Sensitivity', '95 dB'), ('Bass boost', '0 – 12 dB'),
              ('Input sensitivity', '110 mV – 4 V'), ('Fuse', '20 A'),
              ('Driver', '8″ subwoofer'), ('Enclosure', '33 × 22 × 8 cm')],
        note='Final order specifications remain subject to the approved sample and project document.',
    ),
    'd8000': dict(
        model='ZM-D8000.1',
        title='ZM-D8000.1 — 8000 W monoblock amplifier | ZEMING',
        desc='ZM-D8000.1 monoblock car amplifier: 8000 W maximum power, 1 Ω minimum impedance, dual-fan cooling, brushed aluminium housing.',
        eyebrow='DSP &amp; amplifier · monoblock',
        name='8000 W monoblock amplifier',
        blurb='A high-power monoblock for serious bass systems, with adjustable controls on the front panel and dual-fan cooling. OEM / ODM support is available on this platform.',
        gallery=['amp-d8000', 'p-amp'],
        rows=[('Product type', 'Monoblock car amplifier'), ('Maximum power', '8000 W'),
              ('Minimum impedance', '1 Ω'), ('Input', 'RCA input / RCA output'),
              ('Controls', 'HPF / LPF / Gain / Bass boost'), ('Cooling', 'Dual fan cooling'),
              ('Housing', 'Brushed aluminium shell'), ('Power terminals', '+12V / REM / GND'),
              ('Application', 'Aftermarket car audio system'), ('OEM / ODM', 'Supported')],
        note='Published values are the current catalogue specifications; the approved sample governs the order.',
    ),
}


def build_detail(key, d):
    rel = [p for p in M if p['fam'] == 'component' and p['model'] != d['model']][:3]
    gal = d['gallery']
    thumbs = ''.join(
        '<button class="ds-thumb" data-src="assets/img/pic/%s" aria-pressed="%s" aria-label="View image %d">'
        '<img src="assets/img/pic/%s" alt="" loading="lazy"></button>'
        % (imgfile(g), 'true' if i == 0 else 'false', i + 1, imgfile(g)) for i, g in enumerate(gal))

    if key == 'm65k':
        head = ('<tr><th scope="col">Specification</th><th scope="col">2-Way<span>ZM-M65K Comp</span></th>'
                '<th scope="col">3-Way<span>ZM-M65K 3W Comp</span></th></tr>')
        body = ''.join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % r for r in d['cfg'])
        specs = ('<div class="ds-table-wrap"><table class="cmptable ds-cfg"><thead>%s</thead><tbody>%s</tbody></table></div>'
                 % (head, body))
    else:
        specs = '<div class="pgrid">%s</div>' % prow(d['rows'])

    def rel_href(x):
        return ('product-%s.html' % slug(x['model'])) if 'detail' in x else ('contact.html?model=%s' % x['model'])

    relhtml = ''.join(
        '<a class="relcard" href="%s"><span class="relcard__img"><img src="assets/img/pic/%s" alt="" loading="lazy"></span>'
        '<span><span class="relcard__code">%s</span><span class="relcard__name">%s</span></span></a>'
        % (rel_href(x), imgfile(x['img']), x['model'], x['name']) for x in rel)

    html = HEAD.format(title=d['title'], desc=d['desc']) + NAV + """
<main id="main">

<section class="phero phero--crumb">
  <div class="wrap">
    <p class="phero__crumb"><a href="index.html">Home</a> <span>/</span> <a href="products.html">Products</a> <span>/</span> <a href="products.html#component">%s</a> <span>/</span> %s</p>
  </div>
</section>

<section class="section" style="padding-top:clamp(18px,3vw,30px)">
  <div class="wrap">
    <div class="ds-top">
      <div class="ds-gallery reveal">
        <div class="ds-gallery__main"><img src="assets/img/pic/%s" alt="%s %s" width="1200" height="1200"></div>
        <div class="ds-thumbs">%s</div>
      </div>
      <div class="reveal" style="--i:1">
        <p class="ds-eyebrow">%s</p>
        <h1 class="ds-model">%s</h1>
        <p class="ds-name">%s</p>
        <p class="ds-blurb">%s</p>
        <p class="ds-flag">Published catalogue data — the approved sample governs the order.</p>
        <div class="ds-actions">
          <a class="btn btn--brand" href="contact.html?model=%s">Request the data sheet
            <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M1 5h12" stroke="currentColor" stroke-width="1.4"/></svg>
          </a>
          <a class="btn btn--ghost" href="oem-odm.html">Discuss customisation</a>
        </div>
      </div>
    </div>

    <nav class="ds-nav" aria-label="Datasheet sections">
      <a href="#specs">Specifications</a>
      <a href="#custom">Customisation</a>
      <a href="#related">Related platforms</a>
    </nav>

    <section class="ds-sec" id="specs">
      <h2><span>01</span>Specifications</h2>
      %s
      <p class="ds-note">%s</p>
    </section>

    <section class="ds-sec" id="custom">
      <h2><span>02</span>Customisation</h2>
      <p class="body-copy" style="max-width:64ch">Branding, appearance, acoustic tuning and packaging are reviewed per project. Logo, finish, accessories, housing and interface options are confirmed for feasibility before sampling.</p>
      <div class="pill-row mt-5">
        <span class="pill">Branding</span><span class="pill">Appearance</span><span class="pill">Acoustic tuning</span>
        <span class="pill">Packaging</span><span class="pill">Accessories</span>
      </div>
      <div class="btn-row mt-6">
        <a class="btn btn--brand" href="contact.html?model=%s">Discuss this platform</a>
        <a class="btn btn--ghost" href="oem-odm.html">OEM / ODM process</a>
      </div>
    </section>

    <section class="ds-sec" id="related">
      <h2><span>03</span>Related platforms</h2>
      <div class="relgrid">%s</div>
    </section>
  </div>
</section>

</main>
""" % (FAM_LABEL['component'], d['model'], imgfile(gal[0]), d['model'], d['name'], thumbs,
       d['eyebrow'], d['model'], d['name'], d['blurb'], d['model'],
       specs, d['note'], d['model'], relhtml) + FOOT + '<script src="assets/site.js"></script>\n<script src="assets/catalog.js"></script>\n</body>\n</html>\n'

    open(os.path.join(OUT, 'product-%s.html' % slug(d['model'])), 'w', encoding='utf-8').write(html)


build_listing()
for k, d in DETAIL.items():
    build_detail(k, d)

print('catalogue rebuilt: %d platforms, %d datasheets' % (len(M), len(DETAIL)))
