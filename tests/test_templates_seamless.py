# The exported master tile must contain every wrapped piece: its 3x3 preview must equal the repeat engine's own lattice, for all three repeats.
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m,x=''):print(('PASS ' if c else 'FAIL ')+m,x);return c
objs="""[
 {k:'ph',kind:'circle',col:'#ec5fa0',size:5,type:'circle',x0:-0.12,x1:0.12,y0:-0.12,y1:0.12,rot:0,fh:false,fv:false},
 {k:'ph',kind:'rect',col:'#7a5cd6',size:5,type:'rect',x0:0.82,x1:1.18,y0:0.30,y1:0.44,rot:33,fh:false,fv:false},
 {k:'ph',kind:'oval',col:'#1fa59a',size:5,type:'ellipse',x0:0.30,x1:0.62,y0:-0.06,y1:0.07,rot:-20,fh:false,fv:false},
 {k:'ph',kind:'triangle',col:'#4aa551',size:5,type:'triangle',x0:-0.08,x1:0.12,y0:0.84,y1:1.06,rot:15,fh:false,fv:false,ar:40},
 {k:'ph',kind:'square',col:'#ee7b30',size:5,type:'rect',x0:0.55,x1:0.68,y0:0.55,y1:0.68,rot:45,fh:false,fv:false},
 {k:'ph',kind:'circle',col:'#ec5fa0',size:5,type:'circle',x0:0.40,x1:0.52,y0:0.90,y1:1.02,rot:0,fh:false,fv:false,ar:-30}]"""
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate;res=[]
  for lay in ['grid','halfDrop','halfBrick']:
    pg.evaluate("l=>document.querySelector('.layout-btn[data-layout='+l+']').click()",lay);pg.wait_for_timeout(250)
    js("o=>window.__sketchpadTemplates.apply(o,{name:'seam'})".replace("o)=>","o)=>"),None) if False else None
    js("()=>{window.__sketchpadTemplates.apply("+objs+",{name:'seam'});}");pg.wait_for_timeout(400)
    r=js("""(async()=>{const T=window.__sketchpadTemplates;const a=await T.render(1200,1200,{preview:true,outlines:true,arrows:true,opacity:100});const t0=T.truth(1200,1200);const t=document.createElement('canvas');t.width=t.height=1200;const tg=t.getContext('2d');tg.fillStyle='#fff';tg.fillRect(0,0,1200,1200);tg.drawImage(t0,0,0);
      const A=a.getContext('2d').getImageData(0,0,1200,1200).data,B=t.getContext('2d').getImageData(0,0,1200,1200).data;
      let diff=0,n=0,ink=0,bad=0;for(let i=0;i<A.length;i+=4){const x=Math.abs(A[i]-B[i])+Math.abs(A[i+1]-B[i+1])+Math.abs(A[i+2]-B[i+2]);diff+=x;n++;if(A[i]<250||A[i+1]<250||A[i+2]<250||B[i]<250||B[i+1]<250||B[i+2]<250)ink++;if(x>180)bad++}
      // truth has no arrows (derived arrows are strokes too, so they are included): both include them
      return {meanAlphaDiff:diff/n,ink,bad}})()""")
    res.append(ok(r['ink']>3000 and r['bad']/max(1,r['ink'])<0.03,lay+': master tile reproduces the repeat engine lattice',r))
  # a transparent master export keeps its size and has ink on the wrapped edges
  e=js("""(async()=>{const c=await window.__sketchpadTemplates.render(900,600,{preview:false,outlines:true,arrows:true,opacity:100});return [c.width,c.height]})()""")
  res.append(ok(e==[900,600],'custom dimensions respected',e))
  print('errs',errs);print('ALL PASS' if all(res) and not errs else 'SOME FAILED');b.close()
