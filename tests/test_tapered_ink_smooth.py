import sys;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from playwright.sync_api import sync_playwright
def ok(c,m):
  assert c,m;print('PASS',m)
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.goto('http://localhost:8790/index.html');pg.wait_for_timeout(2500)
  r=pg.evaluate("""(()=>{const br=BrushEngine.getBrush('taperedInk'),base=BrushEngine.getSettings('taperedInk'),out={};
   for(const sc of [1,8,32]){const c=document.createElement('canvas');c.width=1100;c.height=400;const g=c.getContext('2d');g.setTransform(sc,0,0,sc,0,0);
    const pts=[];for(let i=0;i<=80;i++)pts.push({x:2+i*(1000/sc)/80,y:200/sc,pressure:.5});
    BrushEngine.renderStroke(g,{id:'x',points:pts,color:'#000'},br,Object.assign({},base,{size:8}),1);
    const d=g.getImageData(0,0,1100,400).data,top=[];for(let x=300;x<800;x++){let y=0;while(y<400&&d[(y*1100+x)*4+3]<128)y++;top.push(y);}
    out[sc]=Math.max(...top)-Math.min(...top);}
   return out})()""")
  print(r)
  ok(all(v<=2 for v in r.values()),'Tapered Ink body edge is smooth at 1x, 8x and 32x zoom (no scalloping)')
  b.close()
