# Canvas Tiling 1x1/2x2/3x3: display-only pattern scale. Run: python3 tests/test_canvas_tiling.py (server on :8790)
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def px(pg,x,y):return pg.evaluate("([x,y])=>{const c=document.getElementById('canvas').getContext('2d').getImageData(x,y,1,1).data;return [c[0],c[1],c[2]]}",[x,y])
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  geo=js("(()=>{const I=window.__sketchpadInternals();return null})()")
  # draw one dot-ish stroke with the pen in the middle of the tile
  def tile():return js("(()=>{const s=window.__sketchpadGetState();return {TW:s.tileW||s.TW,TH:s.tileH||s.TH}})()")
  print('state keys',js("Object.keys(window.__sketchpadGetState())"))
  def strokes():return js("window.__sketchpadGetState().strokes.map(s=>({n:s.points.length,x:s.points[0].x,y:s.points[0].y,x1:s.points[s.points.length-1].x}))")
  r=pg.locator('#canvas').bounding_box()
  cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  pg.mouse.move(cx-40,cy);pg.mouse.down();pg.mouse.move(cx+40,cy+10,steps=10);pg.mouse.up();pg.wait_for_timeout(400)
  s1=strokes();print('1x1 stroke',s1)
  ok=True
  for lay in ['grid','halfDrop','halfBrick']:
    js("(l)=>document.querySelector('.layout-btn[data-layout='+l+']').click()",lay) if False else pg.evaluate("l=>document.querySelector('.layout-btn[data-layout='+l+']').click()",lay)
    pg.wait_for_timeout(300)
    for n in [2,3,1]:
      pg.evaluate("n=>window.__sketchpadCanvasTiling.set(n,true)",n);pg.wait_for_timeout(500)
      print(lay,n,'effective',js("window.__sketchpadCanvasTiling.n()"),'strokes unchanged',strokes()==s1)
      ok&=strokes()==s1
  # draw at 3x3 in the middle: fold keeps stroke in source coords, continuous
  pg.evaluate("l=>document.querySelector('.layout-btn[data-layout='+l+']').click()",'grid')
  pg.evaluate("window.__sketchpadCanvasTiling.set(3,true)");pg.wait_for_timeout(500)
  pg.mouse.move(cx+120,cy+80);pg.mouse.down();pg.mouse.move(cx+200,cy+120,steps=10);pg.mouse.up();pg.wait_for_timeout(500)
  s2=strokes();print('after 3x3 draw',s2)
  d=s2[-1];print('new stroke span in source px',round(d['x1']-d['x'],1),'(screen span ~80 css px; expect larger than that / scale 1/3)')
  pg.screenshot(path='cvt3.png')
  pg.evaluate("window.__sketchpadCanvasTiling.set(2,true)");pg.wait_for_timeout(500);pg.screenshot(path='cvt2.png')
  pg.evaluate("window.__sketchpadCanvasTiling.set(1,true)");pg.wait_for_timeout(500);pg.screenshot(path='cvt1.png')
  for n in (4,8):
    js("n=>window.__sketchpadCanvasTiling.set(n,true)",n);pg.wait_for_timeout(300);print('n',n,'effective',js('window.__sketchpadCanvasTiling.n()'))
  js('window.__sketchpadCanvasTiling.set(99,true)');print('clamped',js('window.__sketchpadCanvasTiling.get()'))
  js('window.__sketchpadCanvasTiling.set(1,true)')
  print('errs',errs);print('OK' if ok and not errs else 'FAIL')
  b.close()
