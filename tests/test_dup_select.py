from playwright.sync_api import sync_playwright
import common as t500
ST="window.__sketchpadGetState()"
def ok(n,c,extra=''): print(('PASS ' if c else 'FAIL ')+n,extra)
FL="""(()=>{const S=window.__sketchpadGetState().strokes;return S.filter(s=>s.radial).map(src=>{const R=src.radial;return {cx:Math.round(R.cx),cy:Math.round(R.cy),petals:1+S.filter(c=>c.radialOf===src.id).length,fills:S.filter(f=>f.fillOf&&(f.fillOf===src.id||S.find(c=>c.id===f.fillOf&&c.radialOf===src.id))).length}})})()"""
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(500)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    pg.locator('#pathEditBar button:has-text("Fill:")').first.click();pg.wait_for_timeout(400)
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(400)
    # select ONE petal, duplicate from quick actions
    pg.mouse.click(610,350);pg.wait_for_timeout(300)
    print('sel',js(ST+".selectedStrokeId"),js(ST+".multiSel?"+ST+".multiSel.strokeIds.length:0"))
    js("document.getElementById('qaDup').click()");pg.wait_for_timeout(600)
    r=js(FL);print(r)
    ok('whole flower copied',len(r)==2 and all(x['petals']==6 for x in r))
    js("window.__sketchpadInternals().setMulti([],[],null);window.__sketchpadInternals().syncStrokeSelectionUI();window.__sketchpadInternals().segVerBump()");pg.wait_for_timeout(300)
    pt=js("(()=>{const S=window.__sketchpadGetState().strokes;const src=S.filter(s=>s.radial)[1];const o=[src,...S.filter(c=>c.radialOf===src.id)][1];const c=document.getElementById('canvas').getBoundingClientRect();const p=o.points[Math.floor(o.points.length/2)];return [p.x,p.y,c.left,c.top,c.width,c.height,document.getElementById('canvas').width,document.getElementById('canvas').height]})()")
    sx=pt[2]+pt[0]*pt[4]/pt[6];sy=pt[3]+pt[1]*pt[5]/pt[7]
    pg.mouse.click(sx,sy);pg.wait_for_timeout(400)
    pg.wait_for_timeout(900)
    print('1st tap: single',js(ST+".selectedStrokeId")!=None)
    pg.mouse.move(sx,sy);pg.mouse.down();pg.mouse.move(sx+20,sy+10,steps=4);pg.mouse.up();pg.wait_for_timeout(400)
    n=js(ST+".multiSel?"+ST+".multiSel.strokeIds.length:0");ok('re-tap/drag petal selects whole flower',n==12,n)
    box=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    pg.mouse.move(box[0],box[1]);pg.mouse.down();pg.mouse.move(box[0]+150,box[1]+90,steps=10);pg.mouse.up();pg.wait_for_timeout(500)
    r=js(FL);print(r);ok('flower moved as one',abs(r[1]['cx']-921)>100 and all(x['petals']==6 and x['fills']==6 for x in r),r)
    print(errs);b.close()
