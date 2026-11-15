// Full-page screenshot of a single page, with every .reveal fired first.
// usage: node tools/shot_fullpage.js index.html 1440 shots/home-full-1440.jpg
const http = require('http'), fs = require('fs');

const get = (p, m = 'GET') => new Promise((res, rej) => {
  http.request({ host: '127.0.0.1', port: 9222, path: p, method: m }, r => {
    let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d)));
  }).on('error', rej).end();
});

(async () => {
  const [page, w, out] = process.argv.slice(2);
  const W = +w || 1440;

  const t = await get('/json/new?about:blank', 'PUT');
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  let id = 0; const pend = new Map();
  const send = (m, p = {}) => new Promise((res, rej) => {
    const i = ++id; pend.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method: m, params: p }));
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

  await new Promise(r => ws.onopen = r);
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 700 });

  await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + page });
  await wait(1200);

  // walk the page so IntersectionObserver fires for every .reveal
  const H = await ev('document.body.scrollHeight');
  for (let y = 0; y < H; y += 500) { await ev('window.scrollTo(0,' + y + ')'); await wait(170); }
  await wait(900);
  await ev('window.scrollTo(0,0)');
  await wait(700);

  // make sure lazy images are decoded
  await ev(`Promise.race([Promise.all([...document.images].map(i=>i.complete&&i.naturalWidth?1:new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,6000))]).then(()=>1)`);
  await wait(400);

  const info = await ev(`(()=>{const d=document.documentElement;return JSON.stringify({h:Math.max(d.scrollHeight,d.offsetHeight,d.clientHeight),ovf:d.scrollWidth-window.innerWidth,reveals:[...document.querySelectorAll('.reveal')].filter(e=>getComputedStyle(e).opacity<0.9).length})})()`);
  const { h, ovf, reveals } = JSON.parse(info);

  const s = await send('Page.captureScreenshot', {
    format: 'jpeg', quality: 88, captureBeyondViewport: true, fromSurface: true,
    clip: { x: 0, y: 0, width: W, height: h, scale: 1 }
  });
  fs.mkdirSync(require('path').dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(s.data, 'base64'));
  const kb = (fs.statSync(out).size / 1024).toFixed(0);
  console.log(`${out}  ${W}x${h}  ${kb}KB  overflowX=${ovf}  unfiredReveals=${reveals}`);
  ws.close(); process.exit(0);
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
