// 量导航与面板对齐关系，量完即关标签，避免标签堆积
const http = require('http');
const W = +process.argv[2] || 1440;
const PAGE = process.argv[3] || 'index.html';

function req(method, path) {
  return new Promise((res, rej) => {
    const r = http.request({ host: '127.0.0.1', port: 9222, path, method }, x => {
      let d = ''; x.on('data', c => d += c); x.on('end', () => res(d));
    });
    r.on('error', rej); r.end();
  });
}

(async () => {
  const t = JSON.parse(await req('PUT', '/json/new?about:blank'));
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  let id = 0;
  const send = (m, p = {}) => new Promise((res, rej) => {
    const i = ++id;
    ws.send(JSON.stringify({ id: i, method: m, params: p }));
    const h = e => { const x = JSON.parse(e.data); if (x.id === i) { ws.removeEventListener('message', h); x.error ? rej(new Error(JSON.stringify(x.error))) : res(x.result); } };
    ws.addEventListener('message', h);
    setTimeout(() => rej(new Error('timeout ' + m)), 20000);
  });
  const ev = x => send('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true }).then(o => o.result && o.result.value);
  const wait = ms => new Promise(r => setTimeout(r, ms));

  ws.onopen = async () => {
    try {
      await send('Page.enable'); await send('Runtime.enable');
      await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: false });
      await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + PAGE });
      await wait(1600);
      await ev("document.fonts.ready.then(()=>1)");
      const out = await ev(`(()=>{
        const q=s=>document.querySelector(s);
        const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)]};
        const links=q('.nav__links'), btn=q('[data-navm] .navm__btn'), grp=q('[data-navm]'), panel=q('.navm__panel--mega');
        return JSON.stringify({links:r(links),grp:r(grp),btn:r(btn),panel:r(panel),navInner:r(q('.nav__inner')),logo:r(q('.nav__logo'))});
      })()`);
      console.log(W, out);
    } catch (e) { console.log('ERR', e.message); }
    try { await req('GET', '/json/close/' + t.id); } catch (e) {}
    process.exit(0);
  };
})();
