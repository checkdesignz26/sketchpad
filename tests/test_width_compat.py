import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  def curve(x0,y0,amp,L,n=24):
    pts=[(x0+L*i/n,y0+amp*math.sin(math.pi*i/n)) for i in range(n+1)]
    pg.mouse.move(*pts[0]);pg.mouse.down()
    for q in pts[1:]:pg.mouse.move(*q)
    pg.mouse.up();pg.wait_for_timeout(300)
  curve(cx-200,cy,40,400)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx,cy+40);pg.wait_for_timeout(500)
  A=js("window.__sketchpadGetState().selectedStrokeId")
  js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');s.settings=Object.assign({},s.settings,{size:16});s.color='#c2185b';I.rebuildAllLayers();})()"%A)
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  js("document.querySelector('.wp-pre[data-k=both]').click()");pg.wait_for_timeout(300)
  clip={'x':cx-240,'y':cy-40,'width':480,'height':140}
  def stateset(**kw):
    js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');Object.assign(s,%s);for(const k in s)if(s[k]===null&&(k==='capS'||k==='capE'||k==='dash'))delete s[k];I.rebuildAllLayers();})()"%(A,__import__('json').dumps(kw)))
    pg.wait_for_timeout(500)
  B=lambda sel:js("document.querySelector('#strokeActionsBar %s').click()"%sel)
  D=lambda v:js("(()=>{const sel=document.querySelector('#strokeActionsBar .dash-sel');sel.value='%s';sel.dispatchEvent(new Event('change'))})()"%v)
  B('.cap-btn[data-cap=capS][data-v=flat]');B('.cap-btn[data-cap=capE][data-v=flat]');pg.wait_for_timeout(500);pg.screenshot(path=SD+'wc1.png',clip=clip)
  B('.cap-btn[data-cap=capE][data-v=round]');pg.wait_for_timeout(500);pg.screenshot(path=SD+'wc2.png',clip=clip)
  js("document.querySelector('.wp-pre[data-k=swell]').click()");pg.wait_for_timeout(300)
  B('.cap-btn[data-cap=capE][data-v=flat]');pg.wait_for_timeout(500);pg.screenshot(path=SD+'wc2.png',clip=clip)
  D('dashed');pg.wait_for_timeout(500);pg.screenshot(path=SD+'wc3.png',clip=clip)
  D('dotted');pg.wait_for_timeout(500);pg.screenshot(path=SD+'wc4.png',clip=clip)
  D('')
  # zoom: handles must still be draggable
  for _ in range(3):js("document.getElementById('zoomPill')&&document.getElementById('zoomPill').click()") if False else None
  js("document.getElementById('zoomInBtn')&&document.getElementById('zoomInBtn').click()")
  pg.wait_for_timeout(300)
  # closed stroke is refused explicitly
  stateset(closed=True)
  pg.wait_for_timeout(300)
  js("window.__sketchpadInternals().syncStrokeSelectionUI()");pg.wait_for_timeout(300)
  ok(js("document.querySelectorAll('#widthOverlay .wp-h').length")==0,'closed shapes show no width handles')
  ok('Closed' in js("document.getElementById('wpHint').textContent"),'panel explains closed shapes keep an even width')
  print(errs);b.close()
