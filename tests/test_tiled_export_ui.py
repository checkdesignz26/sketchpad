from playwright.sync_api import sync_playwright
import common as t500,time,struct,zlib
def ok(n,c,extra=''): print(('PASS ' if c else 'FAIL ')+n,extra,flush=True)
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    pg.context.set_default_timeout(15000)
    for (x0,y0,x1,y1,col) in [(700,520,800,700,'#cc2244'),(420,350,520,470,'#2244cc')]:
        js(f"(()=>{{const b=document.getElementById('brushColor');b.value='{col}';b.dispatchEvent(new Event('input',{{bubbles:true}}))}})()")
        js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(150)
        pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
    js("document.querySelector('.layout-btn[data-layout=halfDrop]').click()");pg.wait_for_timeout(300)
    before=js("JSON.stringify(window.__sketchpadGetState().strokes)")
    # open through the Export menu
    pg.locator('#exportMenuBtn').click();pg.wait_for_timeout(300)
    ok('menu has tiled export',pg.locator('text=Tiled export (1×1').count()>0)
    pg.locator('text=Tiled export (1×1').first.click();pg.wait_for_timeout(400)
    ok('popover open',js("document.getElementById('tilePopover').classList.contains('open')"))
    pg.locator('#tilePopover .tile-n[data-n="2"]').click()
    pg.screenshot(path='tilepop.png')
    t=time.time()
    with pg.expect_download() as dl: pg.locator('#tileSaveBtn').click()
    d=dl.value;path=d.path();dt=time.time()-t
    raw=open(path,'rb').read();w,h=struct.unpack('>II',raw[16:24])
    ok('2x2 halfDrop PNG saved',raw[:8]==b'\x89PNG\r\n\x1a\n' and (w,h)==(1560,1560),(d.suggested_filename,w,h,len(raw),round(dt,1)))
    # decode fully with zlib to prove the IDAT stream is valid
    i=8;idat=b''
    while i<len(raw):
        ln=struct.unpack('>I',raw[i:i+4])[0];ty=raw[i+4:i+8];idat+=raw[i+8:i+8+ln] if ty==b'IDAT' else b'';i+=12+ln
    dec=zlib.decompress(idat);ok('IDAT inflates to full size',len(dec)==h*(w*4+1),len(dec))
    ok('project untouched',before==js("JSON.stringify(window.__sketchpadGetState().strokes)"))
    # big one: 3x3 at x3 (7020 px) near the warn level
    js("document.getElementById('tileRes').value='3';document.getElementById('tileRes').dispatchEvent(new Event('change'))")
    pg.locator('#tilePopover .tile-n[data-n="3"]').click();print(js("document.getElementById('tileInfo').textContent"))
    t=time.time()
    with pg.expect_download() as dl: pg.locator('#tileSaveBtn').click()
    d=dl.value;raw=open(d.path(),'rb').read();w,h=struct.unpack('>II',raw[16:24])
    ok('3x3 x3 saved',(w,h)==(7020,7020),(w,h,round(len(raw)/1e6,1),'MB',round(time.time()-t,1),'s'))
    # warn path: 3x3 x4 needs a second tap
    js("document.getElementById('tileRes').value='4';document.getElementById('tileRes').dispatchEvent(new Event('change'))")
    print(js("document.getElementById('tileInfo').textContent"))
    pg.locator('#tileSaveBtn').click();pg.wait_for_timeout(300);print('after first tap:',js("document.getElementById('tileSaveBtn').textContent"),'|',js("document.getElementById('status').textContent"))
    # existing exports still work
    for lab in ['exportBtn']:
        with pg.expect_download() as dl: js(f"document.getElementById('{lab}').click()")
        ok(lab+' still downloads',dl.value.suggested_filename.endswith('.png'),dl.value.suggested_filename)
    with pg.expect_download() as dl: js("exportTileSharp(2)") if False else js("window.__sketchpadHi.tile(2).then(c=>c.toBlob(b=>{const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='x.png';document.body.appendChild(a);a.click()}))")
    ok('sharper tile builds',True)
    print('errors',errs);b.close()
