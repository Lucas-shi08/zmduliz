const http = require('http');
const fs = require('fs');

const PORT = 9222;
const BASE = 'http://127.0.0.1:8788';

const get = (p, m = 'GET') => new Promise((res, rej) => {
  http.request({ host: '127.0.0.1', port: PORT, path: p, method: m }, r => {
    let d = ''; r.on('data', c => d += c);
    r.on('end', () => { try { res(JSON.parse(d)) } catch (e) { rej(e) } });
  }).on('error', rej).end();
});

(async () => {
  const t = await get('/json/new?about:blank', 'PUT');
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  let id = 0; const pend = new Map();
  const send = (method, params = {}) => new Promise((res, rej) => {
    const i = ++id; pend.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) {
      const p = pend.get(m.id); pend.delete(m.id);
      m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result);
    }
  };
  const ev = x => send('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true })
    .then(r => r.result && r.result.value);
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const shot = async (file, clip) => {
    const s = await send('Page.captureScreenshot', Object.assign({ format: 'jpeg', quality: 88 }, clip ? { clip } : {}));
    fs.writeFileSync(file, Buffer.from(s.data, 'base64'));
  };

  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');

  /* ---------- desktop ---------- */
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: BASE + '/index.html' });
  await wait(2200);
  await shot('shots/nav-0.jpg', { x: 0, y: 0, width: 1440, height: 150, scale: 1 });

  // open Products
  await ev(`document.querySelector('.navm__btn[aria-controls="navm-products"]').click()`);
  await wait(500);
  await shot('shots/nav-1.jpg', { x: 0, y: 0, width: 1440, height: 460, scale: 1 });

  // open OEM/ODM
  await ev(`document.querySelector('.navm__btn[aria-controls="navm-oem"]').click()`);
  await wait(500);
  await shot('shots/nav-2.jpg', { x: 0, y: 0, width: 1440, height: 380, scale: 1 });

  // open About Us
  await ev(`document.querySelector('.navm__btn[aria-controls="navm-about"]').click()`);
  await wait(500);
  await shot('shots/nav-3.jpg', { x: 0, y: 0, width: 1440, height: 340, scale: 1 });

  // report layout metrics
  console.log(await ev(`(() => {
    const inner = document.querySelector('.nav__inner');
    const links = document.querySelector('.nav__links');
    const cta = document.querySelector('.nav__cta a');
    return JSON.stringify({
      overflow: inner.scrollWidth - inner.clientWidth,
      linksW: Math.round(links.getBoundingClientRect().width),
      ctaW: Math.round(cta.getBoundingClientRect().width),
      ctaRight: Math.round(cta.getBoundingClientRect().right),
      panelW: Math.round(document.getElementById('navm-products').getBoundingClientRect().width)
    });
  })()`));

  // news page
  await send('Page.navigate', { url: BASE + '/news.html' });
  await wait(1800);
  await shot('shots/news-top.jpg');
  console.log(await ev(`(() => {
    const d = document.documentElement;
    return JSON.stringify({ hScroll: d.scrollWidth - d.clientWidth, notes: document.querySelectorAll('.note').length });
  })()`));

  /* ---------- mobile ---------- */
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await send('Page.navigate', { url: BASE + '/index.html' });
  await wait(1800);
  await ev(`document.querySelector('.nav__burger').click()`);
  await wait(900);
  await shot('shots/nav-m1.jpg');
  console.log(await ev(`(() => {
    const d = document.documentElement;
    const dr = document.querySelector('.drawer');
    return JSON.stringify({ hScroll: d.scrollWidth - d.clientWidth, drawerOpen: document.body.classList.contains('menu-open'), groups: document.querySelectorAll('.dacc').length });
  })()`));
  await ev(`document.querySelector('.dacc summary').click()`);
  await wait(700);
  await shot('shots/nav-m2.jpg');

  await get('/json/close/' + t.id, 'PUT');
  ws.close();
  process.exit(0);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
