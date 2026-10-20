import sys;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def get(js,e):return js(e)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  js("(()=>{const s=document.getElementById('brushSize');if(s){s.value=24;s.dispatchEvent(new Event('input',{bubbles:true}));}})()")
  pg.mouse.move(cx-200,cy);pg.mouse.down();pg.mouse.move(cx+200,cy,steps=14);pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx,cy);pg.wait_for_timeout(600)
  assert js("window.__sketchpadGetState().selectedStrokeId"),'no stroke'
  js("document.querySelector('#strokeActionsBar .wp-toggle').click()");pg.wait_for_timeout(300)
  n=js("document.querySelectorAll('#widthOverlay .wp-h').length");print('handles',n);assert n==4
  js("(()=>{const s=document.querySelector('#strokeActionsBar .wp-preset');s.value='swell';s.dispatchEvent(new Event('change'))})()");pg.wait_for_timeout(400)
  n=js("document.querySelectorAll('#widthOverlay .wp-h').length");print('after swell handles',n);assert n==6
  clip={'x':cx-240,'y':cy-90,'width':480,'height':180}
  pg.screenshot(path=SD+'w_swell.png',clip=clip)
  # drag the middle upper handle further out
  hs=js("[...document.querySelectorAll('#widthOverlay .wp-h')].map(h=>[h.style.left,h.style.top,h._q.t,h._side])")
  mid=[h for h in hs if abs(h[2]-.5)<.01 and h[3]==1][0]
  box=pg.locator('#canvasWrap').bounding_box()
  x=box['x']+float(mid[0][:-2]);y=box['y']+float(mid[1][:-2])
  w0=js("[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>Math.abs(h._q.t-.5)<.01)._q.w")
  pg.mouse.move(x,y);pg.mouse.down();pg.mouse.move(x,y-30,steps=6);pg.mouse.up();pg.wait_for_timeout(400)
  w1=js("[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>Math.abs(h._q.t-.5)<.05)._q.w");print('w',w0,w1)
  assert abs(w1-w0)>.1
  # tap line to add a point
  pg.mouse.click(cx-120,cy);pg.wait_for_timeout(400)
  n=js("document.querySelectorAll('#widthOverlay .wp-h').length");print('after tap add',n);assert n==8
  pg.screenshot(path=SD+'w_after.png',clip=clip)
  js("document.querySelector('#strokeActionsBar .wp-reset').click()");pg.wait_for_timeout(300)
  n=js("document.querySelectorAll('#widthOverlay .wp-h').length");assert n==4
  print(errs);b.close()
