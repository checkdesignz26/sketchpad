import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':1180,'height':820},has_touch=True);pg=ctx.new_page();js=pg.evaluate
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://localhost:8790/index.html');pg.wait_for_timeout(2000)
  pg.locator('button:has-text("New Project"):visible').first.click();pg.wait_for_timeout(600)
  pg.locator('button:has-text("Start drawing")').click();pg.wait_for_timeout(2500)
  cdp=ctx.new_cdp_session(pg)
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  n=lambda:len(js("window.__sketchpadGetState().strokes"))
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  pg.mouse.move(cx-80,cy-80);pg.mouse.down()
  for i in range(1,13):pg.mouse.move(cx-80+i*10,cy-80+i*4)
  pg.mouse.up();pg.wait_for_timeout(300)
  def touch2(dx=0,hold=80,sep=60):
    pts=lambda k:[{'x':cx+10+(-sep/2)+dx*k,'y':cy-40,'id':1},{'x':cx+10+sep/2+dx*k,'y':cy-40,'id':2}]
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':pts(0)})
    pg.wait_for_timeout(hold)
    if dx:
      for k in (.3,.6,1):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':pts(k)});pg.wait_for_timeout(30)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});pg.wait_for_timeout(500)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx-20,cy-80+4*6);pg.wait_for_timeout(400)
  ok(js("!!window.__sketchpadGetState().selectedStrokeId"),'stroke selected')
  n0=n();touch2(dx=40);ok(n()==n0,'a two-finger drag (pan / pinch) does not duplicate')
  touch2(hold=900);ok(n()==n0,'two fingers held alone do NOT duplicate (needs the Pencil too)')
  # Undo is still what a two-finger tap does outside Edit mode / with nothing selected
  js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.move(cx+100,cy+60);pg.mouse.down()
  for i in range(1,9):pg.mouse.move(cx+100+i*8,cy+60+i*5)
  pg.mouse.up();pg.wait_for_timeout(400)
  n2=n();touch2();ok(n()==n2-1,'in Draw mode a two-finger tap is still Undo (%d -> %d)'%(n2,n()))
  print(errs);b.close()
