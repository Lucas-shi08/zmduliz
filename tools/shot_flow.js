// Screenshot the seven-step .flow band on index.html / oem-odm.html at several widths.
// Requires: chrome --headless=new --remote-debugging-port=9222  +  python serve.py
// Run: node tools/shot_flow.js
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

process.on('unhandledRejection', e => { console.error('REJ', e && e.message); process.exit(1); });

const SEC = "document.querySelectorAll('.section')[2]";       // index.html — 03
const PROC = "document.querySelector('#process')";            // oem-odm.html — 01

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
    const s = await send('Page.captureScreenshot',
      Object.assign({ format: 'jpeg', quality: 86, captureBeyondViewport: true }, { clip }));
    fs.writeFileSync(file, Buffer.from(s.data, 'base64'));
  };

  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');

  const jobs = [];
  for (const [page, sel, tag] of [['index.html', SEC, 'index'], ['oem-odm.html', PROC, 'oem']]) {
    for (const w of [1440, 1180, 900, 760, 390]) jobs.push({ page, sel, tag, w });
  }

  for (const { page, sel, tag, w } of jobs) {
    await send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 700 });
    await send('Page.navigate', { url: `${BASE}/${page}` });
    await wait(800);
    await ev(`${sel}.scrollIntoView()`);
    await wait(1600);   // let the .reveal stagger settle before measuring
    // only the images inside this section, and never wait more than 3s
    await ev(`Promise.race([
      Promise.all([...${sel}.querySelectorAll('img')].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))),
      new Promise(r => setTimeout(r, 3000))
    ]).then(() => 1)`);
    await wait(200);

    const box = await ev(`(() => {
      const r = ${sel}.getBoundingClientRect();
      return { x: 0, y: Math.round(r.top + window.scrollY), width: ${w}, height: Math.round(r.height) };
    })()`);

    await shot(`shots/flow-${tag}-${w}.jpg`, { ...box, scale: 1 });

    const audit = await ev(`(() => {
      const s = ${sel};
      const items = [...s.querySelectorAll('.flow__item')];
      const tops = items.map(i => Math.round(i.getBoundingClientRect().top));
      const imgs = [...s.querySelectorAll('.flow__media img')];
      return {
        items: items.length,
        brokenImgs: imgs.filter(i => !i.complete || i.naturalWidth === 0).length,
        rows: new Set(tops).size,
        perRow: items.filter(i => Math.round(i.getBoundingClientRect().top) === tops[0]).length,
        overflowX: document.documentElement.scrollWidth - window.innerWidth,
        secH: Math.round(s.getBoundingClientRect().height),
      };
    })()`);
    console.log(`${tag} @${w}`, JSON.stringify(audit));
  }

  ws.close();
  process.exit(0);
})();
