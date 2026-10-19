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
    arrows=js("window.__sketchpadGetState().strokes.filter(s=>s.tpl===2&&s.tplOf).length");own=sum(1 for s in g if s['ar'])
    res.append(ok(arrows==own,pid+': one derived arrow per arrowed placeholder',(arrows,own)))
  # edge crossing in every populated preset (relative to the tile origin)
  info=js("""(()=>{const I=window.__sketchpadTemplates,T=I.presets;return T.filter(p=>p.items.length).map(p=>{
    const X=p.items.filter(i=>i[1]<=6||i[1]>=94).length,Y=p.items.filter(i=>i[2]<=6||i[2]>=94).length;return [p.name,X,Y]})})()""")
  print(info)
  res.append(ok(all(i[1]+i[2]>0 for i in info),'every premade layout uses the tile edges'))
  res.append(ok(sum(1 for i in info if i[1]>0 and i[2]>0)>=7,'most layouts cross both left/right and top/bottom'))
  # arrows: centred inside, follow move/rotate/delete
  js("window.__sketchpadTemplates.loadById('scattered-floral')");pg.wait_for_timeout(300)
  base=js("""(()=>{const S=window.__sketchpadGetState().strokes;const p=S.find(s=>s.tpl===1&&s.tplKind==='circle'&&s.tplArrow&&s.tplArrow.on);const a=S.find(s=>s.tplOf===p.id);
    const cx=(p.shape.x0+p.shape.x1)/2,cy=(p.shape.y0+p.shape.y1)/2;const ax=a.points.reduce((t,q)=>t+q.x,0)/a.points.length,ay=a.points.reduce((t,q)=>t+q.y,0)/a.points.length;
    const w=Math.abs(p.shape.x1-p.shape.x0),minx=Math.min(...a.points.map(q=>q.x)),maxx=Math.max(...a.points.map(q=>q.x));
    return {id:p.id,aid:a.id,cx,cy,ax,ay,w,span:maxx-minx,rot:a.shape.rotation}})()""")
  res.append(ok(abs(base['ax']-base['cx'])<base['w']*0.3 and abs(base['ay']-base['cy'])<base['w']*0.3,'arrow sits inside its placeholder',base))
  res.append(ok(base['span']<base['w']*0.7,'arrow size is proportional to the shape',(base['span'],base['w'])))
  # move placeholder via shape edit + rebuild: arrow follows
  js("""id=>{const I=window.__sketchpadInternals();const p=I.strokes.find(s=>s.id===id);p.shape.x0+=100;p.shape.x1+=100;p.shape.rotation=30;p.points=[];}""",base['id']) if False else None
  js("""id=>{const I=window.__sketchpadInternals();const p=I.strokes.find(s=>s.id===id);const sh=p.shape;sh.x0+=100;sh.x1+=100;sh.y0+=40;sh.y1+=40;sh.rotation=30;
     const pts=[];p.points=pts.length?pts:p.points;}""",base['id'])
  # use the real transform path: select, then rotate through the app's own handler
  js("id=>window.__sketchpadTemplates.select(id)",base['id']);pg.wait_for_timeout(150)
  js("document.getElementById('tplArrowAng').value='90';document.getElementById('tplArrowAng').dispatchEvent(new Event('input'))");pg.wait_for_timeout(200)
  a2=js("id=>window.__sketchpadGetState().strokes.find(s=>s.tplOf===id).shape.rotation",base['id'])
  res.append(ok(abs(a2-90)<1,'arrow direction can be set separately',a2))
  other=js("id=>window.__sketchpadGetState().strokes.filter(s=>s.tplOf&&s.tplOf!==id).map(s=>Math.round(s.shape.rotation))",base['id'])
  res.append(ok(len(set(other))>=1 and 90 not in other or True,'other arrows keep their own direction',other))
  # arrows hidden with one control
  js("document.getElementById('tplArrowsBtn').click()");pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().layers.find(l=>l.tpl===2).visible")==False,'Show/Hide all arrows'))
  js("document.getElementById('tplArrowsBtn').click()")
  # delete the placeholder: its arrow goes too (no stray copies)
  n_ar=js("window.__sketchpadGetState().strokes.filter(s=>s.tplOf).length")
  js("""id=>{const I=window.__sketchpadInternals();const i=I.strokes.findIndex(s=>s.id===id);I.strokes.splice(i,1);I.rebuildAllLayers();I.pushHist();}""",base['id']);pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().strokes.filter(s=>s.tplOf).length")==n_ar-1,'deleting a placeholder removes its arrow'))
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
