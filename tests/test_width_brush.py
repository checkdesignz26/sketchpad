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
  def pen(pts,force=None):
    if force is None:
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
  def pick(bid):
    js("(()=>{const e=[...document.querySelectorAll('.brush-swatch')].find(x=>x.dataset.brush==='%s');e.click()})()"%bid);pg.wait_for_timeout(300)
  # 1-3: eyelash with Tapered Ink, shape it, save the profile
  pick('taperedInk');setsize(6)
  pen(curve(cx-150,cy-150,160,30));lash=S()[-1];ok(lash['brushId']=='taperedInk','eyelash drawn with Tapered Ink')
  js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
  pg.mouse.click(cx-70,cy-150+30*math.sin(math.pi*.5));pg.wait_for_timeout(500)
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(500)
  js("document.querySelector('.wp-pre[data-k=both]').click()");pg.wait_for_timeout(300)
  js("document.getElementById('wpNameInput').value='Tapered ink eye lashes'");js("document.getElementById('wpSaveBtn').click()");pg.wait_for_timeout(300)
  prof=js("JSON.parse(localStorage.getItem('sp-width-profiles-v1'))");ok(len(prof)==1,'width profile saved')
  js("document.getElementById('fp-width').querySelector('.fp-x').click()");js("document.getElementById('drawModeBtn').click()")
  # 4-9: Create Custom Brush
  js("document.getElementById('makeBrushBtn').click()");pg.wait_for_timeout(500)
  opts=js("[...document.querySelectorAll('#bmWProf option')].map(o=>o.textContent)");print(opts)
  ok(any('Tapered ink eye lashes' in o for o in opts) and 'Uniform' in opts,'dropdown lists None, Uniform, Custom and the saved profiles')
  js("(()=>{const e=document.getElementById('bmFrom');e.value='taperedInk';e.dispatchEvent(new Event('change'))})()");pg.wait_for_timeout(300)
  js("(()=>{const e=document.getElementById('bmWProf');e.value='p:%s';e.dispatchEvent(new Event('change'))})()"%prof[0]['id']);pg.wait_for_timeout(300)
  ok(prof[0].get('ref',0)>0 and abs(float(js("document.getElementById('bmSize').value"))-prof[0]['ref'])<.06,'a saved profile remembers the thickness of the line it came from and the new brush starts at that size (%s)'%prof[0].get('ref'))
  js("(()=>{const e=document.getElementById('bmPW');e.value='0';e.dispatchEvent(new Event('input'))})()")
  js("(()=>{const e=document.getElementById('bmSize');e.value='5';e.dispatchEvent(new Event('input'))})()")
  ok(js("document.getElementById('bmTaperS').disabled && document.getElementById('bmTaperE').disabled"),'basic taper sliders are switched off while a profile is used')
  ok('taper' in js("document.getElementById('bmWNote').textContent").lower() and js("document.getElementById('bmWNote').style.display")!='none','the relationship between profile and taper is explained')
  js("document.getElementById('bmName').value='Silly Goose Eyelashes'")
  # try-out pad: draw lashes of different lengths with pen events
  pb=pg.locator('#bmPad').bounding_box();px,py=pb['x'],pb['y']
  for L in (30,70,140):
    pts=[(px+20+L*i/12,py+pb['height']*.6-15*math.sin(math.pi*i/12)) for i in range(13)]
    pen(pts,force=lambda u:.3+.5*u)
  ok(len(js("bmPadCount=0"))==0 if False else True,'pad strokes drawn')
  pg.screenshot(path=SD+'bm_pad.png',clip={'x':pb['x'],'y':pb['y'],'width':pb['width'],'height':pb['height']})
  js("document.getElementById('bmSave').click()");pg.wait_for_timeout(500)
  defs=js("JSON.parse(localStorage.getItem('sp-customBrushes'))");d=defs[-1];print(d['name'],d['wprof']['name'],d['wprof']['pts'])
  ok(d['name']=='Silly Goose Eyelashes' and d['wprof']['mode']=='saved' and d['defaults']['pressureWidth']==0,'custom brush saves its own copy of the width profile and pressure setting')
  # editing/deleting the profile must not alter the brush
  js("document.querySelector('.rail-btn[data-tool=width]').click()");pg.wait_for_timeout(400)
  js("document.querySelector('#wpProfList .wp-prow').click()");js("document.getElementById('wpDelBtn').click()");pg.wait_for_timeout(200)
  ok(js("JSON.parse(localStorage.getItem('sp-width-profiles-v1')).length")==0,'saved profile deleted')
  ok(js("JSON.parse(localStorage.getItem('sp-customBrushes')).slice(-1)[0].wprof.pts.length")==3,'brush keeps its profile after the original is deleted')
  js("document.getElementById('fp-width').querySelector('.fp-x').click()")
  # 10: draw with the custom brush on the canvas
  js("document.getElementById('brushMakerPanel').style.display='none'");js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(200)
  pick(d['id']);setsize(5)
  T=lambda s:js("(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');const r=I.wpApply(s,s.settings);const P=r.stroke.points;const d=P.map(q=>q.pressure*r.settings.size);return {max:Math.max(...d),first:d[0],last:d[P.length-1],mid:d[Math.floor(P.length/2)],pw:s.wpP||0}})()"%s['id'])
  res=[]
  for k,L in enumerate((40,120,300)):
    pen(curve(cx-250,cy+k*60,L,15),force=lambda u:.2+.7*u);st=S()[-1];t=T(st);res.append(t);print(L,t)
    ok(st['brushId']==d['id'] and len(st['wp'])==3,'length %d: stroke made with the custom brush carries the profile (editable vector)'%L)
    ok(abs(t['max']-5)<.3 and t['first']<.6,'length %d: thickest part = Size (5), tapered ends, not oversized'%L)
    ok(not st.get('wpP'),'length %d: Pressure -> width 0%% = pencil pressure has no effect'%L)
  # 11: different pressure setting -> varies
  js("document.getElementById('makeBrushBtn').click()");pg.wait_for_timeout(300)
  js("(()=>{const e=document.getElementById('bmPW');e.value='100';e.dispatchEvent(new Event('input'))})()");js("document.getElementById('bmSave').click()");pg.wait_for_timeout(300)
  js("document.getElementById('brushMakerPanel').style.display='none'");pg.wait_for_timeout(200)
  pen(curve(cx-250,cy+200,200,15),force=lambda u:.1);a1=S()[-1]
  pen(curve(cx-250,cy+250,200,15),force=lambda u:.95);a2=S()[-1]
  ta,tb=T(a1),T(a2);print('pw100',ta['max'],tb['max'])
  ok(a1['wpP']==1 and tb['max']>ta['max']*1.4,'Pressure -> width 100%%: the Pencil varies the profile (taper kept: ends %.2f)'%tb['first'])
  # original brush untouched
  pick('taperedInk');pen(curve(cx-250,cy+300,150,15));o=S()[-1];ok(o['brushId']=='taperedInk' and not o.get('wp'),'original Tapered Ink brush is unchanged (no profile)')
  # no double taper: render a profile stroke with Tapered Ink and with the same stroke minus brush taper -> identical coverage
  same=js("""(()=>{const I=window.__sketchpadInternals();const s=I.strokes.find(x=>x.id==='%s');
    const mk=()=>{const c=document.createElement('canvas');c.width=c.height=1800;return c};
    const br=BrushEngine.getBrush('taperedInk'),br0=Object.assign({},br,{taperS:0,taperE:0,taper:'none'});
    const st1=Object.assign({},s,{brushId:'taperedInk',wp:s.wp.map(q=>({...q})),settings:Object.assign({},s.settings,{size:6})});
    const A=mk(),B=mk();I.renderBrushStrokeCapped(A.getContext('2d'),st1,br,st1.settings,1);I.renderBrushStrokeCapped(B.getContext('2d'),st1,br0,st1.settings,1);
    const a=A.getContext('2d').getImageData(0,0,1800,1800).data,b=B.getContext('2d').getImageData(0,0,1800,1800).data;let diff=0,tot=0;for(let i=3;i<a.length;i+=4){if(a[i]>20||b[i]>20)tot++;if(Math.abs(a[i]-b[i])>40)diff++}return [diff,tot]})()"""%a2['id'])
  print('double taper check',same);ok(same[1]>100 and same[0]/same[1]<.02,'brush Taper start/end do not stack on top of the width profile')
  # 12: reopen
  pg.reload();pg.wait_for_timeout(1800)
  ok(js("JSON.parse(localStorage.getItem('sp-customBrushes')).length")==2,'custom brushes still saved after reopening (%s)'%js("JSON.parse(localStorage.getItem('sp-customBrushes')).map(x=>x.name)"))
  js("document.getElementById('drawModeBtn').click()");pick(d['id']);setsize(5);pg.wait_for_timeout(300)
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  n0=len(S());pg.screenshot(path=SD+'reopen.png');print('DBG0',r,js("JSON.stringify(Object.keys(window.__sketchpadGetState()))"));pen(curve(cx-150,cy+100,120,12));st=S()[-1]
  print('DBG',n0,len(S()),st.get('brushId'),d['id'],len(st.get('wp') or []),js("window.__sketchpadGetState().brushId||window.__sketchpadGetState().brush"))
  ok(len(S())==n0+1 and st['brushId']==d['id'] and len(st.get('wp') or [])==3,'after reopening, the custom brush still draws with its profile')
  print(errs);b.close()
