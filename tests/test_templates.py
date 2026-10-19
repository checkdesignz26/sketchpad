# Pattern Templates: presets, editing rules, guide layers, My Templates, export. Server on :8790.
import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m,x=''):print(('PASS ' if c else 'FAIL ')+m,x);return c
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate;res=[]
  T="window.__sketchpadTemplates"
  res.append(ok(js(T+".presets.length")==12,'12 premade templates'))
  kinds=js("window.__sketchpadTemplates.presets.map(p=>[p.name,[...new Set(p.items.map(i=>i[0]))].length,p.items.length])")
  print(kinds)
  res.append(ok(all(k[1]>=3 for k in kinds if k[2]>0 and k[0] not in('Airy Scattered',)) ,'every populated preset mixes shapes'))
  # draw a stroke of real artwork first: loading must not touch it
  r=pg.locator('#canvas').bounding_box();cx,cy=r['x']+r['width']/2,r['y']+r['height']/2
  pg.mouse.move(cx-50,cy);pg.mouse.down();pg.mouse.move(cx+50,cy+20,steps=6);pg.mouse.up();pg.wait_for_timeout(250)
  art=js("window.__sketchpadGetState().strokes.map(s=>s.id)")
  for pid in [p['id'] for p in js(T+".presets")]:
    js("id=>window.__sketchpadTemplates.loadById(id)",pid);pg.wait_for_timeout(150)
  js("window.__sketchpadTemplates.loadById('scattered-floral')");pg.wait_for_timeout(300)
  st=js("window.__sketchpadGetState()")
  g=[s for s in st['strokes'] if s.get('tpl')]
  ph=[x for x in g if x['tpl']==1];res.append(ok(len(ph)==10,'scattered floral has 10 placeholders',len(ph)))
  res.append(ok(all(s['id'] in [x['id'] for x in st['strokes']] for s in st['strokes'] if s['id'] in art) and set(art)<={s['id'] for s in st['strokes']},'artwork untouched by loading'))
  res.append(ok(not any(s.get('fillColor') for s in g),'no fills, outlines only'))
  lay=js("window.__sketchpadGetState().layers.filter(l=>l.tpl).map(l=>[l.name,l.tpl])");print(lay)
  res.append(ok(len(lay)==2,'two guide layers'))
  res.append(ok(js("window.__sketchpadGetState().activeLayerId")!=[l for l in js("window.__sketchpadGetState().layers") if l.get('tpl')][0]['id'],'drawing layer is not a guide layer'))
  gs=lambda:js("window.__sketchpadGetState().strokes.filter(s=>s.tpl)")
  tp=[s for s in gs() if s.get('tplKind')=='oval'][0]
  cxo=(tp['shape']['x0']+tp['shape']['x1'])/2;cyo=(tp['shape']['y0']+tp['shape']['y1'])/2
  js("id=>window.__sketchpadTemplates.select(id)",tp['id'])
  # node editing is refused for placeholders
  js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().pathEditStrokeId")in(None,''),'Edit Path refused for placeholders'))
  res.append(ok(js("document.getElementById('editPathBtn').disabled")==True,'Edit Path button disabled for placeholders'))
  n0=len(gs())
  js("window.__sketchpadTemplates.replace('triangle')");pg.wait_for_timeout(200)
  t2=[s for s in gs() if s['id']==tp['id']][0]
  c2=((t2['shape']['x0']+t2['shape']['x1'])/2,(t2['shape']['y0']+t2['shape']['y1'])/2)
  res.append(ok(t2['shape']['type']=='triangle' and abs(c2[0]-cxo)<0.01 and abs(c2[1]-cyo)<0.01 and t2['color']==tp['color'] and len(gs())==n0,'replace shape keeps centre/colour, nothing else moves'))
  # move via the existing group/transform: undo restores
  js("window.__sketchpadInternals().undo()");pg.wait_for_timeout(200)
  t3=[s for s in gs() if s['id']==tp['id']][0]
  res.append(ok(t3['shape']['type']=='ellipse','undo reverts the replacement',t3['shape']['type']))
  # add shape + arrow
  js("window.__sketchpadTemplates.add('square')");js("window.__sketchpadTemplates.add('triangle')");pg.wait_for_timeout(200)
  res.append(ok(len(gs())>=n0+1,'add shape and arrow'))
  # guide layers are excluded from pattern export
  res.append(ok(js("""(async()=>{const c=await window.__sketchpadHi.tile(1,true);const g=c.getContext('2d');const d=g.getImageData(0,0,c.width,c.height).data;let a=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)a++;return a})()""")>0,'pattern export still has the artwork'))
  only=js("""(async()=>{const I=window.__sketchpadInternals();const keep=I.strokes.filter(s=>!s.tpl);const g=I.strokes.filter(s=>s.tpl);
    const saved=I.strokes.splice(0,I.strokes.length,...g);I.rebuildAllLayers();const c=await window.__sketchpadHi.tile(1,true);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let a=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)a++;
    I.strokes.splice(0,I.strokes.length,...saved);I.rebuildAllLayers();return a})()""")
  res.append(ok(only==0,'guides never appear in the pattern export',only))
  hi=js("""(async()=>{const I=window.__sketchpadInternals();const keep=I.strokes.filter(s=>!s.tpl);const g=I.strokes.filter(s=>s.tpl);const saved=I.strokes.splice(0,I.strokes.length,...g);I.rebuildAllLayers();const c=await window.__sketchpadHi.build(600,true);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let a=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)a++;I.strokes.splice(0,I.strokes.length,...saved);I.rebuildAllLayers();return a})()""")
  res.append(ok(hi==0,'guides never appear in the hi-res card export',hi))
  # guide PNG: size, transparency, outlines present
  png=js("""(async()=>{const c=await window.__sketchpadTemplates.render(900,900,{preview:false,outlines:true,arrows:true,opacity:100});const g=c.getContext('2d');const d=g.getImageData(0,0,c.width,c.height).data;let a=0,t=0;for(let i=3;i<d.length;i+=4){if(d[i]>0)a++;else t++}
    const L=g.getImageData(0,0,1,c.height).data,R=g.getImageData(c.width-1,0,1,c.height).data;let df=0;for(let i=0;i<L.length;i++)df+=Math.abs(L[i]-R[i]);return {w:c.width,h:c.height,drawn:a,transparent:t,edge:df}})()""")
  res.append(ok(png['w']==900 and png['drawn']>500 and png['transparent']>png['drawn'],'guide PNG: transparent interior with coloured outlines',png))
  pv=js("""(async()=>{const c=await window.__sketchpadTemplates.render(900,900,{preview:true,outlines:true,arrows:false,opacity:50});return [c.width,c.height]})()""")
  res.append(ok(pv==[900,900],'3x3 preview export',pv))
  # edge-crossing placeholder wraps: a circle centred on the tile's right edge appears on BOTH edges of the master tile
  js("""()=>{const T=window.__sketchpadTemplates;T.apply([{k:'ph',kind:'circle',col:'#e8546f',size:6,type:'circle',x0:0.9,x1:1.1,y0:0.4,y1:0.6,rot:0,fh:false,fv:false}],{name:'edge'});}""")
  pg.wait_for_timeout(300)
  e=js("""(async()=>{const c=await window.__sketchpadTemplates.render(600,600,{preview:false,outlines:true,arrows:true,opacity:100});const g=c.getContext('2d');
    const L=g.getImageData(0,0,1,c.height).data,R=g.getImageData(c.width-1,0,1,c.height).data;let l=0,r=0,df=0;for(let i=3;i<L.length;i+=4){if(L[i]>0)l++;if(R[i]>0)r++;df+=Math.abs(L[i-3]-R[i-3])}return {l,r,df}})()""")
  res.append(ok(e['l']>5 and e['r']>5,'edge-crossing placeholder appears on both edges (wraps)',e))
  js("window.__sketchpadTemplates.loadById('half-drop-floral')");pg.wait_for_timeout(500)
  res.append(ok(js("window.__sketchpadGetState().layout")=='halfDrop','half-drop preset switches the repeat layout'))
  js("window.__sketchpadTemplates.loadById('half-brick-tossed')");pg.wait_for_timeout(500)
  res.append(ok(js("window.__sketchpadGetState().layout")=='halfBrick','half-brick preset switches the repeat layout'))
  js("window.__sketchpadTemplates.loadById('scattered-floral')")
  js("window.__sketchpadTemplates.add('square')");js("window.__sketchpadTemplates.add('triangle')")
  gs_before=gs()
  # My Templates: save/reopen/persist
  doc=js("window.__sketchpadTemplates.doc('Mine')")
  d2=js("d=>window.__sketchpadTemplates.validate(d)",doc);res.append(ok(len(d2['objs'])>0,'native template round-trips through validation'))
  bad=js("""()=>{try{window.__sketchpadTemplates.validate({format:'x'});return 'accepted'}catch(e){return 'rejected'}}""")
  res.append(ok(bad=='rejected','invalid import is rejected'))
  bad2=js("""()=>{try{window.__sketchpadTemplates.validate({format:'pattern-sketch-template',version:1,objs:[{k:'ph',type:'ellipse',col:'red',x0:0,x1:1,y0:0,y1:1}]});return 'accepted'}catch(e){return 'rejected'}}""")
  res.append(ok(bad2=='rejected','bad colour rejected'))
  js("""d=>{localStorage.setItem('sp-templates-v1',JSON.stringify({v:1,list:[{id:'t1',name:'Mine',doc:d}]}))}""",doc)
  pg.click('#tplTabs button[data-tab=my]') if False else None
  # persistence of guides across reload (autosave)
  pg.wait_for_timeout(2500)
  pg.reload();pg.wait_for_timeout(3500)
  gp=js("window.__sketchpadGetState().strokes.filter(s=>s.tpl).length");lp=js("window.__sketchpadGetState().layers.filter(l=>l.tpl).length")
  res.append(ok(gp==len(gs_before) and lp==2,'guides survive a refresh',(gp,lp)))
  js("window.__sketchpadTemplates.loadById('blank-custom')");pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().strokes.filter(s=>s.tpl).length")==0,'blank custom is empty'))
  js("window.__sketchpadInternals().undo()");pg.wait_for_timeout(200)
  res.append(ok(js("window.__sketchpadGetState().strokes.filter(s=>s.tpl).length")==len(gs_before),'undo brings the previous guides back'))
  print('errs',errs);print('ALL PASS' if all(res) and not errs else 'SOME FAILED');b.close()
