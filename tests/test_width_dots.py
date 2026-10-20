import sys,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  # draw a horizontal-ish lash by rendering a synthetic stroke at 17x zoom; compare gaps for several brushes & lengths
  res=js("""(()=>{
   const I=window.__sketchpadInternals();const out=[];
   for(const bid of ['taperedInk','smoothPen','pencil']){
    for(const L of [8,25,80]){
     const br=BrushEngine.getBrush(bid);if(!br)continue;
     const base=BrushEngine.getSettings(bid);
     const Z=17,W=Math.min(2400,Math.ceil(L*Z+80)),H=260;
     const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');g.setTransform(Z,0,0,Z,40,H/2);
     const pts=[];for(let i=0;i<=40;i++){pts.push({x:L*i/40/ (W>2400?1:1),y:-Math.sin(Math.PI*i/40)*L*.08,pressure:.5})}
     const wp=[{id:'ws',t:0,w:.08},{id:'a',t:.15,w:.55},{id:'b',t:.5,w:1},{id:'we',t:1,w:.08}];
     const st={id:'t'+L,brushId:bid,color:'#000',points:pts,wp,wpP:0,settings:{}};
     const s=Object.assign({},base,{size:4,pressureWidth:0});
     I.renderBrushStrokeCapped(g,st,br,s,1);
     const d=g.getImageData(0,0,W,H).data;
     let first=-1,last=-1,gaps=0,thick=[];
     for(let x=0;x<W;x++){let n=0;for(let y=0;y<H;y++)if(d[(y*W+x)*4+3]>60)n++;thick.push(n);if(n>0){if(first<0)first=x;last=x}}
     for(let x=first;x<=last;x++)if(thick[x]==0)gaps++;
     const mx=Math.max(...thick);
     out.push({bid,L,gaps,span:last-first,maxThickUnits:+(mx/Z).toFixed(2),tipPx:thick[first+3]});
    }
   }
   return out})()""")
  for r in res:print(r)
  for r in res:
    ok(r['gaps']==0,'%s length %d: no gaps/dots at 17x zoom'%(r['bid'],r['L']))
  b.close()
