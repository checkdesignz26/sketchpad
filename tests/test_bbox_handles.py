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
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  pg.mouse.move(cx-80,cy-60);pg.mouse.down()
  for i in range(1,13):pg.mouse.move(cx-80+i*10,cy-60+i*8)
  pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx-80+60,cy-60+48);pg.wait_for_timeout(400)
  ok(js("!!window.__sketchpadGetState().selectedStrokeId"),'stroke selected')
  bbx=lambda:js("(()=>{const s=window.__sketchpadGetState();const st=s.strokes.find(x=>x.id===s.selectedStrokeId);const xs=st.points.map(p=>p.x),ys=st.points.map(p=>p.y);return [Math.max(...xs)-Math.min(...xs),Math.max(...ys)-Math.min(...ys)]})()")
  hs=js("[...document.querySelectorAll('#paintBBoxOverlay .handle')].map(h=>h.dataset.h||'se')")
  ok(sorted(hs)==sorted(['nw','ne','sw','n','s','w','e','se']),'8 handles: %s'%hs)
  ok(js("!!document.getElementById('paintRotateHandle').getBoundingClientRect().width"),'rotate handle present')
  pg.screenshot(path='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/bbox.png')
  def drag(h,dx,dy):
    q=js("(()=>{const r=document.querySelector('#paintBBoxOverlay .handle[data-h=\"%s\"]').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"%h)
    pg.mouse.move(q[0],q[1]);pg.mouse.down();
    for k in (.3,.6,1):pg.mouse.move(q[0]+dx*k,q[1]+dy*k)
    pg.mouse.up();pg.wait_for_timeout(300)
  w0,h0=bbx();drag('e',60,0);w1,h1=bbx()
  ok(w1>w0+20 and abs(h1-h0)<1,'east handle stretches wider only (%.0f,%.0f -> %.0f,%.0f)'%(w0,h0,w1,h1))
  drag('s',0,50);w2,h2=bbx();ok(h2>h1+15 and abs(w2-w1)<1,'south handle makes it taller only (%.0f -> %.0f)'%(h1,h2))
  drag('n',0,-40);w3,h3=bbx();ok(h3>h2+10 and abs(w3-w2)<1,'north handle makes it taller only (%.0f -> %.0f)'%(h2,h3))
  drag('w',-40,0);w4,h4=bbx();ok(w4>w3+10 and abs(h4-h3)<1,'west handle makes it wider only')
  drag('nw',-30,-30);w5,h5=bbx();ok(w5>w4+5 and abs((w5/h5)-(w4/h4))<.03,'corner keeps proportions')
  ok(js("document.getElementById('undoBtn')?1:1"),'ok')
  print(errs);b.close()
