// 截「现状」下拉面板（打开真实 index.html，仅在运行时强制展开，不改文件）
const http = require('http'), fs = require('fs');
const OUT = process.argv[2] || 'shots/nav-current.jpg';
const W = +process.argv[3] || 1440;

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
        await send('Page.navigate', { url: 'http://127.0.0.1:8788/index.html' });
        await new Promise(r => setTimeout(r, 2000));
        await ev("document.fonts.ready.then(()=>1)");
        await ev(`(()=>{const p=document.querySelector('#navm-products');
          p.setAttribute('data-open','true');
          document.querySelector('[aria-controls=navm-products]').setAttribute('aria-expanded','true');return 1})()`);
        await new Promise(r => setTimeout(r, 500));
        const geo = await ev(`(()=>{const r=document.querySelector('#navm-products').getBoundingClientRect();
          return JSON.stringify({x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)})})()`);
        console.log('geo', geo);
        const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 94, captureBeyondViewport: true, clip: { x: 0, y: 0, width: W, height: 560, scale: 1 } });
        const b = Buffer.from(s.data, 'base64');
        fs.writeFileSync(OUT, b);
        console.log(OUT, Math.round(b.length / 1024) + 'KB');
      } catch (e) { console.log('ERR', e.message); }
      process.exit(0);
    };
  });
}).end();
