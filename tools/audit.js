// 全站巡检：报错 / 缺图 / 横向溢出 / 超级菜单开合与 Esc
// usage: node tools/audit.js
const http = require('http');

const PAGES = ['index.html', 'products.html', 'product-zm-m65k.html', 'product-zm-d8000-1.html',
  'product-zm-sl8c.html', 'capabilities.html', 'oem-odm.html', 'brand-studio.html',
  'company.html', 'news.html', 'contact.html'];
const WIDTHS = [1440, 1024, 390];

function req(method, path) {
  return new Promise((res, rej) => {
    const r = http.request({ host: '127.0.0.1', port: 9222, path, method }, x => {
      let d = ''; x.on('data', c => d += c); x.on('end', () => res(d));
    });
    r.on('error', rej); r.end();
  });
}

async function run() {
  const bad = [];
  for (const W of WIDTHS) {
    const t = JSON.parse(await req('PUT', '/json/new?about:blank'));
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    let id = 0, errors = [], wsErrs = [];
    const send = (m, p = {}) => new Promise((res, rej) => {
      const i = ++id;
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
      const h = e => { const x = JSON.parse(e.data); if (x.id === i) { ws.removeEventListener('message', h); x.error ? rej(new Error(JSON.stringify(x.error))) : res(x.result); } };
      ws.addEventListener('message', h);
      setTimeout(() => rej(new Error('timeout ' + m)), 25000);
    });
    const ev = x => send('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true }).then(o => o.result && o.result.value);
    const wait = ms => new Promise(r => setTimeout(r, ms));

    await new Promise(r => { ws.onopen = r; });
    ws.addEventListener('message', e => {
      const x = JSON.parse(e.data);
      if (x.method === 'Runtime.exceptionThrown') wsErrs.push(x.params.exceptionDetails.text + ' ' + (x.params.exceptionDetails.exception || {}).description);
      if (x.method === 'Runtime.consoleAPICalled' && x.params.type === 'error') wsErrs.push(x.params.args.map(a => a.value || a.description).join(' '));
    });
    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 600 });

    for (const P of PAGES) {
      wsErrs = [];
      await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + P });
      await wait(1500);
      await ev("document.fonts.ready.then(()=>1)");
      await ev("window.scrollTo(0,document.body.scrollHeight);1");
      await wait(700);
      await ev("window.scrollTo(0,0);1");
      await wait(300);

      const r = JSON.parse(await ev(`(()=>{
        const img=[...document.images].filter(i=>i.complete && i.naturalWidth===0).map(i=>i.getAttribute('src'));
        const de=document.documentElement;
        const mega=document.querySelectorAll('.navm__panel--mega').length;
        const links=[...document.querySelectorAll('.mega__item, .mega__feat, .mega__foot a')].map(a=>a.getAttribute('href'));
        const fab=document.querySelectorAll('.wafab');
        let fabBox=null;
        if (fab.length) { const r=fab[0].getBoundingClientRect(); fabBox=[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]; }
        return JSON.stringify({img, over: de.scrollWidth-innerWidth, mega, links, fab:fab.length, fabBox, panels: document.querySelectorAll('.navm__panel').length});
      })()`));
      let nav = 'n/a';
      if (W >= 1000) {
        const b = JSON.parse(await ev(`(()=>{const b=document.querySelector('[data-navm] .navm__btn');const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
        await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: b.x, y: b.y, buttons: 0 });
        await wait(320);
        const open = await ev(`document.querySelector('.navm__panel--mega').getAttribute('data-open')`);
        const box = await ev(`(()=>{const r=document.querySelector('.navm__panel--mega').getBoundingClientRect();return Math.round(r.left)+','+Math.round(r.right)+' of '+innerWidth})()`);
        // Esc 在面板内按下
        await ev(`document.querySelector('.mega__item').focus();1`);
        await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
        await wait(260);
        const afterEsc = await ev(`document.querySelector('.navm__panel--mega').getAttribute('data-open')`);
        const focusBack = await ev(`document.activeElement.className`);
        nav = `open=${open} esc=${afterEsc === null ? 'closed' : 'STILL-OPEN'} focus=${focusBack} box=${box}`;
        if (open !== 'true' || afterEsc !== null) bad.push(`${W} ${P} nav ${nav}`);
        await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
      } else {
        const hidden = await ev(`getComputedStyle(document.querySelector('.navm')).display`);
        nav = `navm display=${hidden}`;
        if (hidden !== 'none') bad.push(`${W} ${P} navm not hidden`);
      }

      const flag = [];
      if (r.img.length) { flag.push('MISSING-IMG'); bad.push(`${W} ${P} img ${r.img.join('|')}`); }
      if (r.over > 0) { flag.push('OVERFLOW+' + r.over); bad.push(`${W} ${P} overflow ${r.over}`); }
      if (r.mega !== 1) { flag.push('MEGA=' + r.mega); bad.push(`${W} ${P} mega ${r.mega}`); }
      if (wsErrs.length) { flag.push('JS-ERR'); bad.push(`${W} ${P} js ${wsErrs[0]}`); }
      if (r.fab !== 1) { flag.push('FAB=' + r.fab); bad.push(`${W} ${P} fab count ${r.fab}`); }
      else {
        const [fx, fy, fw, fh] = r.fabBox;
        if (fx + fw > W || fy + fh > 900 || fx < 0 || fy < 0) { flag.push('FAB-OUT'); bad.push(`${W} ${P} fab box ${r.fabBox}`); }
        if (W < 600 && fw > 56) { flag.push('FAB-BIG'); bad.push(`${W} ${P} fab ${fw}px`); }
      }

      console.log(`${W} ${P.padEnd(24)} img${r.img.length} over${r.over} fab${r.fabBox ? '@' + r.fabBox[2] + 'px' : '?'} ${nav} ${flag.join(' ') || 'ok'}`);
    }
    await req('GET', '/json/close/' + t.id);
  }
  console.log('\n== FAILURES ==', bad.length ? '\n' + bad.join('\n') : 'none');
  process.exit(0);
}
run();
