import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  def curve(x0,y0,amp=60,L=360,n=24):
    pts=[(x0+L*i/n,y0+amp*math.sin(math.pi*i/n)) for i in range(n+1)]
    pg.mouse.move(*pts[0]);pg.mouse.down()
    for q in pts[1:]:pg.mouse.move(*q)
    pg.mouse.up();pg.wait_for_timeout(300)
  curve(cx-180,cy)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx,cy+60*0.95-60+0);pg.wait_for_timeout(300)
  # select the stroke by tapping its mid point
  pg.mouse.click(cx,cy+60);pg.wait_for_timeout(600)
  sid=js("window.__sketchpadGetState().selectedStrokeId");ok(sid,'stroke selected')
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(600)
  ok(js("document.getElementById('fp-width')&&document.getElementById('fp-width').classList.contains('show')"),'Width panel opens from the toolbar icon')
  ok(js("document.querySelectorAll('#widthOverlay .wp-h').length")==2,'two end handles shown')
  W=lambda:js("(()=>{const s=window.__sketchpadGetState().strokes.find(x=>x.id==='%s');return s&&s.wp?s.wp.map(q=>[q.id,+q.t.toFixed(3),+q.w.toFixed(3)]):null})()"%sid)
  # tap line to add a point
  box=pg.locator('#canvasWrap').bounding_box()
  pg.mouse.click(cx-60,cy+60*math.sin(math.pi*(120/360)));pg.wait_for_timeout(500)
  w=W();print(w);ok(w and len(w)==3,'tap adds a width point')
  sel=js("[...document.querySelectorAll('#widthOverlay .wp-h')].filter(h=>h.classList.contains('sel')).length");ok(sel==1,'new point is selected')
  def handle(i_id):
    return js("(()=>{const h=[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>h._id==='%s');const r=h.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()"%i_id)
  newid=[q for q in w if q[0] not in('ws','we')][0][0]
  el0=js("(()=>{const h=[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>h._id==='%s');window.__h0=h;return 1})()"%newid)
  x,y=handle(newid);w0=[q for q in w if q[0]==newid][0]
  pg.mouse.move(x,y);pg.mouse.down()
  for k in range(1,13):pg.mouse.move(x,y+k*4)   # outward (below)
  pg.mouse.up();pg.wait_for_timeout(400)
  w1=[q for q in W() if q[0]==newid][0];print('outward',w0,w1)
  ok(w1[2]>w0[2]+.8,'drag outward widens (full drag, not cut short)')
  ok(js("[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>h._id==='%s')===window.__h0"%newid),'handle element survives the drag')
  ok(js("[...document.querySelectorAll('#widthOverlay .wp-h')].find(h=>h._id==='%s').classList.contains('sel')"%newid),'point stays selected after release')
  # select again & drag inward
  x,y=handle(newid)
  pg.mouse.move(x,y);pg.mouse.down()
  for k in range(1,5):pg.mouse.move(x,y-k)
  pg.mouse.up();pg.wait_for_timeout(400)
  w2=[q for q in W() if q[0]==newid][0];print('inward',w2)
  ok(w2[2]<w1[2]-.5,'drag inward narrows (re-editable)')
  # move along the path
  x,y=handle(newid)
  pg.mouse.move(x,y);pg.mouse.down()
  f=lambda u:(cx-180+360*u,cy+60*math.sin(math.pi*u));u0=w2[1]
  th=lambda u:math.atan2(60*math.pi*math.cos(math.pi*u),360)
  o0=(x-f(u0)[0],y-f(u0)[1])
  # a real finger keeps its distance from the line while following it: rotate the offset with the line's direction
  for k in range(1,16):
    u=u0+.01*k;a=th(u)-th(u0);ox=o0[0]*math.cos(a)-o0[1]*math.sin(a);oy=o0[0]*math.sin(a)+o0[1]*math.cos(a)
    pg.mouse.move(f(u)[0]+ox,f(u)[1]+oy)
  pg.mouse.up();pg.wait_for_timeout(400)
  w3=[q for q in W() if q[0]==newid][0];print('along',w3)
  ok(w3[1]>w2[1]+.05,'drag along the line moves the point')
  ok(abs(w3[2]-w2[2])<.35,'moving along keeps the width')
  # add a second point and adjust both
  pg.mouse.click(cx+120,cy+60*math.sin(math.pi*(300/360)));pg.wait_for_timeout(500)
  ok(len(W())==4,'second point added')
  s0=js("window.__sketchpadGetState().histLen")
  # undo / redo
  js("document.getElementById('undoBtn')&&document.getElementById('undoBtn').click()");pg.wait_for_timeout(300)
  n_after_undo=len(W() or [])
  js("document.getElementById('redoBtn')&&document.getElementById('redoBtn').click()");pg.wait_for_timeout(300)
  print('undo->',n_after_undo,'redo->',len(W() or []));ok(n_after_undo==3 and len(W())==4,'undo / redo of a width point')
  clip={'x':cx-230,'y':cy-60,'width':460,'height':200}
  pg.screenshot(path=SD+'w2_edit.png',clip=clip)
  # presets
  js("document.querySelector('.wp-pre[data-k=both]').click()");pg.wait_for_timeout(300);ok(len(W())==3,'preset applied')
  js("document.querySelector('.wp-pre[data-k=even]').click()");pg.wait_for_timeout(300);ok(W() is None,'Uniform removes the profile')
  # save a profile, apply to another stroke at another size
  js("document.querySelector('.wp-pre[data-k=swell]').click()");pg.wait_for_timeout(300)
  js("(()=>{const i=document.getElementById('wpNameInput');i.value='Soft Swell'})()");js("document.getElementById('wpSaveBtn').click()");pg.wait_for_timeout(300)
  prof=js("JSON.parse(localStorage.getItem('sp-width-profiles-v1'))");print(prof)
  ok(len(prof)==1 and prof[0]['name']=='Soft Swell' and set(prof[0].keys())=={'id','name','v','interp','pts','ref'},'profile saved (name + shape only)')
  ok(js("document.querySelectorAll('#wpProfList canvas').length")==1,'profile thumbnail shown')
  # second, longer stroke with a bigger brush
  js("document.getElementById('modeDrawBtn')&&document.getElementById('modeDrawBtn').click()")
  print('done');
  # drawing must never be intercepted: Width panel left open, back to Draw mode, draw right over the selected line
  js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(400)
  n0=len(js("window.__sketchpadGetState().strokes"));pg.mouse.move(cx-100,cy+30);pg.mouse.down()
  for i in range(1,12):pg.mouse.move(cx-100+i*10,cy+30+math.sin(i/2)*20)
  pg.mouse.up();pg.wait_for_timeout(300)
  ok(len(js("window.__sketchpadGetState().strokes"))==n0+1,'drawing still works with the Width panel open in Draw mode (not intercepted)')
  print(errs);b.close()
