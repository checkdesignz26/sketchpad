from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':1180,'height':820},has_touch=True);pg=ctx.new_page();js=pg.evaluate
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
  def pen(a):cdp.send('Input.dispatchMouseEvent',a|{'x':X,'y':Y,'pointerType':'pen'})
  def go(hold,fingers=2,penmove=0,fmove=0):
    pen({'type':'mouseMoved'});pen({'type':'mousePressed','button':'left','buttons':1,'clickCount':1,'force':.5})
    pts=lambda k:[{'x':cx+60+i*70+fmove*k,'y':cy+120,'id':i+1} for i in range(fingers)]
    if fingers:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':pts(0)})
    pg.wait_for_timeout(hold)
    if penmove:cdp.send('Input.dispatchMouseEvent',{'type':'mouseMoved','x':X+penmove,'y':Y,'button':'left','buttons':1,'pointerType':'pen','force':.5})
    if fmove:
      for k in (.5,1):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':pts(k)})
    pg.wait_for_timeout(700 if (penmove or fmove) else 100)
    if fingers:cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    pen({'type':'mouseReleased','button':'left','buttons':0,'clickCount':1});pg.wait_for_timeout(400)
  go(150,fingers=0);ok(bool(js("window.__sketchpadGetState().selectedStrokeId")),'selected')
  n0=n();go(900,fingers=0);ok(n()==n0,'Pencil hold alone does not duplicate')
  n0=n();go(900);ok(n()==n0+1,'Pencil held with two fingers duplicates (%d -> %d)'%(n0,n()))
  n0=n();go(300,fmove=40);ok(n()==n0,'moving the fingers cancels it')
  n0=n();go(300,penmove=40);ok(n()==n0,'moving the Pencil cancels it')
  js("document.getElementById('dblDupChk').click()")
  n1=n();go(900);ok(n()==n1,'off in the View menu: no duplicate')
  print(errs);b.close()
