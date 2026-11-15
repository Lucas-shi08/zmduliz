/* product catalogue: family filter + model search */
(function () {
  'use strict';
  var chips = document.querySelectorAll('.cf-chip');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.pcard'));
  var countEl = document.querySelector('.cf-count');
  var searchEl = document.querySelector('.cf-search input');
  var empty = document.querySelector('.noresult');
  if (!cards.length) return;

  var fam = 'all';

  function selectFam(key) {
    var hit = null;
    chips.forEach(function (x) {
      var on = x.getAttribute('data-fam') === key;
      x.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) hit = x;
    });
    fam = hit ? key : 'all';
    apply();
    return hit;
  }

  function jumpToCatalogue(smooth) {
    var bar = document.querySelector('.filterbar');
    if (!bar) return;
    var navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'), 10) || 68;
    function target() { return Math.max(0, bar.getBoundingClientRect().top + window.pageYOffset - navH); }
    window.scrollTo({ top: target(), behavior: smooth ? 'smooth' : 'auto' });
    /* the hero art can settle a frame or two after load and shift the bar, so
       re-align once the layout is final (only for the instant jump) */
    if (!smooth) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { window.scrollTo({ top: target(), behavior: 'auto' }); });
      });
    }
  }

  function apply() {
    var q = (searchEl && searchEl.value || '').trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {
      var okFam = fam === 'all' || c.getAttribute('data-fam') === fam;
      var hay = (c.getAttribute('data-search') || '').toLowerCase();
      var okQ = !q || hay.indexOf(q) > -1;
      var show = okFam && okQ;
      c.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (countEl) {
      countEl.textContent = shown + ' of ' + cards.length + ' platforms shown';
    }
    if (empty) empty.classList.toggle('show', shown === 0);
  }

  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      var key = b.getAttribute('data-fam');
      selectFam(key);
      /* keep the address bar in sync so the filtered view is shareable and
         survives a refresh (replaceState does not fire hashchange) */
      if (history.replaceState) {
        history.replaceState(null, '', key === 'all'
          ? location.pathname + location.search
          : '#' + key);
      }
    });
  });

  if (searchEl) {
    searchEl.addEventListener('input', apply);
    searchEl.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { searchEl.value = ''; apply(); }
    });
  }

  /* deep link: products.html#subwoofer preselects that family and drops you at
     the catalog. The nav dropdown points at these anchors, so this also has to
     react to hash changes made while the catalog page is already open — without
     the listener the URL changed but the grid stayed on "All platforms". */
  function syncFromHash(smooth) {
    var key = (location.hash || '').replace('#', '');
    if (!key) return false;
    /* #catalogue = "show me everything", used by the nav's All platforms entry */
    if (key === 'catalogue') {
      selectFam('all');
      jumpToCatalogue(smooth);
      return true;
    }
    var hit = selectFam(key);
    if (hit) jumpToCatalogue(smooth);
    return !!hit;
  }

  if (!syncFromHash(false)) apply();

  window.addEventListener('hashchange', function () {
    if (!syncFromHash(true)) selectFam('all');
  });
})();

/* datasheet: thumbnail gallery + section scroll-spy */
(function () {
  'use strict';
  var main = document.querySelector('.ds-gallery__main img');
  var thumbs = document.querySelectorAll('.ds-thumb');
  thumbs.forEach(function (t) {
    t.addEventListener('click', function () {
      thumbs.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      t.setAttribute('aria-pressed', 'true');
      if (main) main.src = t.getAttribute('data-src');
    });
  });

  var links = document.querySelectorAll('.ds-nav a');
  if (links.length && 'IntersectionObserver' in window) {
    var secs = Array.prototype.map.call(links, function (a) { return document.querySelector(a.getAttribute('href')); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var i = secs.indexOf(en.target);
        if (i < 0) return;
        links.forEach(function (a) { a.classList.remove('active'); });
        links[i].classList.add('active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secs.forEach(function (s) { if (s) io.observe(s); });
  }
})();

/* ---------- compare (same family, two at a time) ---------- */
(function () {
  'use strict';
  var dataEl = document.getElementById('cmpdata');
  if (!dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);
  var byModel = {};
  DATA.forEach(function (d) { byModel[d.m] = d; });

  var sel = [];
  var bar = document.getElementById('cmpbar');
  var slots = document.getElementById('cmpslots');
  var openBtn = document.getElementById('cmpopen');
  var clearBtn = document.getElementById('cmpclear');
  var modal = document.getElementById('cmpmodal');
  var body = document.getElementById('cmpbody');
  var diffInput = document.getElementById('cmpdiff');
  var toast = document.getElementById('cmptoast');
  var toastTimer = null;
  var lastFocus = null;
  var btns = Array.prototype.slice.call(document.querySelectorAll('.pcard__cmp'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.pcard'));

  function say(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 4200);
  }

  function render() {
    var first = sel.length ? byModel[sel[0]] : null;
    btns.forEach(function (b) {
      var m = b.getAttribute('data-model');
      b.setAttribute('aria-pressed', sel.indexOf(m) > -1 ? 'true' : 'false');
    });
    cards.forEach(function (c) {
      c.classList.toggle('is-locked', !!(first && c.getAttribute('data-fam') !== first.f));
    });

    if (!slots) return;
    slots.innerHTML = '';
    sel.forEach(function (m) {
      var d = byModel[m];
      var chip = document.createElement('span');
      chip.className = 'cmpslot';
      chip.innerHTML = '<span>' + d.m + '</span>';
      var x = document.createElement('button');
      x.type = 'button';
      x.setAttribute('aria-label', 'Remove ' + d.m + ' from comparison');
      x.textContent = '\u00d7';
      x.addEventListener('click', function () { sel.splice(sel.indexOf(m), 1); render(); });
      chip.appendChild(x);
      slots.appendChild(chip);
    });

    bar.hidden = sel.length === 0;
    openBtn.disabled = sel.length < 2;
    openBtn.textContent = sel.length < 2 ? 'Select one more' : 'Compare platforms';
    document.body.classList.toggle('cmp-active', sel.length > 0);
  }

  function toggle(btn) {
    var m = btn.getAttribute('data-model');
    var d = byModel[m];
    if (!d) return;
    var i = sel.indexOf(m);
    if (i > -1) { sel.splice(i, 1); render(); return; }

    if (sel.length === 0) { sel.push(m); render(); return; }
    var first = byModel[sel[0]];
    if (first.f !== d.f) {
      say('Only platforms in the same family can be compared. ' + first.m + ' is a ' + first.fl.replace('&amp;', '&') + '; ' + d.m + ' is a ' + d.fl.replace('&amp;', '&') + '.');
      return;
    }
    if (sel.length >= 2) {
      say('Two platforms at a time — remove one before adding ' + d.m + '.');
      return;
    }
    sel.push(m);
    render();
  }

  btns.forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); toggle(b); });
  });

  if (clearBtn) clearBtn.addEventListener('click', function () { sel = []; render(); });

  /* ---- table ---- */
  function norm(v) {
    return String(v).toLowerCase().replace(/\s+/g, ' ').replace(/[\u00a0]/g, ' ').trim();
  }

  function colHead(d) {
    return '<th scope="col"><div class="cmpcol"><img src="assets/img/pic/' + d.img + '" alt="" loading="lazy">' +
      '<span><b>' + d.m + '</b><span>' + d.n + '</span>' +
      '<a href="' + d.u + '">Datasheet</a></span></div></th>';
  }

  function build() {
    var A = byModel[sel[0]], B = byModel[sel[1]];
    if (!A || !B) return;

    var mapA = {}, mapB = {}, labels = [];
    A.rows.forEach(function (r) { mapA[r[0]] = r[1]; labels.push(r[0]); });
    B.rows.forEach(function (r) { if (labels.indexOf(r[0]) === -1) labels.push(r[0]); mapB[r[0]] = r[1]; });

    var rows = [], diffs = 0;
    labels.forEach(function (k) {
      var a = mapA[k] == null ? '—' : mapA[k];
      var b = mapB[k] == null ? '—' : mapB[k];
      var d = norm(a) !== norm(b);
      var miss = a === '—' || b === '—';
      if (d) diffs++;
      rows.push({ k: k, a: a, b: b, d: d, miss: miss });
    });

    var only = diffInput && diffInput.checked;
    var shown = only ? rows.filter(function (r) { return r.d; }) : rows;

    var html = '<table class="cmptable"><thead><tr><th scope="col">Parameter</th>' + colHead(A) + colHead(B) + '</tr></thead><tbody>';
    shown.forEach(function (r) {
      html += '<tr class="' + (r.d ? 'is-diff' : '') + (r.miss ? ' is-missing' : '') + '"><th scope="row">' + r.k + '</th><td>' + r.a + '</td><td>' + r.b + '</td></tr>';
    });
    html += '</tbody></table>';
    html += '<p class="cmpsum"><span><b>' + diffs + '</b> of ' + rows.length + ' parameters differ</span>' +
      '<span>' + (only ? 'Showing differences only' : 'Showing all parameters') + '</span>' +
      '<span>— = not specified for this platform</span></p>';
    body.innerHTML = html;
  }

  function openModal() {
    if (sel.length < 2) return;
    lastFocus = document.activeElement;
    build();
    modal.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    var closeBtn = modal.querySelector('.cmpmodal__close');
    if (closeBtn) closeBtn.focus();
  }

  function closeModal() {
    modal.hidden = true;
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (diffInput) diffInput.addEventListener('change', build);
  Array.prototype.forEach.call(document.querySelectorAll('[data-close]'), function (el) {
    el.addEventListener('click', closeModal);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal && !modal.hidden) closeModal();
  });

  render();
})();
