// 超级菜单正式版实测：真实鼠标悬停 → 量版面 → 截导航区
// usage: node tools/shot_mega_live.js <width> <out.jpg> [page]
const http = require('http'), fs = require('fs');
const W = +process.argv[2] || 1440;
const OUT = process.argv[3] || 'shots/mega-1440.jpg';
const PAGE = process.argv[4] || 'index.html';
const SCROLL = +process.argv[5] || 0;
const MENU = +process.argv[6] || 0;   // 0 products, 1 oem, 2 about

http.request({ host: '127.0.0.1', port: 9222, path: '/json/new?about:blank', method: 'PUT' }, r => {
  let d = ''; r.on('data', c => d += c);
  r.on('end', () => {
    const ws = new WebSocket(JSON.parse(d).webSocketDebuggerUrl);
    let id = 0;
    const send = (m, p = {}) => new Promise((res, rej) => {
      const i = ++id;
      ws.send(JSON.stringify({ id: i, method: m, params: p }));
      const h = e => { const x = JSON.parse(e.data); if (x.id === i) { ws.removeEventListener('message', h); x.error ? rej(new Error(JSON.stringify(x.error))) : res(x.result); } };
      ws.addEventListener('message', h);
      setTimeout(() => rej(new Error('timeout ' + m)), 25000);
    });
    const ev = x => send('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true }).then(o => o.result && o.result.value);
    const wait = ms => new Promise(r => setTimeout(r, ms));

    ws.onclose = e => { console.log('CLOSE', e.code); process.exit(0); };
    ws.onopen = async () => {
      try {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: W, height: 1000, deviceScaleFactor: 2, mobile: false });
        await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + PAGE });
        await wait(2000);
        await ev("document.fonts.ready.then(()=>1)");
        await wait(300);

        if (SCROLL) { await ev('window.scrollTo(0,' + SCROLL + ');1'); await wait(700); }

        // 真实鼠标移入 Products 按钮，触发 mouseenter
        const btn = JSON.parse(await ev(`(()=>{const b=document.querySelectorAll('[data-navm] .navm__btn')[${MENU}];const r=b.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})()`));
        if (!btn) { console.log('no nav'); process.exit(0); }
        await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: btn.x, y: btn.y, buttons: 0 });
        await wait(520);

        const geo = await ev(`(()=>{
          const p=document.querySelectorAll('.navm__panel--mega')[${MENU}];
          if(!p) return JSON.stringify({none:true});
          const r=p.getBoundingClientRect();
          const cs=getComputedStyle(p);
          const feat=p.querySelector('.mega__feat');
          const fs_=feat?getComputedStyle(feat):null;
          const items=[...document.querySelectorAll('.mega__item')].map(a=>a.getBoundingClientRect());
          return JSON.stringify({
            open:p.getAttribute('data-open'), op:cs.opacity, vis:cs.visibility,
            panel:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),right:Math.round(r.right)},
            overflowRight:Math.round(r.right-innerWidth), overflowLeft:Math.round(r.x),
            featVisible: fs_? fs_.display!=='none' : false,
            docScrollW: document.documentElement.scrollWidth, vw: innerWidth,
            row1: items.map(i=>Math.round(i.y)).slice(0,8),
            colX: items.map(i=>Math.round(i.x)).slice(0,8)
          });
        })()`);
        console.log(W + 'px', geo);
        const g = JSON.parse(geo);
        const H = g.panel ? Math.min(760, g.panel.y + g.panel.h + 40) : 200;
        const s = await send('Page.captureScreenshot', {
          format: 'jpeg', quality: 92, captureBeyondViewport: true,
          clip: { x: 0, y: SCROLL || 0, width: Math.min(W, g.docScrollW || W), height: H, scale: 1 }
        });
        fs.writeFileSync(OUT, Buffer.from(s.data, 'base64'));
        console.log('->', OUT);
      } catch (e) { console.log('ERR', e.message); }
      process.exit(0);
    };
  });
}).end();
