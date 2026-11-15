// Hero screenshot with CDP.  usage: node tools/shot_hero.js 1440 2 out.png
const http = require('http'), fs = require('fs');
const [W, DPR, OUT] = [ +process.argv[2] || 1440, +process.argv[3] || 2, process.argv[4] || 'shots/hero.png' ];

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
      setTimeout(() => rej(new Error('timeout ' + m)), 20000);
    });
    ws.onclose = e => { console.log('CLOSE', e.code); process.exit(0); };
    ws.onopen = async () => {
      try {
        await send('Page.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: DPR, mobile: false });
        await send('Page.navigate', { url: 'http://127.0.0.1:8788/index.html' });
        await new Promise(r => setTimeout(r, 2600));
        const info = await send('Runtime.evaluate', {
          expression: `(()=>{const i=document.querySelector('.hero__bg img');const r=i.getBoundingClientRect();
            return JSON.stringify({src:i.currentSrc.split('/').pop(),nat:i.naturalWidth+'x'+i.naturalHeight,box:Math.round(r.width)+'x'+Math.round(r.height)})})()`,
          returnByValue: true
        });
        console.log('img', info.result.value);
        const s = await send('Page.captureScreenshot', { format: 'jpeg', quality: 95 });
        const b = Buffer.from(s.data, 'base64');
        fs.writeFileSync(OUT, b);
        console.log(OUT, b.length, 'bytes');
      } catch (e) { console.log('ERR', e.message); }
      process.exit(0);
    };
  });
}).end();
