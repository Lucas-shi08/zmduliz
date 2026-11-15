// 悬浮球实测：默认 / hover / teaser / 对比条避让，输出视口截图
// usage: node tools/shot_wafab.js <w> <page> <out.jpg> [mode]
//   mode: plain | hover | teaser | cmp
const http = require('http'), fs = require('fs');
const W = +process.argv[2] || 1440;
const PAGE = process.argv[3] || 'index.html';
const OUT = process.argv[4] || 'shots/wa.jpg';
const MODE = process.argv[5] || 'plain';

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
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 2, mobile: W < 600 });
  await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + PAGE });
  await wait(1700);
  await ev("document.fonts.ready.then(()=>1)");

  if (MODE === 'cmp') {
    // 勾两个可对比型号，让对比条出现
    await ev(`(function(){var b=[...document.querySelectorAll('.pcard__cmp')];b[0].click();b[1].click();return 1})()`);
    await wait(600);
  }
  if (MODE === 'teaser') { await wait(1200); }   // 1.9s 触发 + 0.3s 动画

  if (MODE === 'hover') {
    const b = JSON.parse(await ev(`(()=>{const b=document.querySelector('.wafab');const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: b.x, y: b.y, buttons: 0 });
    await wait(420);
  }

  const m = await ev(`(()=>{
    const f=document.querySelector('.wafab'), r=f.getBoundingClientRect();
    const tip=f.querySelector('.wafab__tip'), tr=tip?tip.getBoundingClientRect():null;
    const bar=document.getElementById('cmpbar');
    return JSON.stringify({
      fab:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],
      right:Math.round(innerWidth-r.right), bottom:Math.round(innerHeight-r.bottom),
      tip: tr? [Math.round(tr.x),Math.round(tr.y),Math.round(tr.width),Math.round(tr.height)]:null,
      cmpbar: bar? {hidden:bar.hasAttribute('hidden'), h:bar.offsetHeight}:null,
      cmpVar:getComputedStyle(document.documentElement).getPropertyValue('--cmpbar-h').trim(),
      over:document.documentElement.scrollWidth-innerWidth,
      z:getComputedStyle(f).zIndex
    });
  })()`);
  console.log(W, MODE, m);

  const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92, scale: 1 });
  fs.writeFileSync(OUT, Buffer.from(s.data, 'base64'));
  console.log('->', OUT);
  await req('GET', '/json/close/' + t.id);
  process.exit(0);
})();
