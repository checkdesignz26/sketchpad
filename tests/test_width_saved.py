import sys,math,json;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  cdp=pg.context.new_cdp_session(pg)
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  S=lambda:js("window.__sketchpadGetState().strokes")
  def pen(pts,force=None,ptype='mouse'):
    # pen events via CDP so e.pressure / pointerType are real; force=None -> plain mouse
    if ptype=='mouse':
      pg.mouse.move(*pts[0]);pg.mouse.down()
      for q in pts[1:]:pg.mouse.move(*q)
      pg.mouse.up();pg.wait_for_timeout(300);return
    def ev(t,x,y,f):cdp.send('Input.dispatchMouseEvent',{'type':t,'x':x,'y':y,'button':'left','buttons':1 if t!='mouseReleased' else 0,'clickCount':1,'pointerType':'pen','force':f})
    ev('mousePressed',*pts[0],force(0))
    for i,q in enumerate(pts[1:],1):ev('mouseMoved',*q,force(i/len(pts)))
    ev('mouseReleased',*pts[-1],force(1));pg.wait_for_timeout(300)
  def curve(x0,y0,L,amp,n=30):return [(x0+L*i/n,y0+amp*math.sin(math.pi*i/n)) for i in range(n+1)]
  def setsize(v):
    js("(()=>{const e=document.getElementById('tbSizeNum');e.value='%s';e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))})()"%v);pg.wait_for_timeout(200)
  # a legacy-style saved profile (older version stored un-normalised multipliers; peak 3)
  js("localStorage.setItem('sp-width-profiles-v1',JSON.stringify([{id:'old1',name:'Tapered ink eye lashes',v:1,interp:'smooth',pts:[{t:0,w:.1},{t:.45,w:3},{t:1,w:.1}]}]))")
  pg.reload();pg.wait_for_timeout(2000)
  print('after reload canvas present',js("!!document.getElementById('canvas')"))
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  js("document.querySelector('#wpProfList .wp-prow').click()");js("document.getElementById('wpUseBtn').click()");pg.wait_for_timeout(200)
  ok(js("document.getElementById('wpNewChk').checked"),'saved profile enabled for new lines')
  js("document.getElementById('fp-width').querySelector('.fp-x').click()");js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(300)
  def thick(st):
    res=js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');const r=I.wpApply(s,s.settings);const P=r.stroke.points;const n=P.length;const d=P.map(q=>q.pressure*r.settings.size);return {n,mid:d[Math.floor(n*.45)],max:Math.max(...d),first:d[0],last:d[n-1],size:s.settings.size,pw:r.settings.pressureWidth}})()"%st['id'])
    return res
  res={}
  for k,sz in enumerate([2,4,8]):
    setsize(sz);pen(curve(cx-250,cy-200+k*70,200,25));st=S()[-1];t=thick(st);res[sz]=t;print(sz,t)
    ok(st.get('wp') and abs(max(q['w'] for q in st['wp'])-1)<1e-6,'width %s: legacy profile applied normalised (peak 1x)'%sz)
    ok(abs(t['max']-sz)<sz*.06,'width %s: thickest point equals the brush width (%.2f)'%(sz,t['max']))
    ok(t['first']<sz*.2 and t['last']<sz*.2,'width %s: both ends tapered'%sz)
  ok(abs(res[8]['mid']/res[2]['mid']-4)<.2,'same profile at widths 2/4/8 scales proportionally')
  # short straight stroke
  setsize(4);pen([(cx+60,cy-200),(cx+75,cy-198),(cx+90,cy-196)]);st=S()[-1];t=thick(st);print('short',t)
  ok(abs(t['max']-4)<.3 and t['first']<1,'short straight stroke keeps correct proportions')
  # profile-only: pressure does not matter; with pen force varying
  setsize(4)
  pen(curve(cx-250,cy+50,200,25),ptype='pen',force=lambda u:.15);a=S()[-1]
  pen(curve(cx-250,cy+100,200,25),ptype='pen',force=lambda u:.95);bb=S()[-1]
  pen(curve(cx-250,cy+150,200,25),ptype='pen',force=lambda u:.2+.7*u);c=S()[-1]
  pa,pb,pc=thick(a),thick(bb),thick(c)
  print('profile-only light/heavy/ramp',pa['max'],pb['max'],pc['max'])
  ok(abs(pa['max']-pb['max'])<.05 and abs(pa['max']-pc['max'])<.05 and abs(pa['max']-4)<.3,'Profile only: Pencil pressure does not change the thickness')
  ok(not a.get('wpP'),'Profile only is the default')
  # Profile + Pressure
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(400)
  js("(()=>{const e=document.getElementById('wpPressSel');e.value='both';e.dispatchEvent(new Event('change'))})()");js("document.getElementById('fp-width').querySelector('.fp-x').click()");js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(300)
  setsize(4)
  pen(curve(cx-250,cy+200,200,25),ptype='pen',force=lambda u:.1);d1=S()[-1]
  pen(curve(cx-250,cy+250,200,25),ptype='pen',force=lambda u:.95);d2=S()[-1]
  pen(curve(cx-250,cy+300,200,25));d3=S()[-1]   # mouse: pressure 0.5 = same as profile only
  t1,t2,t3=thick(d1),thick(d2),thick(d3);print('profile+pressure light/heavy/mouse',t1['max'],t2['max'],t3['max'])
  ok(d1.get('wpP') and t2['max']>t1['max']*1.4,'Profile + Pressure: pressure varies the thickness (controlled)')
  ok(t2['max']<=4*1.5 and t1['max']>=4*.4,'variation stays within about +/-45%%')
  ok(abs(t3['max']-4)<.3,'finger / mouse (pressure 0.5) behaves exactly like Profile only')
  # apply to an existing stroke keeps geometry; edit does not change saved profile
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  sid=a['id'];before=json.dumps([(q['x'],q['y']) for q in a['points']])
  js("(()=>{const I=window.__sketchpadInternals();I.setMulti&&0})()")
  prof0=js("localStorage.getItem('sp-width-profiles-v1')")
  js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');s.wp[1].w=.5;})()"%sid)
  ok(js("localStorage.getItem('sp-width-profiles-v1')")==prof0,'editing a stroke does not modify the saved profile')
  after=json.dumps([(q['x'],q['y']) for q in [s for s in S() if s['id']==sid][0]['points']]);ok(before==after,'path geometry untouched')
  # high zoom: thickness is in canvas units, not screen pixels
  for _ in range(7):js("document.getElementById('zoomInBtn')&&document.getElementById('zoomInBtn').click()")
  pg.wait_for_timeout(500);js("document.getElementById('drawModeBtn').click()");setsize(4)
  pen(curve(cx-40,cy-10,60,8,n=20));z=S()[-1];tz=thick(z);print('zoomed',tz,js("document.getElementById('zoomPill').textContent"))
  ok(abs(tz['max']-4)<.3 and z['settings']['size']==4,'at very high zoom the thickness is still 4 canvas units (not screen pixels)')
  # persistence
  pg.reload();pg.wait_for_timeout(1500)
  pr=js("JSON.parse(localStorage.getItem('sp-width-profiles-v1'))");ok(len(pr)==1 and pr[0]['name']=='Tapered ink eye lashes','saved profile survives restart (older profile untouched: peak %s)'%max(q['w'] for q in pr[0]['pts']))
  print(errs);b.close()
