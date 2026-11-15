/* ZEMING site interactions */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- nav: stuck state (theme aware) ---------- */
  var nav = document.querySelector('.nav');
  var lightTop = document.body.classList.contains('is-light');
  function onScroll() {
    if (!nav) return;
    if (window.scrollY > 24) {
      nav.classList.add(lightTop ? 'is-light-stuck' : 'is-stuck');
      nav.classList.remove(lightTop ? 'is-stuck' : 'is-light-stuck');
    } else {
      nav.classList.remove('is-stuck', 'is-light-stuck');
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = document.querySelector('.nav__burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.documentElement.style.overflow = open ? 'hidden' : '';
    });
    document.querySelectorAll('.drawer a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
        document.documentElement.style.overflow = '';
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  var io = null;
  if (!reduce && 'IntersectionObserver' in window) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- number count-up ---------- */
  function fmt(v, dec) {
    if (dec) return v.toFixed(dec);
    return v >= 1000 ? Math.round(v).toLocaleString('en-US') : String(Math.round(v));
  }
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var dec = (el.getAttribute('data-dec') | 0);
    var dur = 1100, t0 = performance.now();
    if (reduce) { el.textContent = fmt(target, dec); return; }
    function tick(t) {
      var p = Math.min(1, (t - t0) / dur);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * e, dec);
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = fmt(target, dec);
    }
    requestAnimationFrame(tick);
  }
  if (!reduce && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { countUp(en.target); cio.unobserve(en.target); }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });
  } else {
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var d = (el.getAttribute('data-dec') | 0);
      el.textContent = fmt(parseFloat(el.getAttribute('data-count')), d);
    });
  }

  /* ---------- product filter ---------- */
  var filters = document.querySelectorAll('.filter');
  var items = document.querySelectorAll('[data-cat]');
  if (filters.length && items.length) {
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filters.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var f = btn.getAttribute('data-filter');
        items.forEach(function (it) {
          var show = f === 'all' || it.getAttribute('data-cat') === f;
          it.style.display = show ? '' : 'none';
        });
      });
    });
  }

  /* ---------- subnav scroll spy ---------- */
  var subLinks = document.querySelectorAll('.subnav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var secs = Array.prototype.map.call(subLinks, function (a) {
      return document.querySelector(a.getAttribute('href'));
    });
    var sio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) {
          subLinks.forEach(function (a) { a.classList.remove('active'); });
          var idx = secs.indexOf(en.target);
          if (idx > -1) subLinks[idx].classList.add('active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secs.forEach(function (s) { if (s) sio.observe(s); });
  }

  /* ---------- inquiry form ---------- */
  var form = document.querySelector('form[data-inquiry]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var missing = false;
      form.querySelectorAll('[required]').forEach(function (f) {
        if (!f.value.trim()) {
          missing = true;
          f.style.borderColor = '#C4553A';
          f.addEventListener('input', function () { f.style.borderColor = ''; }, { once: true });
        }
      });
      if (missing) return;
      var ok = document.querySelector('.form-ok');
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      setTimeout(function () {
        form.style.display = 'none';
        if (ok) { ok.classList.add('show'); ok.focus(); }
      }, 700);
    });
  }

  /* ---------- curve draw ---------- */
  var curves = document.querySelectorAll('[data-draw] path');
  if (curves.length && !reduce && 'IntersectionObserver' in window) {
    curves.forEach(function (p) {
      var len = p.getTotalLength ? p.getTotalLength() : 0;
      if (!len) return;
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
    });
    var dio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.querySelectorAll('path').forEach(function (p, i) {
            p.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(.16,1,.3,1) ' + (i * 160) + 'ms';
            p.style.strokeDashoffset = 0;
          });
          dio.unobserve(en.target);
        }
      });
    }, { threshold: 0.35 });
    document.querySelectorAll('[data-draw]').forEach(function (s) { dio.observe(s); });
  }
})();

/* ---------- language switcher ---------- */
(function () {
  'use strict';
  var roots = document.querySelectorAll('[data-lang]');
  if (!roots.length) return;

  var NOTES = {
    zh: 'Chinese edition is in preparation — English content is shown for now. Mention 中文 in your enquiry and we will reply in Chinese.',
    es: 'Spanish edition is in preparation — English content is shown for now. Mention Español in your enquiry and we will reply in Spanish.',
    de: 'German edition is in preparation — English content is shown for now. Mention Deutsch in your enquiry and we will reply in German.',
    fr: 'French edition is in preparation — English content is shown for now. Mention Français in your enquiry and we will reply in French.'
  };

  function closeAll() {
    Array.prototype.forEach.call(roots, function (r) {
      var b = r.querySelector('.lang__btn');
      var p = r.querySelector('.lang__panel');
      if (b) b.setAttribute('aria-expanded', 'false');
      if (p) p.hidden = true;
    });
  }

  function handle(opt) {
    var code = opt.getAttribute('data-lang-code');
    if (!code || opt.classList.contains('is-active')) { closeAll(); return; }
    var scope = opt.closest('[data-lang]');
    var note = scope ? scope.querySelector('.lang__note')
                     : document.querySelector('.drawer__lang .lang__note');
    if (note) {
      note.textContent = NOTES[code] || 'This edition is in preparation.';
      note.hidden = false;
    }
  }

  Array.prototype.forEach.call(roots, function (root) {
    var btn = root.querySelector('.lang__btn');
    var panel = root.querySelector('.lang__panel');
    var note = root.querySelector('.lang__note');
    if (!btn || !panel) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = panel.hidden;
      closeAll();
      panel.hidden = !willOpen;
      btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      if (willOpen && note) note.hidden = true;
    });

    panel.addEventListener('click', function (e) {
      e.stopPropagation();
      var opt = e.target.closest ? e.target.closest('[data-lang-code]') : null;
      if (opt) handle(opt);
    });
  });

  document.addEventListener('click', function (e) {
    var chip = e.target.closest ? e.target.closest('.drawer__lang [data-lang-code]') : null;
    if (chip) { handle(chip); return; }
    if (!e.target.closest || !e.target.closest('[data-lang]')) closeAll();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll();
  });
})();

/* ---------- primary nav: dropdowns ---------- */
(function () {
  'use strict';
  var groups = Array.prototype.slice.call(document.querySelectorAll('[data-navm]'));
  if (!groups.length) return;

  var hoverable = window.matchMedia && window.matchMedia('(hover: hover) and (min-width: 1000px)').matches;
  var closeTimer = null;
  /* set while we move focus ourselves, so the focusin handler does not
     immediately re-open the panel we just closed on Escape */
  var skipFocusOpen = false;
  /* focus arrives from a mouse click too — only keyboard focus should reveal the
     panel, otherwise the menu flashes open for a frame before the link navigates */
  var keyboardFocus = false;
  document.addEventListener('keydown', function () { keyboardFocus = true; }, true);
  document.addEventListener('mousedown', function () { keyboardFocus = false; }, true);
  document.addEventListener('touchstart', function () { keyboardFocus = false; }, true);

  function setState(g, open) {
    var btn = g.querySelector('.navm__btn');
    var panel = g.querySelector('.navm__panel');
    if (!btn || !panel) return;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) panel.setAttribute('data-open', 'true');
    else panel.removeAttribute('data-open');
  }

  function closeAll(except) {
    groups.forEach(function (g) { if (g !== except) setState(g, false); });
  }

  groups.forEach(function (g) {
    var btn = g.querySelector('.navm__btn');
    var panel = g.querySelector('.navm__panel');
    if (!btn || !panel) return;

    /* The label is a real link to the overview page, so a plain click navigates.
       The panel is a hover / focus affordance only — never a click toggle, which
       is what made "click Products" feel like it jumped away unasked. */

    if (hoverable) {
      g.addEventListener('mouseenter', function () {
        clearTimeout(closeTimer);
        closeAll(g);
        setState(g, true);
      });
      g.addEventListener('mouseleave', function () {
        clearTimeout(closeTimer);
        closeTimer = setTimeout(function () { setState(g, false); }, 160);
      });
    }

    /* keyboard: focusing the label reveals the panel so Tab can walk into it */
    g.addEventListener('focusin', function () {
      if (skipFocusOpen || !keyboardFocus) return;
      clearTimeout(closeTimer);
      closeAll(g);
      setState(g, true);
    });

    g.addEventListener('focusout', function (e) {
      if (!g.contains(e.relatedTarget)) setState(g, false);
    });

    /* picking an item closes the panel — same-page anchors do not reload the
       document, so nothing else would dismiss it */
    panel.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('a')) {
        clearTimeout(closeTimer);
        setState(g, false);
      }
    });

    g.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        skipFocusOpen = true;
        setState(g, false);
        btn.focus();
        skipFocusOpen = false;
      }
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('[data-navm]')) closeAll(null);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll(null);
  });

  /* ---------- document viewer (certificates) ---------- */
  var certLinks = document.querySelectorAll('[data-cert]');
  if (certLinks.length) {
    var box = document.createElement('div');
    box.className = 'certbox';
    box.hidden = true;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Document viewer');
    box.innerHTML = '<button class="certbox__close" type="button" aria-label="Close document viewer">&times;</button>' +
      '<figure class="certbox__fig"><figcaption class="mono"></figcaption></figure>';
    document.body.appendChild(box);

    var boxFig = box.querySelector('figure');
    var boxCap = box.querySelector('figcaption');
    var boxClose = box.querySelector('.certbox__close');
    var lastFocus = null;

    function openDoc(link) {
      lastFocus = link;
      var img = document.createElement('img');
      img.src = link.getAttribute('data-cert');
      img.alt = link.getAttribute('data-cert-label') || '';
      boxFig.insertBefore(img, boxFig.firstChild);
      boxCap.textContent = link.getAttribute('data-cert-label') || '';
      box.hidden = false;
      document.documentElement.classList.add('is-locked');
      boxClose.focus();
    }

    function closeDoc() {
      var img = boxFig.querySelector('img');
      if (img) img.parentNode.removeChild(img);
      box.hidden = true;
      document.documentElement.classList.remove('is-locked');
      if (lastFocus) { lastFocus.focus(); lastFocus = null; }
    }

    Array.prototype.forEach.call(certLinks, function (link) {
      link.addEventListener('click', function (e) {
        // let modifier clicks / middle clicks open the file itself
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button > 0) return;
        e.preventDefault();
        openDoc(link);
      });
    });

    boxClose.addEventListener('click', closeDoc);
    box.addEventListener('click', function (e) { if (e.target === box) closeDoc(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !box.hidden) { closeDoc(); }
    });
  }
})();

/* ---------- WhatsApp floating button ---------- */
(function () {
  'use strict';
  var fab = document.querySelector('.wafab');
  if (!fab) return;

  /* the compare bar is fixed to the bottom edge on catalogue pages; lift the
     button by its live height so the two never sit on top of each other */
  var bar = document.getElementById('cmpbar');
  var root = document.documentElement;
  if (bar) {
    var sync = function () {
      var h = bar.hasAttribute('hidden') ? 0 : bar.offsetHeight;
      root.style.setProperty('--cmpbar-h', h + 'px');
    };
    sync();
    if (window.MutationObserver) {
      new MutationObserver(sync).observe(bar, { attributes: true, attributeFilter: ['hidden'] });
    }
    if (window.ResizeObserver) new ResizeObserver(sync).observe(bar);
    window.addEventListener('resize', sync);
  }

  /* reveal the label once per session on hover-capable screens, so the disc is
     not just a green circle for a first-time visitor */
  var hoverable = window.matchMedia && window.matchMedia('(hover: hover) and (min-width: 600px)').matches;
  if (!hoverable) return;
  try {
    if (sessionStorage.getItem('zm-wa-teaser')) return;
    sessionStorage.setItem('zm-wa-teaser', '1');
  } catch (err) { return; }
  setTimeout(function () {
    fab.classList.add('is-teaser');
    setTimeout(function () { fab.classList.remove('is-teaser'); }, 3800);
  }, 1900);
})();
