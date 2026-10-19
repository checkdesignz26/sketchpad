# One export path: default 3600x3600 @300dpi, custom size, transparent, no double tiling, no tiled-export panel. Server on :8790.
import sys,os,json,struct;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m,x=''):print(('PASS ' if c else 'FAIL ')+m,x);return c
B64="""(async(w,h,t)=>{const E=window.__sketchpadExport;const r=await E.png(w,h,300,t);const bm=await createImageBitmap(r.blob);
const c=document.createElement('canvas');c.width=bm.width;c.height=bm.height;const g=c.getContext('2d');g.drawImage(bm,0,0);
const col=x=>{const d=g.getImageData(x,0,1,bm.height).data;return Array.from(d)};
const L=g.getImageData(0,0,1,bm.height).data,R=g.getImageData(bm.width-1,0,1,bm.height).data;let diff=0;for(let i=0;i<L.length;i++)diff+=Math.abs(L[i]-R[i]);
const a=g.getImageData(0,0,1,1).data[3];
const buf=new Uint8Array(await r.blob.arrayBuffer());let phys=null;for(let i=8;i<buf.length-12;){const len=(buf[i]<<24|buf[i+1]<<16|buf[i+2]<<8|buf[i+3])>>>0;const ty=String.fromCharCode(...buf.slice(i+4,i+8));if(ty==='pHYs'){phys=((buf[i+8]<<24|buf[i+9]<<16|buf[i+10]<<8|buf[i+11])>>>0);break;}i+=12+len;}
return {w:bm.width,h:bm.height,edge:diff/L.length,alpha:a,ppm:phys};})"""
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate;res=[]
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  for dx,dy in [(-80,-60),(40,-30)]:
    pg.mouse.move(cx+dx,cy+dy);pg.mouse.down();pg.mouse.move(cx+dx+60,cy+dy+40,steps=6);pg.mouse.up();pg.wait_for_timeout(250)
  d=js("window.__sketchpadExport.defaults()");res.append(ok(d['w']==3600 and d['h']==3600 and d['dpi']==300,'default export 3600x3600 @300',d))
  o=js(B64+"(900,900,false)")  # smaller probe keeps the test fast; same code path as 3600
  res.append(ok(o['w']==900 and o['h']==900,'requested size, not the 780 canvas',o))
  res.append(ok(o['ppm']==11811,'300 dpi written',o['ppm']))
  res.append(ok(o['edge']<2,'left/right edges match (seamless)',o['edge']))
  t=js(B64+"(1200,1200,true)");res.append(ok(t['alpha']==0 and t['w']==1200,'transparent PNG',t))
  full=js("(async()=>{const r=await window.__sketchpadExport.png(3600,3600,300,false);return [r.w,r.h,r.blob.size]})()")
  res.append(ok(full[:2]==[3600,3600],'full 3600x3600 export works',full))
  res.append(ok(js("window.__sketchpadExport.check(20000,20000)")!='' ,'oversize refused with a message'))
  # custom dialog
  js("window.__sketchpadExport.open()");pg.wait_for_timeout(200)
  pg.fill('#expW','1000');res.append(ok(js("document.getElementById('expH').value")=='1000','height follows width (tile shape kept)'))
  res.append(ok(js("!!document.querySelector('#tilePopover,#tileSaveBtn,#tileRes')")==False,'no tiled-export panel remains'))
  js("document.getElementById('expPopover').classList.remove('open')")
  # saved 2x2 must export as its own tile, not become 4x4
  n0=js("window.__sketchpadGetState().strokes.length")
  pg.click('#tbRepeatPill');pg.wait_for_timeout(300)
  js("window.__sketchpadCanvasTiling.set(2,true)");pg.wait_for_timeout(300)
  pg.click('#cvtNewBtn');pg.wait_for_timeout(2500)
  n1=js("window.__sketchpadGetState().strokes.length")
  res.append(ok(n1==n0*4 and js("window.__sketchpadCanvasTiling.get()")==1,'saved 2x2 holds four copies, tiling reset',(n0,n1)))
  d2=js("window.__sketchpadExport.defaults()");res.append(ok(d2['w']==3600,'saved pattern still exports at 3600',d2))
  o2=js(B64+"(900,900,false)");res.append(ok(o2['w']==900 and o2['edge']<2,'saved pattern export seamless',o2))
  print('errs',errs);print('ALL PASS' if all(res) and not errs else 'SOME FAILED');b.close()
