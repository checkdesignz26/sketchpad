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
    t500.pick_petal(pg);pg.wait_for_timeout(300)
    print('sel',js(ST+".selectedStrokeId"),js(ST+".multiSel?"+ST+".multiSel.strokeIds.length:0"))
    js("document.getElementById('qaDup').click()");pg.wait_for_timeout(600)
    r=js(FL);print(r)
    ok('whole flower copied',len(r)==2 and all(x['petals']==6 for x in r))
    print('multi',js(ST+".multiSel?"+ST+".multiSel.strokeIds.length:0"),'box',js("(()=>{const b=document.getElementById('groupBox');const r=b.getBoundingClientRect();return [b.style.display,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]})()"))
    js("window.__sketchpadInternals().segVerBump()");pg.wait_for_timeout(300)
    box=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    for label,mv in (('mouse drag',None),):
        pg.mouse.move(box[0],box[1]);pg.mouse.down();pg.mouse.move(box[0]+150,box[1]+90,steps=10);pg.mouse.up();pg.wait_for_timeout(500)
        print(label,js(FL))
    # touch-style drag via pointer events with pointerType touch
    box=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    js("""(b)=>{const el=document.elementFromPoint(b[0],b[1]);window.__hit=el&&(el.id||el.className||el.tagName)}""",box)
    print('element under box centre',js("window.__hit"))
    print(errs);b.close()
