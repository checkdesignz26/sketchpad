from playwright.sync_api import sync_playwright
import json
def ok(n,c,extra=''): print(('PASS ' if c else 'FAIL ')+n,extra,flush=True)
ST="window.__sketchpadGetState()"
def boot(p,vw,vh):
    b=p.chromium.launch();pg=b.new_context(viewport={'width':vw,'height':vh},has_touch=True).new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8790/index.html');pg.wait_for_timeout(2000)
    pg.locator('button:has-text("New Project"):visible').first.click();pg.wait_for_timeout(600)
    pg.locator('button:has-text("Start drawing")').click();pg.wait_for_timeout(2500)
    return b,pg,errs
def draw(pg,vw):
    js=pg.evaluate
    for (fx,fy,gx,gy,col) in [(.62,.55,.72,.78,'#cc2244'),(.40,.40,.50,.60,'#2244cc')]:
        js(f"(()=>{{const b=document.getElementById('brushColor');b.value='{col}';b.dispatchEvent(new Event('input',{{bubbles:true}}))}})()")
        js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(150)
        vh=pg.viewport_size['height']
        pg.mouse.move(vw*fx,vh*fy);pg.mouse.down();pg.mouse.move(vw*gx,vh*gy,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
# preview canvas vs analytic lattice rule built from a small tile
RULE="""async()=>{const c=document.getElementById('tilePrev');const g=c.getContext('2d');const W=c.width,H=c.height;
 const key=window.__sketchpadTileExport; return [W,H]}"""
with sync_playwright() as p:
    for (vw,vh,label) in [(1180,820,'iPad 11in landscape'),(1024,768,'iPad 9.7in landscape'),(820,1180,'iPad 11in portrait'),(744,1133,'iPad mini portrait')]:
        b,pg,errs=boot(p,vw,vh);js=pg.evaluate;draw(pg,vw)
        print('==',label,vw,vh,flush=True)
        js("document.querySelector('.layout-btn[data-layout=halfDrop]').click()");pg.wait_for_timeout(300)
        pg.locator('#exportMenuBtn').click();pg.wait_for_timeout(300)
        pg.locator('text=Tiled export (1×1').first.click();pg.wait_for_timeout(1200)
        js("document.querySelector('.layout-btn[data-layout=grid]').click()");pg.wait_for_timeout(1000)
        PER="""(n)=>{const c=document.getElementById('tilePrev');const W=c.width,H=c.height;const e=c.getContext('2d').getImageData(0,0,W,H).data;const p=Math.round(W/n);let bad=0,k=0;
          for(let y=0;y<H;y+=3)for(let x=0;x+p<W;x+=3){const a=(y*W+x)*4,b=(y*W+x+p)*4;k++;if(Math.abs(e[a]-e[b])>4||Math.abs(e[a+1]-e[b+1])>4||Math.abs(e[a+2]-e[b+2])>4)bad++;}
          return {bad,k,W}}"""
        res={}
        for n in (1,2,3):
            pg.locator(f'#tilePopover .tile-n[data-n="{n}"]').click();pg.wait_for_timeout(700)
            res[n]=js(PER,n if n>1 else 2)
        ok('preview follows 1x1 / 2x2 / 3x3 (repeats appear immediately)',res[1]['bad']>20 and res[2]['bad']==0 and res[3]['bad']==0,res)
        js("document.querySelector('.layout-btn[data-layout=halfDrop]').click()");pg.wait_for_timeout(1000)
        # layout rule on preview pixels (n=2 half drop)
        pg.locator('#tilePopover .tile-n[data-n="2"]').click();pg.wait_for_timeout(700)
        r=js("""async()=>{const c=document.getElementById('tilePrev');const W=c.width,H=c.height,tw=W/2,th=H/2;
          const e=c.getContext('2d').getImageData(0,0,W,H).data;
          // tile = top-left quadrant column 0 ; column 1 must equal column 0 shifted down by th/2 (wrapped)
          let bad=0,n=0;for(let y=0;y<H;y+=2)for(let x=0;x<tw;x+=2){const sy=((y-Math.floor(th/2))%H+H)%H,a=((y)*W+x)*4,b=(sy*W+(x+tw))*4;
            // column0 pixel at (x,y) ; column1 pixel at (x+tw, y+th/2 wrap within the picture)
            const y2=(y+Math.floor(th/2))%H; const b2=(y2*W+(x+tw))*4;n++;
            if(Math.abs(e[a]-e[b2])>3||Math.abs(e[a+1]-e[b2+1])>3||Math.abs(e[a+2]-e[b2+2])>3)bad++;}
          return {bad,n,W,H}}""")
        ok('half-drop preview: 2nd column dropped by half a tile',r['bad']<=r['n']*0.01,r)
        # preview vs real export (scaled): same arrangement
        r=js("""async()=>{const ex=await window.__sketchpadTileExport.png(2,1,false);const bmp=await createImageBitmap(ex.blob);
          const c=document.getElementById('tilePrev');const t=document.createElement('canvas');t.width=c.width;t.height=c.height;const g=t.getContext('2d');g.imageSmoothingQuality='high';g.drawImage(bmp,0,0,c.width,c.height);
          const a=t.getContext('2d').getImageData(0,0,t.width,t.height).data,b=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let sum=0;for(let i=0;i<a.length;i+=4){sum+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);}
          return {meanAbsDiff:Math.round(sum/(a.length/4)/3*100)/100,w:c.width,h:c.height}}""")
        ok('preview matches the exported picture (scaled)',r['meanAbsDiff']<6,r)
        # guides: overlay only, export identical
        before=js("""async()=>{const ex=await window.__sketchpadTileExport.png(2,1,false);return ex.blob.size}""")
        pg.locator('#tileGuides').check();pg.wait_for_timeout(500)
        g=js("""(()=>{const g=document.getElementById('tilePrevG'),c=document.getElementById('tilePrev');const d=g.getContext('2d').getImageData(0,0,g.width,g.height).data;let k=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)k++;return k})()""")
        after=js("""async()=>{const ex=await window.__sketchpadTileExport.png(2,1,false);return ex.blob.size}""")
        ok('guides drawn on overlay only',g>50 and before==after,{'overlay_px':g,'export_bytes_before':before,'after':after})
        # transparency in preview
        pg.locator('#tileTransparent').check();pg.wait_for_timeout(700)
        t=js("""(()=>{const c=document.getElementById('tilePrev');const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let k=0;for(let i=3;i<d.length;i+=4)if(d[i]<255)k++;return k})()""")
        ok('transparent background shows in preview',t>0,t)
        pg.locator('#tileTransparent').uncheck();pg.wait_for_timeout(500)
        # layout switch while open
        js("document.querySelector('.layout-btn[data-layout=halfBrick]').click()");pg.wait_for_timeout(1500)
        ok('preview follows layout change',js("document.getElementById('tileLayNote').textContent").startswith('Layout: Half Brick'),js("document.getElementById('tileLayNote').textContent")[:40])
        # usability: panel inside viewport, no overlaps between controls
        pg.wait_for_timeout(300)
        r=js("""(()=>{const P=document.getElementById('tilePopover').getBoundingClientRect();
          const els=[...document.querySelectorAll('#tilePopover .tile-n, #tileRes, #tileTransparent, #tileGuides, #tileSaveBtn, #tileCloseBtn, #tilePrevBox')].map(e=>({id:e.id||e.className,r:e.getBoundingClientRect()}));
          let overlaps=[];for(let i=0;i<els.length;i++)for(let j=i+1;j<els.length;j++){const a=els[i].r,b=els[j].r;if(a.width&&b.width&&a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)overlaps.push([els[i].id,els[j].id]);}
          const sv=document.getElementById('tileSaveBtn').getBoundingClientRect();
          return {panel:[Math.round(P.left),Math.round(P.top),Math.round(P.right),Math.round(P.bottom)],vh:innerHeight,vw:innerWidth,overlaps,saveVisible:sv.bottom<=innerHeight&&sv.top>=0,scrolls:document.getElementById('tilePopover').scrollHeight>document.getElementById('tilePopover').clientHeight}})()""")
        ok(f'{label}: no overlapping controls, inside screen',not r['overlaps'] and r['panel'][2]<=r['vw'] and r['panel'][3]<=r['vh'],r)
        pg.screenshot(path=f'tileprev_{vw}x{vh}.png')
        # real tap works on Save while a stroke panel is around
        print('errors',errs);b.close()
