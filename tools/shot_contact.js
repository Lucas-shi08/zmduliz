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
    const s = await send('Page.captureScreenshot', Object.assign({ format: 'jpeg', quality: 90 }, clip ? { clip } : {}));
    fs.writeFileSync(file, Buffer.from(s.data, 'base64'));
  };

  await new Promise(r => ws.onopen = r);
  await send('Page.enable');
  await send('Runtime.enable');

  /* ---------- desktop 1440 ---------- */
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: BASE + '/contact.html' });
  await wait(2200);

  await shot('shots/c-top.jpg', { x: 0, y: 0, width: 1440, height: 900, scale: 1 });

  // scroll so the inquiry block is fully visible, then capture the whole block
  const box = await ev(`(() => {
    const r = document.querySelector('.inq').getBoundingClientRect();
    return JSON.stringify({ top: Math.round(r.top + scrollY), h: Math.round(r.height) });
  })()`);
  const b = JSON.parse(box);
  await ev(`window.scrollTo(0, ${b.top - 90})`);
  await wait(900);
  await shot('shots/c-inq.jpg', { x: 0, y: 0, width: 1440, height: Math.min(1400, b.h + 140), scale: 1 });

  // location section
  await ev(`document.getElementById('factory-location').scrollIntoView({block:'start'})`);
  await wait(900);
  await shot('shots/c-loc.jpg', { x: 0, y: 0, width: 1440, height: 900, scale: 1 });

  console.log(await ev(`(() => {
    const d = document.documentElement;
    const card = document.querySelector('.ccard').getBoundingClientRect();
    const fig = document.querySelector('.ccard__fig img');
    const map = document.querySelector('.mapbox').getBoundingClientRect();
    return JSON.stringify({
      hScroll: d.scrollWidth - d.clientWidth,
      pageH: d.scrollHeight,
      card: { w: Math.round(card.width), h: Math.round(card.height) },
      fig: { w: fig.naturalWidth, h: fig.naturalHeight, boxW: Math.round(fig.getBoundingClientRect().width), boxH: Math.round(fig.getBoundingClientRect().height) },
      map: { w: Math.round(map.width), h: Math.round(map.height) },
      imgsBroken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src.split('/').pop())
    });
  })()`));

  /* ---------- tablet 900 ---------- */
  await send('Emulation.setDeviceMetricsOverride', { width: 900, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: BASE + '/contact.html' });
  await wait(1600);
  console.log(await ev(`JSON.stringify({ hScroll: document.documentElement.scrollWidth - document.documentElement.clientWidth })`));

  /* ---------- mobile 390 ---------- */
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await send('Page.navigate', { url: BASE + '/contact.html' });
  await wait(1600);
  await shot('shots/c-m1.jpg');
  await ev(`window.scrollTo(0, document.querySelector('.inq__side').getBoundingClientRect().top + scrollY - 80)`);
  await wait(800);
  await shot('shots/c-m2.jpg');
  await ev(`document.getElementById('factory-location').scrollIntoView({block:'start'})`);
  await wait(800);
  await shot('shots/c-m3.jpg');
  console.log(await ev(`(() => {
    const d = document.documentElement;
    return JSON.stringify({ hScroll: d.scrollWidth - d.clientWidth, mapH: Math.round(document.querySelector('.mapbox').getBoundingClientRect().height) });
  })()`));

  await get('/json/close/' + t.id, 'PUT');
  ws.close();
  process.exit(0);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
