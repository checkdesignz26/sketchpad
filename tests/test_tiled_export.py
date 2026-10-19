from playwright.sync_api import sync_playwright
import common as t500
def ok(n,c,extra=''): print(('PASS ' if c else 'FAIL ')+n,extra,flush=True)
CHECK="""async (args)=>{
 const [n,k,layout,transparent]=args;
 const TX=window.__sketchpadTileExport,H=window.__sketchpadHi;
 const tile=await H.tile(k,transparent); // the seamless tile, via the existing engine
 const tw=tile.width,th=tile.height;
 const tg=tile.getContext('2d').getImageData(0,0,tw,th).data;
 const r=await TX.png(n,k,transparent);
 const bmp=await createImageBitmap(r.blob);
 const c=document.createElement('canvas');c.width=bmp.width;c.height=bmp.height;const g=c.getContext('2d');g.drawImage(bmp,0,0);
 const W=c.width,Hh=c.height,e=g.getImageData(0,0,W,Hh).data;
 // expected pixel from the lattice rule
 let bad=0,checked=0,firstBad=null;
 const sh=(layout==='halfDrop'||layout==='halfBrick');
 for(let y=0;y<Hh;y++)for(let x=0;x<W;x++){
   const ix=Math.floor(x/tw),iy=Math.floor(y/th);let tx,ty;
   if(layout==='halfDrop'&&n>1){const dy=(ix%2)?Math.floor(th/2):0;tx=x-ix*tw;ty=((y-dy)%Hh+Hh)%Hh;ty=((ty%th)+th)%th;}
   else if(layout==='halfBrick'&&n>1){const dx=(iy%2)?Math.floor(tw/2):0;ty=y-iy*th;tx=(((x-dx)%W)+W)%W;tx=((tx%tw)+tw)%tw;}
   else{tx=x-ix*tw;ty=y-iy*th;}
   const a=(y*W+x)*4,b=(ty*tw+tx)*4;checked++;
   if(Math.abs(e[a]-tg[b])>2||Math.abs(e[a+1]-tg[b+1])>2||Math.abs(e[a+2]-tg[b+2])>2||Math.abs(e[a+3]-tg[b+3])>2){bad++;if(!firstBad)firstBad=[x,y];}
 }
 // transparency: any alpha<255 pixel?
 let transp=0;for(let i=3;i<e.length;i+=4)if(e[i]<255)transp++;
 return {W,H:Hh,tw,th,bad,checked,firstBad,transp,bytes:r.blob.size,seamless:r.plan.seamless};
}"""
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    # artwork that crosses the tile edges so wrap matters
    for (x0,y0,x1,y1,col) in [(700,520,800,700,'#cc2244'),(420,350,520,470,'#2244cc')]:
        js(f"(()=>{{const b=document.getElementById('brushColor');b.value='{col}';b.dispatchEvent(new Event('input',{{bubbles:true}}))}})()")
        js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(150)
        pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
    print('strokes',js("window.__sketchpadGetState().strokes.length"),'tile',js("[TW,TH]") if False else '')
    for layout in ['grid','halfDrop','halfBrick']:
        js(f"document.querySelector('.layout-btn[data-layout={layout}]').click()");pg.wait_for_timeout(400)
        for n in (1,2,3):
            r=js(CHECK,[n,1,layout,False])
            ok(f'{layout} {n}x{n} matches lattice rule',r['bad']==0 and r['W']==n*r['tw'] and r['H']==n*r['th'],r)
    # transparency
    js("document.querySelector('.layout-btn[data-layout=grid]').click()");pg.wait_for_timeout(300)
    r=js(CHECK,[2,1,'grid',True]);ok('transparent keeps alpha',r['bad']==0 and r['transp']>0,r)
    r=js(CHECK,[2,1,'grid',False]);ok('opaque has none',r['bad']==0 and r['transp']==0,r)
    # limits
    lim=js("[1,2,3].map(n=>[1,2,3,4].map(k=>{const l=window.__sketchpadTileExport.limit(n,k);return [n,k,!!l.hard,!!l.warn,l.z.W+'x'+l.z.H]}))")
    for row in lim: print(row)
    # UI
    js("window.__sketchpadTileExport.open()");pg.wait_for_timeout(300)
    print('info:',js("document.getElementById('tileInfo').textContent"));print('note:',js("document.getElementById('tileLayNote').textContent"))
    pg.screenshot(path='tilepop.png')
    print('errors',errs);b.close()
