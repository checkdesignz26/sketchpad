import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
import os
SHOT=os.environ.get('SHOT')
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  cdp=pg.context.new_cdp_session(pg)
  ev=lambda t,x,y:cdp.send('Input.dispatchMouseEvent',{'type':t,'x':x,'y':y,'button':'left','buttons':1 if t!='mouseReleased' else 0,'clickCount':1,'pointerType':'pen','force':.5})
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  S=lambda:js("window.__sketchpadGetState().strokes")
  def line(x0,y0,x1,y1):
    pg.mouse.move(x0,y0);pg.mouse.down()
    for i in range(1,13):pg.mouse.move(x0+(x1-x0)*i/12,y0+(y1-y0)*i/12)
    pg.mouse.up();pg.wait_for_timeout(250)
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  line(cx-100,cy-120,cx-100,cy-20)
  line(cx+60,cy+40,cx+60,cy+140)
  bb=lambda s:(min(p['x'] for p in s['points']),max(p['x'] for p in s['points']),min(p['y'] for p in s['points']),max(p['y'] for p in s['points']))
  a=bb(S()[0]);print('A',a,'B',bb(S()[1]))
  sc=js("document.getElementById('canvas').getBoundingClientRect().width/1800")
  js("document.getElementById('qaPanel')&&(document.getElementById('qaPanel').style.display='block')");js("document.getElementById('qaMove').click()");pg.wait_for_timeout(300)
  nlines=lambda:js("document.getElementById('selectionBox').parentNode.querySelectorAll('svg line').length")
  def drag(fx,fy,dx,dy,release=True):
    ev('mousePressed',fx,fy)
    for i in range(1,15):ev('mouseMoved',fx+dx*i/14,fy+dy*i/14)
    pg.wait_for_timeout(100);g=nlines()
    global SHOT
    if SHOT and g>0:pg.screenshot(path=SHOT);SHOT=None
    if release:ev('mouseReleased',fx+dx,fy+dy);pg.wait_for_timeout(500)
    return g
  # 1: drag B to ~3px (screen) beside A's x: must snap exactly onto A and show a guide while dragging
  b0=bb(S()[1]);dxs=(a[0]-b0[0])*sc+0.3
  g=drag(cx+60,cy+90,dxs,-60);b1=bb(S()[1]);print('B after',b1,'guides',g)
  ok(abs(b1[0]-a[0])<0.05,'dragged stroke snaps exactly onto the other stroke\'s edge (off by %.3f units)'%abs(b1[0]-a[0]))
  ok(g>=1,'a guide line is shown while dragging (%d)'%g)
  ok(nlines()==0,'guide lines disappear when you let go')
  # 2: far from anything -> follows the pen exactly
  fx=cx+60+dxs;fy=cy+90-60
  g=drag(fx,fy,150,40);b2=bb(S()[1]);mv=b2[0]-b1[0]
  ok(abs(mv-150/sc)<0.6 and g==0,'a drag far from other elements is not nudged (moved %.2f vs %.2f, %d guides)'%(mv,150/sc,g))
  # 3: engine: canvas centre
  I=js("(()=>{const I=window.__sketchpadInternals();I.sgBegin(new Set(),new Set());const t=I.sgState().t.boxes[0];const cxm=(t.x0+t.x1)/2;const r=I.sgSnap({x0:cxm-20+2,x1:cxm+20+2,y0:t.y0+100,y1:t.y0+160});return [r.dx,r.guides.length]})()")
  ok(abs(I[0]+2)<1e-6 and I[1]>=1,'snaps to the canvas centre line')
  # 4: off switch
  js("document.getElementById('viewSmartBtn').click()");ok(js("localStorage.getItem('sp-smartGuides')")=='0','Smart guides can be switched off (choice remembered)')
  b3=bb(S()[1]);fx=cx+60+dxs+150;fy=cy+90-60+40
  g=drag(fx,fy,(a[0]-b3[0])*sc+0.3,0);b4=bb(S()[1])
  ok(g==0 and abs(b4[0]-a[0])>0.2,'switched off: no guides, no snapping (gap %.2f units)'%abs(b4[0]-a[0]))
  # 5: dragging a selection (group move)
  js("document.getElementById('viewSmartBtn').click()");print('sgOn',js('window.__sketchpadInternals().sgState().on'))
  pg.on('console',lambda m:print('CONSOLE',m.text[:200]))
  js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(300)
  line(cx+200,cy-100,cx+200,cy-20)                          # C, a third stroke
  ST=S();ids=[ST[1]['id'],ST[2]['id']]
  js("(()=>{const I=window.__sketchpadInternals();I.setMulti(%s,[],null);})()"%str(ids).replace("'",'"'));
  js("document.getElementById('drawModeBtn').click()");js("document.getElementById('editModeBtn').click()")
  js("(()=>{const I=window.__sketchpadInternals();I.setMulti(%s,[],null);I.updateGroupBox()})()"%str(ids).replace("'",'"'));pg.wait_for_timeout(500)
  gb=js("(()=>{const e=document.getElementById('groupBox');if(!e||e.style.display==='none')return null;const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()");print('groupBox',gb)
  if gb:
    def gdrag(dx,dy):
      gb=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
      gx,gy=gb[0]+gb[2]/2,gb[1]+gb[3]/2
      ev('mousePressed',gx,gy)
      for i in range(1,15):ev('mouseMoved',gx+dx*i/14,gy+dy*i/14)
      pg.wait_for_timeout(150);g=nlines();ev('mouseReleased',gx+dx,gy+dy);pg.wait_for_timeout(600);return g
    ST=S();bA=bb(ST[0]);bB0=bb(ST[1])
    gdrag(110,25)                                   # move the selection well away first
    ST=S();bB=bb(ST[1]);bC=bb(ST[2])
    ok(abs((bB[0]-bB0[0])*sc-110)<8,'a selection can still be dragged normally (%.1f px)'%((bB[0]-bB0[0])*sc))
    dxg=(bA[0]-bB[0])*sc+0.3                         # ...then back to 0.3 px beside the other stroke
    gg=gdrag(dxg,10)
    ST=S();nB=bb(ST[1]);nC=bb(ST[2])
    ok(abs(nB[0]-bA[0])<0.05,'a dragged selection snaps too: its edge lands on the other element (off %.3f)'%abs(nB[0]-bA[0]))
    ok(abs((nC[0]-bC[0])-(nB[0]-bB[0]))<0.01,'every part of the selection moved by the same amount')
    ok(gg>=1 and nlines()==0,'guides shown during the drag and cleared after (%d)'%gg)
  print(errs);b.close()
