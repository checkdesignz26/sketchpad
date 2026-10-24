import sys,math,json;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  line="[{x:0,y:0},{x:150,y:0},{x:300,y:0}]"
  def pieces(d,unit=10,pts=line,closed='false'):
    return js("(()=>{const I=window.__sketchpadInternals();return I.dashPieces(%s,%s,%s,%s).map(p=>[+p[0].x.toFixed(2),+p[p.length-1].x.toFixed(2)])})()"%(pts,json.dumps(d),unit,closed))
  a=pieces({'seq':[3,2]});print(a)
  ok(len(a)==6 and a[0]==[0,30] and a[1]==[50,80] and a[5][0]==250,'dash 3 / gap 2 at width 10 gives 30px dashes every 50px')
  a=pieces({'seq':[3,2],'off':1});ok(a[0]==[10,40],'offset shifts the pattern forward along the path')
  a=pieces({'seq':[3,2],'off':-1});print(a[0]);ok(a[0][0]==0 and a[0][1]==20,'negative offset shifts it back')
  a=pieces({'seq':[3,2],'cap':'square'});print(a[:2]);ok(a[1]==[45,85],'square ends extend each dash by half a line width')
  a=pieces({'seq':[3,2,1]});print(a[:4]);ok(a[0]==[0,30] and a[1]==[50,60] and a[2][0]==90 and a[3]==[120,150],'odd sequences repeat (3,2,1 = 3,2,1,3,2,1)')
  a=pieces({'seq':[10,5,20,5]},unit=1);print(a[:3]);ok(a[0]==[0,10] and a[1]==[15,35] and a[2][0]==40,'custom long-short sequence')
  a=pieces({'seq':[0,2]});ok(len(a)==15 and abs(a[0][1]-a[0][0])<1,'zero-length dashes become dots')
  sq="[{x:0,y:0},{x:100,y:0},{x:100,y:100},{x:0,y:100}]"
  a=pieces({'seq':[3,2]},pts=sq,closed='true');ok(len(a)>=8,'closed paths dash all the way round (%d)'%len(a))
  ok(len(pieces({'seq':[0.01,0.01]},unit=0.1))<=4000,'huge piece counts are capped')
  # ---- UI on a real stroke ----
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  pts=[(cx-180+360*i/24,cy+50*math.sin(math.pi*i/24)) for i in range(25)]
  pg.mouse.move(*pts[0]);pg.mouse.down()
  for q in pts[1:]:pg.mouse.move(*q)
  pg.mouse.up();pg.wait_for_timeout(300)
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx,cy+50);pg.wait_for_timeout(500)
  sid=js("window.__sketchpadGetState().selectedStrokeId");ok(sid,'stroke selected')
  js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');s.settings=Object.assign({},s.settings,{size:14});s.color='#7b3fa0';})()"%sid)
  bar='#strokeActionsBar '
  D=lambda:js("(()=>{const s=window.__sketchpadGetState().strokes.find(x=>x.id==='%s');return s.dash?JSON.stringify(s.dash):null})()"%sid)
  def setsel(v):js("(()=>{const e=document.querySelector('%s.dash-sel');e.value='%s';e.dispatchEvent(new Event('change'))})()"%(bar,v));pg.wait_for_timeout(500)
  setsel('dashdot');d=json.loads(D());print(d);ok(d['seq']==[4,1.5,.02,1.5],'Dash-dot preset applies a 4-value sequence')
  clip={'x':cx-230,'y':cy-40,'width':460,'height':150}
  pg.screenshot(path=SD+'da1.png',clip=clip)
  # edit a value, add a pair, offset, cap
  js("(()=>{const i=document.querySelector('%s.dash-rows input[type=number][data-i=\"0\"]');i.value='6';i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))})()"%bar);pg.wait_for_timeout(400)
  d=json.loads(D());ok(d['seq'][0]==6 and d['k']=='custom','editing a dash length updates the line and marks it Custom')
  js("document.querySelector('%s.dash-add').click()"%bar);pg.wait_for_timeout(300)
  ok(len(json.loads(D())['seq'])==6,'add a dash/gap pair')
  js("document.querySelector('%s.dash-cap[data-v=square]').click()"%bar);pg.wait_for_timeout(300)
  ok(json.loads(D())['cap']=='square','dash ends: square')
  js("(()=>{const i=document.querySelector('%s.dash-off-n');i.value='2.5';i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))})()"%bar);pg.wait_for_timeout(400)
  ok(json.loads(D())['off']==2.5,'offset updates')
  pg.screenshot(path=SD+'da2.png',clip=clip)
  # undo/redo of dash changes
  js("document.getElementById('undoBtn').click()");pg.wait_for_timeout(300)
  d1=D();js("document.getElementById('redoBtn').click()");pg.wait_for_timeout(300);d2=D()
  print(d1);print(d2);ok(json.loads(d1)['off']==0 and json.loads(d2)['off']==2.5,'undo / redo restore dash settings')
  # remove a pair
  js("document.querySelector('%s.dash-pdelrow').click()"%bar);pg.wait_for_timeout(300);ok(len(json.loads(D())['seq'])==4,'remove a dash/gap pair')
  # presets
  js("document.querySelector('%s.dash-name').value='Long Short'"%bar);js("document.querySelector('%s.dash-psave').click()"%bar);pg.wait_for_timeout(300)
  pr=js("JSON.parse(localStorage.getItem('sp-dash-presets-v1'))");print(pr);ok(len(pr)==1 and pr[0]['name']=='Long Short','dash preset saved')
  setsel('');ok(D() is None,'Solid removes the dash')
  setsel('u:'+pr[0]['id']);ok(json.loads(D())['seq']==pr[0]['seq'],'saved preset can be applied')
  # with width profile
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  js("document.querySelector('.wp-pre[data-k=swell]').click()");pg.wait_for_timeout(500)
  pg.screenshot(path=SD+'da3.png',clip=clip)
  # duplicate keeps dash
  st=js("(()=>{const s=window.__sketchpadGetState().strokes.find(x=>x.id==='%s');return JSON.parse(JSON.stringify(s)).dash})()"%sid);ok(st is not None,'dash is stored on the stroke (saves, duplicates)')
  # svg export outline has several pieces
  n=js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');const o=I.svgStrokeOutline(s,s.settings,BrushEngine.getBrush(s.brushId));return o?(o.d.match(/M/g)||[]).length:0})()"%sid);print('svg subpaths',n);ok(n>6,'SVG export contains every dash')
  pg.reload();pg.wait_for_timeout(1500)
  ok(js("JSON.parse(localStorage.getItem('sp-dash-presets-v1')).length")==1,'dash presets persist after restart')
  print(errs);b.close()
