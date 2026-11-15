// 超级菜单预览截图 + 版面测量
// usage: node tools/shot_preview.js <url> <width> <out.jpg>
const http = require('http'), fs = require('fs');
const [PATH_, W, OUT] = [process.argv[2] || '_preview-megamenu.html', +process.argv[3] || 1440, process.argv[4] || 'shots/megamenu.jpg'];

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
    ws.onclose = e => { console.log('CLOSE', e.code); process.exit(0); };
    ws.onopen = async () => {
      try {
        await send('Page.enable'); await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: W, height: 1000, deviceScaleFactor: 2, mobile: false });
        await send('Page.navigate', { url: 'http://127.0.0.1:8788/' + PATH_ });
        await new Promise(r => setTimeout(r, 2200));
        await ev("document.fonts.ready.then(()=>1)");
        await new Promise(r => setTimeout(r, 400));

        const geo = await ev(`(()=>{
          const p=document.querySelector('.navm__panel--mega');
          const r=p.getBoundingClientRect();
          const nav=document.querySelector('.nav').getBoundingClientRect();
          const btn=document.querySelector('.navm__btn').getBoundingClientRect();
          return JSON.stringify({panel:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),right:Math.round(r.right)},
            navH:Math.round(nav.height), btnX:Math.round(btn.x), vw:innerWidth, overflow:Math.round(r.right-innerWidth)});
        })()`);
        console.log('geo', geo);
        const g = JSON.parse(geo);
        const H = Math.min(1000, g.panel.y + g.panel.h + 120);
        const s = await send('Page.captureScreenshot', {
          format: 'jpeg', quality: 92, captureBeyondViewport: true,
          clip: { x: 0, y: 0, width: W, height: H, scale: 1 }
        });
        const b = Buffer.from(s.data, 'base64');
        fs.writeFileSync(OUT, b);
        console.log(OUT, W + 'x' + H, Math.round(b.length / 1024) + 'KB');
      } catch (e) { console.log('ERR', e.message); }
      process.exit(0);
    };
  });
}).end();
