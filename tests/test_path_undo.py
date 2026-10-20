from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':1180,'height':1150});pg=ctx.new_page();js=pg.evaluate
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://localhost:8790/index.html');pg.wait_for_timeout(2000)
  pg.locator('button:has-text("New Project"):visible').first.click();pg.wait_for_timeout(600)
  pg.locator('button:has-text("Start drawing")').click();pg.wait_for_timeout(2500)
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  pg.mouse.move(cx-100,cy-60);pg.mouse.down()
  for i in range(1,7):
    for k in range(1,9):pg.mouse.move(cx-100+(i-1)*50+k*50/8,cy-60+(70 if i%2 else 0)*(k/8)+(0 if i%2 else 70)*(1-k/8))
  pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx-100+25,cy-60+35);pg.wait_for_timeout(300)
  if not js("!!window.__sketchpadGetState().selectedStrokeId"):
    st=js("(()=>{const s=window.__sketchpadGetState().strokes[0];return s.points[10]})()");pg.mouse.click(r['x']+st['x']*r['width']/1800,r['y']+st['y']*r['height']/1800);pg.wait_for_timeout(300)
  ok(js("!!window.__sketchpadGetState().selectedStrokeId"),'stroke selected')
  js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(500)
  nodes=lambda:js("[...document.querySelectorAll('#pathNodeOverlay .path-node')].map(n=>{const r=n.getBoundingClientRect();return [Math.round(r.x+r.width/2),Math.round(r.y+r.height/2)]})")
  n0=nodes();ok(len(n0)>=3,'Edit Path open with %d nodes'%len(n0))
  def drag(i,dx,dy):
    q=nodes()[i];pg.mouse.move(q[0],q[1]);pg.mouse.down()
    for k in (.3,.6,1):pg.mouse.move(q[0]+dx*k,q[1]+dy*k)
    pg.mouse.up();pg.wait_for_timeout(250)
  a,c2=0,len(n0)-1
  drag(a,0,40);n1=nodes();ok(abs(n1[a][1]-n0[a][1]-40)<3,'node 1 dragged')
  drag(c2,30,-30);n2=nodes();ok(abs(n2[c2][0]-n1[c2][0]-30)<3,'node 2 dragged')
  js("document.getElementById('undoBtn').click()");pg.wait_for_timeout(300);u1=nodes()
  ok(js("!!document.getElementById('pathEditBar').classList.contains('open')"),'still in Edit Path after Undo')
  ok(abs(u1[c2][0]-n1[c2][0])<3 and abs(u1[a][1]-n1[a][1])<3,'Undo takes back ONLY the last node drag')
  js("document.getElementById('undoBtn').click()");pg.wait_for_timeout(300);u2=nodes()
  ok(abs(u2[a][1]-n0[a][1])<3,'second Undo takes back the first drag')
  js("document.getElementById('undoBtn').click()");pg.wait_for_timeout(300);ok(nodes()==u2 and js("document.getElementById('pathEditBar').classList.contains('open')"),'no further undo inside Edit Path (path is not wiped)')
  js("document.getElementById('redoBtn').click()");pg.wait_for_timeout(300);r1=nodes();ok(abs(r1[a][1]-n1[a][1])<3,'Redo brings the drag back')
  q=js("(()=>{const r=document.getElementById('pathEditDoneBtn').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()");pg.mouse.click(q[0],q[1]);pg.wait_for_timeout(500)
  ok(not js("document.getElementById('pathEditBar').classList.contains('open')"),'Done closes Edit Path')
  print(errs);b.close()
