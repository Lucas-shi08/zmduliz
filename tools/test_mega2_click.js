// 验证 OEM / About 面板内链接：真实鼠标点击 → 地址栏 hash → 目标是否进入视口
// usage: node tools/test_mega2_click.js
const http = require('http');

function open(url) {
  return new Promise(res => {
    http.request({ host: '127.0.0.1', port: 9222, path: '/json/new?' + encodeURIComponent(url), method: 'PUT' }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d).webSocketDebuggerUrl));
    }).end();
  });
}

(async () => {
  const wsUrl = await open('about:blank');
  const ws = new WebSocket(wsUrl);
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
  const hover = async (x, y) => { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, buttons: 0 }); await wait(360); };
  const click = async (x, y) => {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, buttons: 0 });
    await wait(90);
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
    await wait(1200);
  };

  ws.onopen = async () => {
    try {
      await send('Page.enable'); await send('Runtime.enable');
      await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });

      const cases = [
        { menu: 1, label: 'The seven steps', page: 'index.html', expect: 'oem-odm.html#process' },
        { menu: 1, label: 'What can change', page: 'index.html', expect: 'oem-odm.html#change' },
        { menu: 2, label: 'Facility & visit', page: 'index.html', expect: 'company.html#facility' },
        { menu: 2, label: 'Company profile', page: 'index.html', expect: 'company.html' },
      ];

      for (const c of cases) {
        await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + c.page });
        await wait(1500);
        await ev('window.scrollTo(0,0);1'); await wait(200);
        const btn = JSON.parse(await ev(`(()=>{const b=document.querySelectorAll('[data-navm] .navm__btn')[${c.menu}];const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
        await hover(btn.x, btn.y);
        const link = JSON.parse(await ev(`(()=>{
          const p=document.querySelectorAll('.navm__panel--mega')[${c.menu}];
          const a=[...p.querySelectorAll('.mega__item')].find(a=>a.textContent.indexOf(${JSON.stringify(c.label)})>-1);
          if(!a) return JSON.stringify({none:true});
          const r=a.getBoundingClientRect();
          return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),href:a.getAttribute('href')});
        })()`));
        if (link.none) { console.log('MISS', c.label); continue; }
        await click(link.x, link.y);

        const got = await ev(`JSON.stringify({url:location.pathname+location.hash})`);
        const g = JSON.parse(got);
        const landed = await ev(`(()=>{
          const el=document.querySelector(':target')||document.body;
          const r=el.getBoundingClientRect();
          return JSON.stringify({target: el.id||'(none)', top:Math.round(r.top), navH:parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'))||0, scrollY:Math.round(scrollY)});
        })()`);
        const ok = g.url.replace(/^\//, '') === c.expect;
        console.log(`${ok ? 'OK  ' : 'FAIL'} ${c.label.padEnd(18)} -> ${g.url}  expect=${c.expect}  ${landed}`);
      }
    } catch (e) { console.log('ERR', e.message); }
    process.exit(0);
  };
})();
