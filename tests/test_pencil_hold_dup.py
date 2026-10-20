from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':1180,'height':820});pg=ctx.new_page();js=pg.evaluate
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://localhost:8790/index.html');pg.wait_for_timeout(2000)
  pg.locator('button:has-text("New Project"):visible').first.click();pg.wait_for_timeout(600)
  pg.locator('button:has-text("Start drawing")').click();pg.wait_for_timeout(2500)
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  cdp=ctx.new_cdp_session(pg);n=lambda:len(js("window.__sketchpadGetState().strokes"))
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  pg.mouse.move(cx-80,cy-60);pg.mouse.down()
  for i in range(1,13):pg.mouse.move(cx-80+i*10,cy-60+i*8)
  pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  X,Y=cx-80+60,cy-60+48
  def pen(hold,move=0):
    cdp.send('Input.dispatchMouseEvent',{'type':'mouseMoved','x':X,'y':Y,'pointerType':'pen'})
    cdp.send('Input.dispatchMouseEvent',{'type':'mousePressed','x':X,'y':Y,'button':'left','buttons':1,'clickCount':1,'pointerType':'pen','force':.5})
    pg.wait_for_timeout(hold)
    if move:cdp.send('Input.dispatchMouseEvent',{'type':'mouseMoved','x':X+move,'y':Y,'button':'left','buttons':1,'pointerType':'pen','force':.5})
    pg.wait_for_timeout(hold if move else 100)
    cdp.send('Input.dispatchMouseEvent',{'type':'mouseReleased','x':X+move,'y':Y,'button':'left','buttons':0,'clickCount':1,'pointerType':'pen'});pg.wait_for_timeout(400)
  pen(150);ok(js("!!window.__sketchpadGetState().selectedStrokeId"),'selected with a quick Pencil tap')
  n0=n();pen(900);ok(n()==n0+1,'holding the Pencil on the selection duplicates (%d -> %d)'%(n0,n()))
  n0=n();pen(250,move=30);ok(n()==n0,'dragging with the Pencil does not duplicate')
  X+=30
  js("document.getElementById('dblDupChk').click()")
  n1=n();pen(900);ok(n()==n1,'off in the View menu: no duplicate')
  print(errs);b.close()
