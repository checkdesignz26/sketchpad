import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  cdp=pg.context.new_cdp_session(pg)
  ev=lambda t,x,y:cdp.send('Input.dispatchMouseEvent',{'type':t,'x':x,'y':y,'button':'left','buttons':1 if t!='mouseReleased' else 0,'clickCount':1,'pointerType':'pen','force':.5})
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  S=lambda:js("window.__sketchpadGetState().strokes")
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  def held(x0,y0,x1,y1,then=None,wait=900):
    ev('mousePressed',x0,y0)
    for i in range(1,26):ev('mouseMoved',x0+(x1-x0)*i/25+math.sin(i)*0.4,y0+(y1-y0)*i/25)
    pg.wait_for_timeout(wait)
    if then:
      for i in range(1,12):ev('mouseMoved',then[0]+0*i,then[1]) if False else None
      steps=10;lx,ly=x1,y1
      for i in range(1,steps+1):ev('mouseMoved',lx+(then[0]-lx)*i/steps,ly+(then[1]-ly)*i/steps)
      pg.wait_for_timeout(150)
    g=js("document.getElementById('selectionBox').parentNode.querySelectorAll('svg line').length")
    ev('mouseReleased',*(then or (x1,y1)));pg.wait_for_timeout(500);return g
  ang=lambda s:(math.degrees(math.atan2(s['shape']['y1']-s['shape']['y0'],s['shape']['x1']-s['shape']['x0'])) if s.get('shape') else None)
  # 1: a line ~3 degrees off horizontal, held: becomes exactly horizontal
  g=held(cx-200,cy-120,cx+100,cy-120+16);s=S()[-1];print('shape',s.get('shape'))
  ok(s.get('shape') and s['shape']['type']=='line' and abs(s['shape']['y1']-s['shape']['y0'])<1e-6,'a held line a few degrees off horizontal locks to exactly horizontal')
  ok(g>=1,'a guide line is shown while it is locked (%d)'%g)
  # 2: a line near 45 degrees
  held(cx-200,cy-40,cx-200+150,cy-40+150*math.tan(math.radians(41)));s=S()[-1]
  ok(abs(abs(ang(s))-45)<1e-6,'a held line near 45 degrees locks to 45 (%.4f)'%ang(s))
  # 3: dragging the held line round: swings onto vertical when within 7 degrees
  held(cx+150,cy-100,cx+300,cy-100,then=(cx+150+8,cy+60));s=S()[-1]
  ok(abs(abs(ang(s))-90)<1e-6,'dragging the held line near vertical locks it to 90 degrees (%.4f)'%ang(s))
  # 4: a line well off any angle is left alone
  held(cx-250,cy+60,cx-100,cy+60+150*math.tan(math.radians(22)));s=S()[-1];a=ang(s)
  ok(abs(a-22)<3 and abs(a-round(a/45)*45)>5,'a line 22 degrees off is not forced to an angle (%.2f)'%a)
  # 5: off in the View menu: no lock
  js("document.getElementById('viewSmartBtn').click()")
  held(cx-250,cy+140,cx+50,cy+140+16);s=S()[-1]
  ok(abs(s['shape']['y1']-s['shape']['y0'])>3,'with Smart guides off the held line is left at its own angle')
  print(errs);b.close()
