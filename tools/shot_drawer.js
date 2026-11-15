// 手机抽屉：展开 Products 分组并截图
const http = require('http'), fs = require('fs');
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
  await new Promise(r => { ws.onopen = r; });
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await send('Page.navigate', { url: 'http://127.0.0.1:8788/index.html' });
  await wait(1600);
  const b = JSON.parse(await ev(`(()=>{const b=document.querySelector('.nav__burger');const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
  for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
    await send('Input.dispatchMouseEvent', { type, x: b.x, y: b.y, button: 'left', clickCount: 1, buttons: type === 'mousePressed' ? 1 : 0 });
    await wait(80);
  }
  await wait(600);
  const IDX = +process.argv[2] || 0;   // 0 products, 1 oem, 2 about
  await ev(`document.querySelectorAll('.dacc summary')[${IDX}].click();1`);
  await wait(500);
  const box = await ev(`(()=>{const d=document.querySelector('.drawer');const r=d.getBoundingClientRect();return Math.round(r.width)+'w overflow='+(document.documentElement.scrollWidth-innerWidth)})()`);
  console.log('drawer', box);
  const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
  const out = 'shots/drawer-390-' + (['products','oem','about'][IDX] || IDX) + '.jpg';
  fs.writeFileSync(out, Buffer.from(s.data, 'base64'));
  console.log('->', out);
  await req('GET', '/json/close/' + t.id);
  process.exit(0);
})();
