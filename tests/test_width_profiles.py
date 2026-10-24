import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  def curve(x0,y0,amp,L,n=24):
    pts=[(x0+L*i/n,y0+amp*math.sin(math.pi*i/n)) for i in range(n+1)]
    pg.mouse.move(*pts[0]);pg.mouse.down()
    for q in pts[1:]:pg.mouse.move(*q)
    pg.mouse.up();pg.wait_for_timeout(300)
  S=lambda:js("window.__sketchpadGetState().strokes")
  curve(cx-200,cy-150,50,160)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx-120,cy-150+50);pg.wait_for_timeout(500)
  A=js("window.__sketchpadGetState().selectedStrokeId");ok(A,'stroke A selected')
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  js("document.querySelector('.wp-pre[data-k=swell]').click()");pg.wait_for_timeout(300)
  js("document.getElementById('wpNameInput').value='Soft Swell'");js("document.getElementById('wpSaveBtn').click()");pg.wait_for_timeout(300)
  prof=js("JSON.parse(localStorage.getItem('sp-width-profiles-v1'))")
  ok(len(prof)==1 and set(prof[0].keys())=={'id','name','v','interp','pts','ref'},'profile holds only name/shape/schema (no path, colour or thickness)')
  # stroke B: long, bigger brush, other colour
  js("document.getElementById('drawModeBtn')&&document.getElementById('drawModeBtn').click()")
  js("document.getElementById('editModeBtn').click()")
  js("document.getElementById('fp-width').querySelector('.fp-x').click()")
  # draw B in draw mode
  js("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/^\\s*✏️?\\s*Draw/.test(x.textContent||''));if(b)b.click()})()")
  pg.wait_for_timeout(200)
  curve(cx-250,cy+20,-40,500,n=40)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  n=len(S());ok(n>=2,'second stroke drawn (%d strokes)'%n)
  B=S()[-1]['id']
  js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');s.settings=Object.assign({},s.settings,{size:20});s.color='#2a9d8f';I.rebuildAllLayers();})()"%B)
  pg.mouse.click(cx,cy+20-40);pg.wait_for_timeout(500)
  sel=js("window.__sketchpadGetState().selectedStrokeId");print('sel',sel==B)
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  before=[js("(()=>{const s=window.__sketchpadGetState().strokes.find(x=>x.id==='%s');return [s.points.length,s.color,s.settings.size,s.wp?1:0]})()"%B)]
  js("document.querySelector('#wpProfList .wp-prow').click()");pg.wait_for_timeout(200)
  js("document.getElementById('wpApplyBtn').click()");pg.wait_for_timeout(400)
  after=js("(()=>{const s=window.__sketchpadGetState().strokes.find(x=>x.id==='%s');return [s.points.length,s.color,s.settings.size,s.wp.map(q=>[q.t,q.w])]})()"%B)
  print(before,after)
  ok(after[0]==before[0][0] and after[1]=='#2a9d8f' and after[2]==20,'applying keeps geometry, colour and thickness')
  ok(after[3]==[[0,.22],[.5,1],[1,.22]],'profile applied proportionally')
  pg.screenshot(path=SD+'w2_applied.png',clip={'x':cx-270,'y':cy-100,'width':540,'height':160})
  # editing the stroke must not change the saved profile
  js("document.querySelector('.wp-pre[data-k=pinch]').click()");pg.wait_for_timeout(300)
  ok(js("JSON.parse(localStorage.getItem('sp-width-profiles-v1'))[0].pts[1].w")==1,'editing a line does not change the saved profile')
  # use for new strokes
  js("document.getElementById('wpUseBtn').click()");pg.wait_for_timeout(200)
  ok(js("document.getElementById('wpNewChk').checked"),'new-stroke option on')
  js("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/^\\s*✏️?\\s*Draw/.test(x.textContent||''));if(b)b.click()})()");pg.wait_for_timeout(200)
  curve(cx-100,cy+120,30,200)
  C=S()[-1];ok(C.get('wp') and len(C['wp'])==3,'new stroke receives the profile')
  js("document.getElementById('wpUniformBtn').click()");pg.wait_for_timeout(200)
  curve(cx-100,cy+170,30,200)
  D=S()[-1];ok(not D.get('wp'),'back to uniform for new strokes')
  # persistence
  pg.reload();pg.wait_for_timeout(1500)
  ok(js("JSON.parse(localStorage.getItem('sp-width-profiles-v1')).length")==1,'saved profile persists after reload')
  # closed stroke is handled explicitly
  print(errs);b.close()
