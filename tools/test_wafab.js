// 悬浮球：键盘焦点可见 / 灯箱与抽屉层级 / 链接属性
const http = require('http');
const W = +process.argv[2] || 1440;
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
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 600 });

  await send('Page.navigate', { url: 'http://127.0.0.1:8788/index.html' });
  await wait(1800);

  console.log('attrs:', await ev(`(()=>{const a=document.querySelector('.wafab');return JSON.stringify({href:a.getAttribute('href').slice(0,60),target:a.target,rel:a.rel,label:a.getAttribute('aria-label'),tipHidden:a.querySelector('.wafab__tip').getAttribute('aria-hidden')})})()`));

  // 键盘：真实 Tab 走到悬浮球，确认 :focus-visible 命中且标签展开
  await ev(`document.body.setAttribute('tabindex','-1');document.body.focus();document.body.removeAttribute('tabindex');1`);
  let hit = -1;
  for (let i = 1; i <= 90; i++) {
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
    const on = await ev(`document.activeElement.classList && document.activeElement.classList.contains('wafab')`);
    if (on) { hit = i; break; }
  }
  await wait(260);
  console.log('focus:', hit > 0 ? await ev(`(()=>{const a=document.querySelector('.wafab');const cs=getComputedStyle(a.querySelector('.wafab__tip'));return JSON.stringify({tabsToReach:${hit}, fv:a.matches(':focus-visible'), tipOpacity:cs.opacity, outline:getComputedStyle(a).outlineWidth+' '+getComputedStyle(a).outlineColor})})()`) : 'NOT-REACHED-IN-90-TABS');

  // 灯箱层级：打开证书，FAB 位置的最上层元素应为灯箱
  const certOk = await ev(`(()=>{const c=document.querySelector('[data-cert]');if(!c)return 'no-cert';c.click();return 'clicked'})()`);
  await wait(500);
  console.log('lightbox:', certOk, await ev(`(()=>{const f=document.querySelector('.wafab'),r=f.getBoundingClientRect();const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return JSON.stringify({top:el.className||el.tagName, lightboxOpen:!document.querySelector('.certbox').hidden})})()`));
  await ev(`document.querySelector('.certbox__x') && document.querySelector('.certbox__x').click();1`);

  await req('GET', '/json/close/' + t.id);
  process.exit(0);
})();
