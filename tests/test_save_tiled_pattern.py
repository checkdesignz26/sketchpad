# Save as New Pattern (Canvas Tiling): one independent editable pattern in the filmstrip. Run with the server on :8790.
import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m,x=''):print(('PASS ' if c else 'FAIL ')+m,x);return c
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate;res=[]
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  for i,(dx,dy) in enumerate([(-80,-60),(40,-30),(-30,70)]):
    pg.mouse.move(cx+dx,cy+dy);pg.mouse.down();pg.mouse.move(cx+dx+50,cy+dy+30,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
  S=lambda:js("window.__sketchpadGetState().strokes.map(s=>({id:s.id,x:s.points[0].x,y:s.points[0].y,sz:(s.settings&&s.settings.size)||null,col:s.color}))")
  base=S();print('base',len(base))
  for lay in ['grid','halfDrop','halfBrick']:
    pg.evaluate("l=>document.querySelector('.layout-btn[data-layout='+l+']').click()",lay)
    n=3 if lay=='grid' else 2
    js("n=>window.__sketchpadCanvasTiling.set(n,true)",n);pg.wait_for_timeout(300)
    st=js("(()=>{const s=window.__sketchpadCanvasTiling.materialise();return {n:JSON.parse(s.strokesJSON).length,ids:new Set(JSON.parse(s.strokesJSON).map(x=>x.id)).size,ct:s.canvasTiling,layers:JSON.parse(s.layersJSON).map(l=>l.id)}})()")
    res.append(ok(st['n']==len(base)*n*n and st['ids']==st['n'] and st['ct']==1,lay+' materialised count/unique ids',st))
  pg.evaluate("l=>document.querySelector('.layout-btn[data-layout='+l+']').click()",'grid')
  js("window.__sketchpadCanvasTiling.set(3,true)");pg.wait_for_timeout(300)
  before=js("document.querySelectorAll('.col-card').length")
  js("window.__sketchpadCanvasTiling.set(2,true)");js("window.__sketchpadCanvasTiling.set(3,true)");js("window.__sketchpadCanvasTiling.set(1,true)");js("window.__sketchpadCanvasTiling.set(3,true)")
  pg.wait_for_timeout(300)
  res.append(ok(js("(window.__sketchpadGetState().strokes.length)")==len(base),'switching scales created nothing'))
  pg.click('#tbRepeatPill');pg.wait_for_timeout(400)
  pg.click('#cvtNewBtn');pg.wait_for_timeout(1500)
  cards=js("[...document.querySelectorAll('.col-card')].map(c=>c.textContent.trim().slice(0,40))")
  print('cards',cards)
  res.append(ok(len(cards)==2,'exactly one new filmstrip entry'))
  res.append(ok(len(S())==len(base)*9,'new pattern opened straight away for editing',len(S())))
  nm=js("[...document.querySelectorAll('.col-card')].map(c=>c.textContent)");res.append(ok(any('— 3×3' in t for t in nm),'auto name uses an em dash and the count',nm))
  # open the new pattern
  pg.locator('.col-card').nth(1).click();pg.wait_for_timeout(2500)
  ns=S();print('new strokes',len(ns))
  res.append(ok(len(ns)==len(base)*9,'new pattern has nine independent copies of every stroke'))
  res.append(ok(js("window.__sketchpadCanvasTiling.get()")==1,'new pattern is a normal 1x1 pattern'))
  res.append(ok(len(set(x['id'] for x in ns)&set(x['id'] for x in base))==0,'no shared ids with the original'))
  # edit one stroke in the new pattern: recolour + delete another; then original must not change
  js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes[0];s.color='#ff0000';I.rebuildAllLayers();I.pushHist();})()")
  js("(()=>{const I=window.__sketchpadInternals();I.strokes.splice(1,1);I.rebuildAllLayers();I.pushHist();})()")
  pg.wait_for_timeout(300)
  res.append(ok(len(S())==len(base)*9-1 and S()[0]['col']=='#ff0000','edited new pattern (recolour/delete)'))
  pg.screenshot(path='tiled_new.png')
  pg.locator('.col-card').nth(0).click();pg.wait_for_timeout(2500)
  a=S();same=len(a)==len(base) and all(u['id']==v['id'] and abs(u['x']-v['x'])<0.05 and abs(u['y']-v['y'])<0.05 and u['col']==v['col'] for u,v in zip(a,base))
  res.append(ok(same,'switching back: original unchanged',(a[:1],base[:1])))
  res.append(ok(js("window.__sketchpadCanvasTiling.get()")==3,'original tiling setting restored'))
  pg.locator('.col-card').nth(1).click();pg.wait_for_timeout(2500)
  res.append(ok(len(S())==len(base)*9-1 and S()[0]['col']=='#ff0000','new pattern edits restored on switch'))
  print('errs',errs);print('ALL PASS' if all(res) and not errs else 'SOME FAILED');b.close()
