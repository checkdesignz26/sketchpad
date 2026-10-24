import sys;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  js("(()=>{const s=document.getElementById('brushSize');if(s){s.value=40;s.dispatchEvent(new Event('input',{bubbles:true}));}})()")
  pg.mouse.move(cx-150,cy);pg.mouse.down();pg.mouse.move(cx+150,cy,steps=12);pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx,cy);pg.wait_for_timeout(600)
  assert js("window.__sketchpadGetState().selectedStrokeId"),'no stroke'
  clip={'x':cx-190,'y':cy-50,'width':380,'height':100}
  vis=js("(()=>{const b=document.querySelector('#strokeActionsBar .cap-btn');const r=b.getBoundingClientRect();return [getComputedStyle(document.getElementById('strokeActionsBar')).display,r.width,r.height]})()");print('bar cap btn',vis);assert vis[0]!='none' and vis[1]>0
  js("document.querySelector('#strokeActionsBar .cap-btn[data-cap=capS][data-v=flat]').click()");pg.wait_for_timeout(300)
  pg.screenshot(path=SD+'cap_sq_start.png',clip=clip)
  js("document.querySelector('#strokeActionsBar .cap-btn[data-cap=capE][data-v=flat]').click()");pg.wait_for_timeout(300)
  js("(()=>{const s=document.querySelector('#strokeActionsBar .dash-sel');s.value='dashed';s.dispatchEvent(new Event('change'))})()");pg.wait_for_timeout(300)
  pg.screenshot(path=SD+'cap_dash_sq.png',clip=clip)
  js("document.querySelector('#strokeActionsBar .cap-btn[data-cap=capS][data-v=round]').click();document.querySelector('#strokeActionsBar .cap-btn[data-cap=capE][data-v=round]').click()")
  js("(()=>{const s=document.querySelector('#strokeActionsBar .dash-sel');s.value='dotted';s.dispatchEvent(new Event('change'))})()");pg.wait_for_timeout(300)
  pg.screenshot(path=SD+'cap_dotted.png',clip=clip)
  print(errs);b.close()
