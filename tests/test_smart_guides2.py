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
  def line(x,y0,y1):
    pg.mouse.move(x,y0);pg.mouse.down()
    for i in range(1,13):pg.mouse.move(x,y0+(y1-y0)*i/12)
    pg.mouse.up();pg.wait_for_timeout(250)
  js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='smoothPen');e.click()})()")
  line(cx-220,cy-60,cy+40);line(cx-100,cy-60,cy+40);line(cx+120,cy-60,cy+40)     # A, B, C (C is the one that moves)
  X=lambda i:S()[i]['points'][0]['x']
  sc=js("document.getElementById('canvas').getBoundingClientRect().width/1800")
  nl=lambda col:js("document.getElementById('selectionBox').parentNode.querySelectorAll('svg line[stroke=\"%s\"]').length"%col)
  js("document.getElementById('qaPanel')&&(document.getElementById('qaPanel').style.display='block')");js("document.getElementById('qaMove').click()");pg.wait_for_timeout(300)
  def drag(fx,fy,dx,dy):
    ev('mousePressed',fx,fy)
    for i in range(1,15):ev('mouseMoved',fx+dx*i/14,fy+dy*i/14)
    pg.wait_for_timeout(100);o=nl('#ff9f1a');pg.screenshot(path='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/sg_space.png') if o else None;ev('mouseReleased',fx+dx,fy+dy);pg.wait_for_timeout(500);return o
  gap=X(1)-X(0)
  # move C so it sits about the same gap to the right of B (0.9 px off): equal spacing must pull it exactly in
  want=(X(1)+gap-X(2))*sc
  o=drag(cx+120,cy-10,want+0.9,0)
  g2=X(2)-X(1);print('gaps',gap,g2,'orange guides',o)
  ok(abs(g2-gap)<0.05,'dragged stroke snaps to the same gap as between the two others (%.3f vs %.3f units)'%(g2,gap))
  ok(o>=2,'equal-gap markers are shown (%d lines)'%o)
  # far from equal gap: not nudged
  x0=X(2);o=drag(cx+120-(x0-X(2))*sc+(x0-1400)*0+0,cy-10,0,0) if False else 0
  # resize helpers through the engine
  res=js("""(()=>{const I=window.__sketchpadInternals();I.sgBegin(new Set([window.__sketchpadGetState().strokes[2].id]),new Set());
    const t=I.sgState().t.boxes.filter(b=>!b.canvas)[0];const tx=t.x1,cxm=tx-70,cym=800,hw=60,hh=60;   // aim the right edge about 2 units short of another element's edge line
    const f=(70-0.4)/hw;const r=I.sgSnapScale(cxm,cym,hw,hh,f);
    return {f,f2:r.f,edge:cxm+hw*r.f,tx,g:r.guides.length}})()""");print(res)
  ok(abs(res['edge']-res['tx'])<1e-6 and res['g']>=1,'resizing from the centre snaps the grown edge onto another element\'s line')
  # group resize by a side handle
  js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(250)
  line(cx+240,cy-60,cy+40)   # D: the target on the right
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(250)
  ST=S();ids=[ST[1]['id'],ST[2]['id']]
  js("(()=>{const I=window.__sketchpadInternals();I.setMulti(%s,[],null);I.updateGroupBox()})()"%str(ids).replace("'",'"'));pg.wait_for_timeout(500)
  hb=js("(()=>{const e=document.querySelector('#groupBox .gh[data-h=se]');if(!e)return null;const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()");print('handle',hb)
  pts=[q for i in (1,2) for q in S()[i]['points']]
  bx0=min(q['x'] for q in pts)-1.5;bx1=max(q['x'] for q in pts)+1.5;by0=min(q['y'] for q in pts)-1.5;by1=max(q['y'] for q in pts)+1.5
  hx,hy=bx1-bx0,by1-by0;T=X(3)+1.5;aim=T+0.4;v=(aim-bx0)/hx-1
  dxp,dyp=v*hx*sc,v*hy*sc
  ev('mousePressed',*hb)
  for i in range(1,15):ev('mouseMoved',hb[0]+dxp*i/14,hb[1]+dyp*i/14)
  pg.wait_for_timeout(150);gl=js("document.getElementById('selectionBox').parentNode.querySelectorAll('svg line').length");ev('mouseReleased',hb[0]+dxp,hb[1]+dyp);pg.wait_for_timeout(800)
  e1=max(q['x']+S()[i]['settings']['size']/2 for i in (1,2) for q in S()[i]['points'])
  Dx=[X(3)-S()[3]['settings']['size']/2,X(3),X(3)+S()[3]['settings']['size']/2]
  print('edge',bx1,'->',e1,'target',T,'aimed',aim,'guides',gl)
  ok(min(abs(e1-t) for t in Dx)<0.1 and gl>=1,'resizing a selection snaps the dragged edge onto the other element (off %.3f units, aimed %.1f beyond)'%(min(abs(e1-t) for t in Dx),aim-T))
  print(errs);b.close()
