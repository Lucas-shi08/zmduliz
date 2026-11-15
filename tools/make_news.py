# -*- coding: utf-8 -*-
"""Build news.html (Blog / News) from the shell of company.html.

Only verified facts go in: the three notes are derived from the M65K datasheet data
and from the data policy the official site already states.
"""
import re

SRC = 'company.html'
OUT = 'news.html'

shell = open(SRC, encoding='utf-8').read()

# ---- head ----
head_re = re.compile(r'<title>.*?</title>\s*<meta name="description" content="[^"]*">', re.S)
new_head = ('<title>Blog &amp; News — Technical notes from the ZEMING plant</title>\n'
            '<meta name="description" content="Technical notes on how ZEMING car audio platforms are '
            'rated and documented, plus company announcements from Guangdong Zeming Technology Co., Ltd.">')
shell = head_re.sub(new_head, shell, count=1)

MAIN = '''<main id="main">

<section class="phero">
  <div class="wrap">
    <div class="phero__grid">
      <div>
        <p class="phero__crumb"><a href="index.html">Home</a> <span>/</span> Blog &amp; News</p>
        <h1 class="phero__h reveal">Notes on how<br>a product gets <em>documented.</em></h1>
        <p class="phero__sub reveal" style="--i:1">What a power rating actually measures, why one platform is published in two configurations, and why some data sheets carry a section with no curve in it. Written from the plant in Foshan.</p>
      </div>
      <div class="phero__aside reveal" style="--i:2">
        <div class="hero__note">
          <b>Editorial rule</b>
          Nothing published here claims a measurement we cannot send you the file for. Ask for the file and it comes with the quotation.
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="notes">

      <article class="note reveal" id="n1">
        <div class="note__no">NOTE 01<span class="note__tag">Platform<br>ZM-M65K</span></div>
        <div>
          <h2>Two configurations, one <em>basket</em></h2>
          <p>The ZM-M65K is published as two builds. <b>ZM-M65K Comp</b> is a 6.5&#8243; two-way: a pair of 165 mm woofers, a pair of tweeters, a two-way crossover. <b>ZM-M65K 3W Comp</b> is the 6.5&#8243; three-way: the same woofer pair, plus a midrange pair and a three-way crossover. Both use the same yellow-Kevlar cone, the same 90 mm ferrite motor and the same 25 mm silk-diaphragm tweeter on a neodymium magnet.</p>
          <p>What changes is the middle of the band and the network that divides it. Adding a dedicated midrange moves the handover points, so the three-way is rated higher: <b>120 W AES / 240 W program</b> against <b>90 W / 180 W</b> for the two-way. Nominal impedance stays 4 &#937; and sensitivity stays 90 dB on both.</p>
          <p>That is the whole point of publishing them together. One tooling position, two positions in a line, and no surprise when two sheets with the same prefix carry different power figures.</p>
          <p class="note__meta"><span>Source &middot; ZM-M65K datasheet</span><a href="product-zm-m65k.html">Open the sheet &rarr;</a></p>
        </div>
      </article>

      <article class="note reveal" id="n2">
        <div class="note__no">NOTE 02<span class="note__tag">Reading<br>a spec</span></div>
        <div>
          <h2>AES power and program power are two different <em>tests</em></h2>
          <p>Every power figure on our sheets carries the rating it was measured to. <b>AES power</b> is the continuous rating under a defined noise signal over a defined time. <b>Continuous program power</b> is the higher, music-like figure used across the aftermarket &mdash; on the M65K, 180 W against 90 W AES.</p>
          <p>Neither number is &ldquo;the&rdquo; power of the loudspeaker. This is where comparison usually goes wrong: a platform rated 90 W AES is not weaker than one advertised at 120 W peak, even though 120 is the larger number on the page. Put the same rating side by side, or ask which test produced it.</p>
          <p>We print both because most catalogues print one, and the one they print is usually the more flattering of the two. If a figure matters to your listing, ask us for the condition behind it before you print it on a box.</p>
          <p class="note__meta"><span>Reference &middot; ZM-M65K, 2-way and 3-way</span><a href="contact.html">Ask a technical question &rarr;</a></p>
        </div>
      </article>

      <article class="note reveal" id="n3">
        <div class="note__no">NOTE 03<span class="note__tag">Data<br>policy</span></div>
        <div>
          <h2>Why the M65K sheet has no frequency-response <em>curve</em></h2>
          <p>Open the ZM-M65K data sheet and you will find a section on frequency response and impedance with no curve drawn in it. That is deliberate. The measurement files we hold are not fully consistent between the two configurations, and a curve that is correct for the two-way would be wrong for the three-way.</p>
          <p>So the sheet says what it can support, and the curve is issued against the build you actually order &mdash; measured on the approved sample, on-axis and at 30&deg; off-axis, together with the impedance file. The same rule applies to frame drawings where the source files disagree.</p>
          <p>If a supplier sends a generic curve stapled to a catalogue sheet, it is fair to ask which build it was measured on. We would rather be asked that than be caught by it.</p>
          <p class="note__meta"><span>Source &middot; published data policy</span><a href="product-zm-m65k.html">Open the sheet &rarr;</a></p>
        </div>
      </article>

    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="newscall reveal">
      <p><b>Company news.</b> Product launches, exhibition dates and certificate renewals are posted here once the document behind them exists &mdash; no announcements before the paperwork. If you need something that has not been published yet, ask us directly and you will usually get a data sheet back.</p>
      <a class="btn btn--brand" href="contact.html">Get an OEM/ODM Quote</a>
    </div>
  </div>
</section>

</main>
'''

main_re = re.compile(r'<main id="main">.*?</main>\n', re.S)
shell, n = main_re.subn(MAIN, shell, count=1)
assert n == 1, 'main block not replaced'

open(OUT, 'w', encoding='utf-8').write(shell)
print('news.html written')
