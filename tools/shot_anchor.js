// 截取带锚点的页面视口，确认吸顶导航没有盖住区块标题
// usage: node tools/shot_anchor.js <width> <out.jpg> <page.html#anchor>
const http=require('http'),fs=require('fs');
const W=+process.argv[2]||1440, OUT=process.argv[3]||'shots/anchor.jpg', URL=process.argv[4];
http.request({host:'127.0.0.1',port:9222,path:'/json/new?about:blank',method:'PUT'},r=>{
let d='';r.on('data',c=>d+=c);r.on('end',()=>{
const ws=new WebSocket(JSON.parse(d).webSocketDebuggerUrl);let id=0;
const send=(m,p={})=>new Promise((res,rej)=>{const i=++id;ws.send(JSON.stringify({id:i,method:m,params:p}));
const h=e=>{const x=JSON.parse(e.data);if(x.id===i){ws.removeEventListener('message',h);x.error?rej(new Error(JSON.stringify(x.error))):res(x.result);}};
ws.addEventListener('message',h);setTimeout(()=>rej(new Error('timeout '+m)),25000);});
const ev=x=>send('Runtime.evaluate',{expression:x,returnByValue:true,awaitPromise:true}).then(o=>o.result&&o.result.value);
ws.onopen=async()=>{
  await send('Page.enable');await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:2,mobile:false});
  await send('Page.navigate',{url:'http://127.0.0.1:8788/'+URL});
  await new Promise(r=>setTimeout(r,2400));
  await ev('document.fonts.ready.then(()=>1)');
  await new Promise(r=>setTimeout(r,800));
  console.log(await ev(`(()=>{const el=document.querySelector(':target');const r=el.getBoundingClientRect();const h=el.querySelector('h2');const hr=h?h.getBoundingClientRect():null;return JSON.stringify({target:el.id,top:Math.round(r.top),headingTop:hr?Math.round(hr.top):null,navH:document.querySelector('.nav').getBoundingClientRect().height})})()`));
  const s=await send('Page.captureScreenshot',{format:'jpeg',quality:92});
  fs.writeFileSync(OUT,Buffer.from(s.data,'base64'));
  console.log('->',OUT);
  process.exit(0);
};});}).end();
