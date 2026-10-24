import sys;import os;sys.path.insert(0,os.path.dirname(__file__))
import common as t500
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b,pg,errs=t500.boot(p);js=pg.evaluate
  # two teardrop strokes (A,B) then a blend between them
  for (x0,y0,x1,y1) in [(400,250,480,330),(700,450,860,610)]:
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(300)
    pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
  ids=js("window.__sketchpadGetState().strokes.map(s=>s.id)");print(len(ids))
  r=js("(ids)=>{const I=window.__sketchpadInternals();const sp=I.blendSpecOf({id:crypto.randomUUID(),aId:ids[0],bId:ids[1],steps:5,colour:true,shape:true,pos:true,size:true,rot:true});return JSON.stringify(I.blendInstall(sp)).slice(0,200)}",ids);print(r)
  pg.wait_for_timeout(300)
  print('strokes',js("window.__sketchpadGetState().strokes.length"))
  js("window.__sketchpadInternals().pushHist()")
  js("window.__sketchpadCanvasTiling.set(2,true)");pg.wait_for_timeout(500)
  snap="""()=>{const c=document.getElementById('canvas'),k=c.width/1800,TW=780,o=(1800-TW)/2;const t=document.createElement('canvas');t.width=200;t.height=200;const g=t.getContext('2d');g.drawImage(c,o*k,o*k,TW*k,TW*k,0,0,200,200);return Array.from(g.getImageData(0,0,200,200).data)}"""
  A=js(snap)
  js("document.getElementById('tbRepeatPill').click()");pg.wait_for_timeout(300);js("document.getElementById('cvtNewBtn').click()");pg.wait_for_timeout(2500)
  pg.locator('.col-card').nth(1).click();pg.wait_for_timeout(3000)
  B=js(snap)
  print('diff',sum(abs(x-y) for x,y in zip(A,B))/len(A),'strokes in copy',js("window.__sketchpadGetState().strokes.length"),'with blendId',js("window.__sketchpadGetState().strokes.filter(s=>s.blendId).length"))
  print(errs);b.close()
