from playwright.sync_api import sync_playwright
import common as t500
ST="window.__sketchpadGetState()"
def sel(pg): return pg.evaluate("(()=>{const s="+ST+";const S=s.strokes;const ms=s.multiSel;const src=ms&&S.find(x=>ms.strokeIds.includes(x.id)&&x.radial);const all=S.filter(x=>x.radial);return {single:s.selectedStrokeId?S.findIndex(x=>x.id===s.selectedStrokeId):null,multi:ms?ms.strokeIds.length:0,flower:src?all.indexOf(src):null,box:document.getElementById('groupBox').style.display}})()")
def scr(pg,k):
    pt=pg.evaluate("(()=>{const S=window.__sketchpadGetState().strokes;const src=S.filter(s=>s.radial)["+str(k)+"];const o=[src,...S.filter(c=>c.radialOf===src.id)][1];const c=document.getElementById('canvas').getBoundingClientRect();const p=o.points[Math.floor(o.points.length/2)];return [p.x,p.y,c.left,c.top,c.width,c.height,document.getElementById('canvas').width,document.getElementById('canvas').height]})()")
    return pt[2]+pt[0]*pt[4]/pt[6],pt[3]+pt[1]*pt[5]/pt[7]
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(460,250);pg.mouse.down();pg.mouse.move(540,420,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(490,330);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(500)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    pg.locator('#pathEditBar button:has-text("Fill:")').first.click();pg.wait_for_timeout(400)
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn')&&0")
    pg.mouse.click(490,330);pg.wait_for_timeout(300);print('select original petal',sel(pg))
    js("document.getElementById('qaDup').click()");pg.wait_for_timeout(500);print('after dup',sel(pg))
    # move the duplicate far away by drag in box
    js("window.__sketchpadInternals().segVerBump()");pg.wait_for_timeout(200)
    box=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    pg.mouse.move(box[0],box[1]);pg.mouse.down();pg.mouse.move(box[0]+330,box[1]+60,steps=10);pg.mouse.up();pg.wait_for_timeout(500);print('after move',sel(pg))
    x,y=scr(pg,0);print('tap original petal at',round(x),round(y))
    pg.mouse.click(x,y);pg.wait_for_timeout(400);print(' ->',sel(pg))
    x,y=scr(pg,1);print('tap copy petal at',round(x),round(y))
    pg.mouse.click(x,y);pg.wait_for_timeout(400);print(' ->',sel(pg))
    pg.mouse.click(x,y);pg.wait_for_timeout(400);print(' again ->',sel(pg))
    for step in ('undo','undo','redo','redo','undo'):
        js(f"document.getElementById('{step}Btn').click()");pg.wait_for_timeout(500)
        n=js(ST+".strokes.filter(s=>s.radial).length")
        x,y=scr(pg,0);pg.mouse.click(x,y);pg.wait_for_timeout(300)
        print(step,'flowers',n,'tap original ->',sel(pg),flush=True)
    # tap with Finger On/Off toggles, quick-move mode
    js("document.getElementById('qaMove').click()");pg.wait_for_timeout(200)
    x,y=scr(pg,0);pg.mouse.click(x,y);pg.wait_for_timeout(300);print('quickMove tap ->',sel(pg))
    js("document.getElementById('qaSelect').click()");pg.wait_for_timeout(200)
    pg.mouse.click(200,700);pg.wait_for_timeout(300)
    x,y=scr(pg,0);pg.mouse.click(x,y);pg.wait_for_timeout(300);print('select tool tap ->',sel(pg))
    print('errors',errs);b.close()
