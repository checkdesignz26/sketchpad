# The saved tiled pattern must LOOK like the tiled canvas (same pattern, smaller scale). Flower with fills + a plain stroke.
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
import common as t500
from playwright.sync_api import sync_playwright
def mk(pg):
    js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(500)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    pg.locator('#pathEditBar button:has-text("Fill:")').first.click();pg.wait_for_timeout(400)
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(400)
SNAP="""()=>{const c=document.getElementById('canvas');const t=document.createElement('canvas');t.width=300;t.height=300;const g=t.getContext('2d');
 const CX=(%s),k=1;g.drawImage(c,0,0,c.width,c.height,0,0,300,300);return Array.from(g.getImageData(0,0,300,300).data)}"""
def diff(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
with sync_playwright() as p:
  b,pg,errs=t500.boot(p);js=pg.evaluate
  mk(pg)
  print('strokes',js("window.__sketchpadGetState().strokes.map(s=>[!!s.radial,s.radialOf?1:0,s.fillOf?1:0,!!s.fillColor,!!s.fill,s.points.length].join(''))"))
  for n in (2,3):
    js("n=>window.__sketchpadCanvasTiling.set(n,true)",n);pg.wait_for_timeout(600)
    # frame as shown: the tile frame region of the main canvas (CX..CX+TW)
    A=js("""()=>{const c=document.getElementById('canvas'),I=window.__sketchpadGetState();const k=c.width/1800,TW=%d;const o=(1800-TW)/2;const t=document.createElement('canvas');t.width=200;t.height=200;const g=t.getContext('2d');g.drawImage(c,o*k,o*k,TW*k,TW*k,0,0,200,200);return Array.from(g.getImageData(0,0,200,200).data)}"""%780)
    js("document.getElementById('tbRepeatPill').click()");pg.wait_for_timeout(300);js("document.getElementById('cvtNewBtn').click()");pg.wait_for_timeout(2500)
    cards=pg.locator('.col-card').count()
    pg.locator('.col-card').nth(cards-1 if n==2 else 1).click();pg.wait_for_timeout(3000)
    B=js("""()=>{const c=document.getElementById('canvas'),k=c.width/1800,TW=780,o=(1800-TW)/2;const t=document.createElement('canvas');t.width=200;t.height=200;const g=t.getContext('2d');g.drawImage(c,o*k,o*k,TW*k,TW*k,0,0,200,200);return Array.from(g.getImageData(0,0,200,200).data)}""")
    print(n,'mean abs diff frame (0-255):',round(diff(A,B),2),'strokes in copy',js("window.__sketchpadGetState().strokes.length"))
    pg.locator('.col-card').nth(0).click();pg.wait_for_timeout(3000)
  print(errs);b.close()
