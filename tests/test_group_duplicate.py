from playwright.sync_api import sync_playwright
import common as t500
def ok(n,c,extra=''): print(('PASS ' if c else 'FAIL ')+n,extra)
ST="window.__sketchpadGetState()"
FL="""(()=>{const S=window.__sketchpadGetState().strokes;const srcs=S.filter(s=>s.radial);
 return srcs.map(src=>{const R=src.radial;const pet=[src,...S.filter(c=>c.radialOf===src.id)];
  const d=pet.map(o=>{const n=o.points.length;let x=0,y=0;o.points.forEach(p=>{x+=p.x;y+=p.y});return Math.hypot(x/n-R.cx,y/n-R.cy)});
  const fills=pet.filter(o=>S.find(f=>f.fillOf===o.id)).length;
  return {cx:Math.round(R.cx),cy:Math.round(R.cy),petals:pet.length,spread:Math.round((Math.max(...d)-Math.min(...d))*10)/10,fills}})})()"""
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
    print('before',js(FL))
    ids=js(ST+".strokes.map(s=>s.id)")
    js(f"window.__sketchpadInternals().setMulti({ids},[],null)");pg.wait_for_timeout(200)
    js("document.getElementById('tbDupBtn').click()");pg.wait_for_timeout(600)
    r=js(FL);print('after dup',r)
    ok('two flowers',len(r)==2)
    ok('copy flower even',all(x['spread']<1.5 and x['petals']==6 and x['fills']==6 for x in r),r)
    ok('centre moved by 40',len(r)==2 and abs(r[1]['cx']-r[0]['cx'])==40)
    ids2=js(ST+".multiSel.strokeIds");print('selected',len(ids2))
    # move copy via drag of the group box
    js("window.__sketchpadInternals().rebuildAllLayers&&window.__sketchpadInternals().rebuildAllLayers()")
    pg.mouse.move(610,400);pg.mouse.down();pg.mouse.move(850,520,steps=8);pg.mouse.up();pg.wait_for_timeout(500)
    r=js(FL);print('after move',r)
    ok('still even after move',all(x['spread']<1.5 and x['petals']==6 and x['fills']==6 for x in r),r)
    for i in (1,2,3):
        js("document.getElementById('undoBtn').click()");pg.wait_for_timeout(400)
        print('undo',i,js(FL),js(ST+".histLen"))
    pg.screenshot(path='dup.png');print(errs);b.close()
