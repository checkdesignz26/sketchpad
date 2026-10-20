# Pattern Templates v2: edge-crossing presets, per-type colours, arrows inside placeholders, wrapping exactness. Server on :8790.
import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m,x=''):print(('PASS ' if c else 'FAIL ')+m,x);return c
T="window.__sketchpadTemplates"
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate;res=[]
  ids=js(T+".presets.map(p=>p.id)")
  col={'circle':'#ec5fa0','oval':'#1fa59a','square':'#ee7b30','rect':'#7a5cd6','triangle':'#4aa551'}
  for pid in ids:
    js("id=>window.__sketchpadTemplates.loadById(id)",pid);pg.wait_for_timeout(200)
    g=js("window.__sketchpadGetState().strokes.filter(s=>s.tpl===1).map(s=>({k:s.tplKind,c:s.color,fill:!!s.fillColor,x0:s.shape&&Math.min(s.shape.x0,s.shape.x1),x1:s.shape&&Math.max(s.shape.x0,s.shape.x1),y0:s.shape&&Math.min(s.shape.y0,s.shape.y1),y1:s.shape&&Math.max(s.shape.y0,s.shape.y1),ar:!!(s.tplArrow&&s.tplArrow.on)}))")
    dims=js("({CX:window.__sketchpadGetState().tileX!=null?window.__sketchpadGetState().tileX:0})")
    if not g: continue
    res.append(ok(all(col[s['k']]==s['c'] for s in g),pid+': one colour per shape type'))
    res.append(ok(not any(s['fill'] for s in g),pid+': no fills'))
    own=sum(1 for s in g if s['ar']);sep=js("window.__sketchpadGetState().strokes.filter(s=>s.tplOf).length")
    res.append(ok(sep==0,pid+': arrows are part of their placeholder, not separate objects',(own,sep)))
  # edge crossing in every populated preset (relative to the tile origin)
  info=js("""(()=>{const I=window.__sketchpadTemplates,T=I.presets;return T.filter(p=>p.items.length).map(p=>{
    const X=p.items.filter(i=>i[1]<=6||i[1]>=94).length,Y=p.items.filter(i=>i[2]<=6||i[2]>=94).length;return [p.name,X,Y]})})()""")
  print(info)
  res.append(ok(all(i[1]+i[2]>0 for i in info),'every premade layout uses the tile edges'))
  res.append(ok(sum(1 for i in info if i[1]>0 and i[2]>0)>=7,'most layouts cross both left/right and top/bottom'))
  # arrows: drawn by the placeholder itself, from its live geometry
  js("window.__sketchpadTemplates.loadById('scattered-floral')");pg.wait_for_timeout(300)
  base=js("""(()=>{const T=window.__sketchpadTemplates,S=window.__sketchpadGetState().strokes;const p=S.find(s=>s.tpl===1&&s.tplKind==='circle'&&s.tplArrow&&s.tplArrow.on);
    const pts=T.arrowPts(p);const cx=(p.shape.x0+p.shape.x1)/2,cy=(p.shape.y0+p.shape.y1)/2,w=Math.abs(p.shape.x1-p.shape.x0);
    const xs=pts.map(q=>q.x),ys=pts.map(q=>q.y);return {id:p.id,cx,cy,w,ax:(Math.min(...xs)+Math.max(...xs))/2,ay:(Math.min(...ys)+Math.max(...ys))/2,span:Math.max(...xs)-Math.min(...xs)}})()""")
  res.append(ok(abs(base['ax']-base['cx'])<2 and abs(base['ay']-base['cy'])<2,'arrow is centred in its placeholder',base))
  res.append(ok(base['span']<base['w']*0.7,'arrow size is proportional to the shape',(base['span'],base['w'])))
  # live drag preview: points moved, shape not yet: the arrow still follows the points
  mv=js("""id=>{const T=window.__sketchpadTemplates,p=window.__sketchpadGetState().strokes.find(s=>s.id===id);const q={...p,points:p.points.map(t=>({...t,x:t.x+80,y:t.y+35}))};
    const a=T.arrowPts(p),b=T.arrowPts(q);return [b[0].x-a[0].x,b[0].y-a[0].y]}""",base['id'])
  res.append(ok(abs(mv[0]-80)<0.5 and abs(mv[1]-35)<0.5,'arrow follows a live drag preview',mv))
  # resize through the app's own Bigger button
  js("id=>window.__sketchpadTemplates.select(id)",base['id']);pg.wait_for_timeout(200)
  js("document.getElementById('shapeBiggerBtn').click()");pg.wait_for_timeout(300)
  g2=js("""id=>{const T=window.__sketchpadTemplates,p=window.__sketchpadGetState().strokes.find(s=>s.id===id);const pts=T.arrowPts(p);const xs=pts.map(q=>q.x);return {w:Math.abs(p.shape.x1-p.shape.x0),span:Math.max(...xs)-Math.min(...xs),cx:(p.shape.x0+p.shape.x1)/2,ax:(Math.min(...xs)+Math.max(...xs))/2}}""",base['id'])
  res.append(ok(g2['w']>base['w']+1 and g2['span']>base['span']+1 and abs(g2['ax']-g2['cx'])<2,'arrow grows and stays centred when the shape is resized',g2))
  # rotate the shape: arrow turns with it
  js("document.getElementById('shapeRotCwBtn')&&0")
  js("""id=>{const I=window.__sketchpadInternals(),p=I.strokes.find(s=>s.id===id);p.shape.rotation=40;}""",base['id'])
  ang=js("""id=>{const T=window.__sketchpadTemplates,p=window.__sketchpadGetState().strokes.find(s=>s.id===id);const a=T.arrowPts(p);return Math.round(Math.atan2(a[1].y-a[0].y,a[1].x-a[0].x)*180/Math.PI)}""",base['id'])
  res.append(ok(ang==40+int(base.get('a',0)) or ang in(40,),'arrow turns with its shape',ang))
  js("document.getElementById('tplArrowAng').value='90';document.getElementById('tplArrowAng').dispatchEvent(new Event('input'))");pg.wait_for_timeout(200)
  ang2=js("""id=>{const T=window.__sketchpadTemplates,p=window.__sketchpadGetState().strokes.find(s=>s.id===id);const a=T.arrowPts(p);return Math.round(Math.atan2(a[1].y-a[0].y,a[1].x-a[0].x)*180/Math.PI)}""",base['id'])
  res.append(ok(ang2==130,'arrow direction can be set separately (shape 40 + arrow 90)',ang2))
  # arrows hidden with one control: ink drops in the guide PNG only when arrows are left out; control flips the flag
  js("document.getElementById('tplArrowsBtn').click()");pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().layers.find(l=>l.tpl===1).arHide")==1,'Show/Hide all arrows'))
  js("document.getElementById('tplArrowsBtn').click()")
  inkA=js("""(async()=>{const c=await window.__sketchpadTemplates.render(600,600,{preview:false,outlines:true,arrows:true,opacity:100});const d=c.getContext('2d').getImageData(0,0,600,600).data;let a=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)a++;return a})()""")
  inkB=js("""(async()=>{const c=await window.__sketchpadTemplates.render(600,600,{preview:false,outlines:true,arrows:false,opacity:100});const d=c.getContext('2d').getImageData(0,0,600,600).data;let a=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)a++;return a})()""")
  res.append(ok(inkA>inkB,'arrows are included in the export unless left out',(inkA,inkB)))
  # deleting a placeholder removes its arrow with it (nothing is left behind)
  js("""id=>{const I=window.__sketchpadInternals();const i=I.strokes.findIndex(s=>s.id===id);I.strokes.splice(i,1);I.rebuildAllLayers();I.pushHist();}""",base['id']);pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().strokes.filter(s=>s.tpl===2).length")==0,'no stray arrow objects after deleting'))
  # saved data does not store the derived arrows
  d=js("window.__sketchpadTemplates.doc('x')");res.append(ok(not any(o['k']=='ar' for o in d['objs']) and any('ar' in o for o in d['objs']),'saved template keeps arrow direction, not extra arrow objects'))
  # colour all of a type
  js("window.__sketchpadTemplates.loadById('tossed-mixed')");pg.wait_for_timeout(300)
  cid=js("window.__sketchpadGetState().strokes.find(s=>s.tpl===1&&s.tplKind==='circle').id")
  js("id=>window.__sketchpadTemplates.select(id)",cid)
  js("document.getElementById('tplColour').value='#112233';document.getElementById('tplColourAllBtn').click()");pg.wait_for_timeout(300)
  cc=js("window.__sketchpadGetState().strokes.filter(s=>s.tpl===1).map(s=>[s.tplKind,s.color])")
  res.append(ok(all(c=='#112233' for k,c in cc if k=='circle') and all(c!='#112233' for k,c in cc if k!='circle'),'colour all circles only'))
  # old saved templates (no arrows, own colours) still load untouched
  old={'format':'pattern-sketch-template','version':1,'name':'Old','layout':'grid','tile':{'w':780,'h':780},'guide':{'opacity':80,'phVisible':True,'arVisible':True,'locked':False},
       'objs':[{'k':'ph','kind':'circle','col':'#abcdef','size':5,'type':'circle','x0':0.1,'x1':0.3,'y0':0.1,'y1':0.3,'rot':0,'fh':False,'fv':False},{'k':'ar','kind':'arrow','col':'#123456','size':4,'type':'arrow','x0':0.5,'x1':0.7,'y0':0.5,'y1':0.6,'rot':45,'fh':False,'fv':False}]}
  v=js("d=>window.__sketchpadTemplates.validate(d)",old);js("(o)=>window.__sketchpadTemplates.apply(o.objs,{name:'Old',guide:o.guide})",v);pg.wait_for_timeout(300)
  oc=js("window.__sketchpadGetState().strokes.filter(s=>s.tpl).map(s=>[s.tpl,s.color])")
  res.append(ok(['1','#abcdef'] in [[str(a),c] for a,c in oc] and len(oc)==2,'older saved templates keep their own colours and loose arrows',oc))
  print('errs',errs);print('ALL PASS' if all(res) and not errs else 'SOME FAILED');b.close()
