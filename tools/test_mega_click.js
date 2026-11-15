// 交互验证：菜单点击 → 目录筛选；?topic=damping → 表单预填
const http = require('http');
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
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

  // 1. products.html：点 Subwoofers
  await send('Page.navigate', { url: 'http://127.0.0.1:8788/products.html' });
  await wait(1600);
  const b = JSON.parse(await ev(`(()=>{const b=document.querySelector('[data-navm] .navm__btn');const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: b.x, y: b.y, buttons: 0 });
  await wait(350);
  const tgt = JSON.parse(await ev(`(()=>{const a=[...document.querySelectorAll('.mega__item')].find(a=>a.textContent.includes('Subwoofers'));const r=a.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
  for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
    await send('Input.dispatchMouseEvent', { type, x: tgt.x, y: tgt.y, button: 'left', clickCount: 1, buttons: type === 'mousePressed' ? 1 : 0 });
    await wait(60);
  }
  await wait(700);
  console.log('click:', await ev(`JSON.stringify({hash:location.hash, open:document.querySelector('.navm__panel--mega').getAttribute('data-open'), shown:document.querySelector('.cf-chip[aria-pressed="true"]')&&document.querySelector('.cf-chip[aria-pressed="true"]').textContent.trim(), visible:[...document.querySelectorAll('.pcard')].filter(c=>c.offsetParent).length, scrollY:Math.round(scrollY)})`));

  // 2. contact.html?topic=damping
  await send('Page.navigate', { url: 'http://127.0.0.1:8788/contact.html?topic=damping' });
  await wait(1500);
  console.log('damping:', await ev(`JSON.stringify({cat:document.getElementById('f-category').value, msg:document.getElementById('f-msg').value})`));

  // 3. contact.html?topic=brand 未回归
  await send('Page.navigate', { url: 'http://127.0.0.1:8788/contact.html?topic=brand' });
  await wait(1200);
  console.log('brand:', await ev(`JSON.stringify({cat:document.getElementById('f-category').value, msg:document.getElementById('f-msg').value.slice(0,40)})`));

  await req('GET', '/json/close/' + t.id);
  process.exit(0);
})();
