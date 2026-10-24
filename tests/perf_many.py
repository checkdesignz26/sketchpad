from playwright.sync_api import sync_playwright
import common as t500
ST="window.__sketchpadGetState()"
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
    pg.mouse.click(610,350);pg.wait_for_timeout(300)
    for n in range(6):
        t=js("(()=>{const t=performance.now();document.getElementById('qaDup').click();return Math.round(performance.now()-t)})()");pg.wait_for_timeout(400)
        js("window.__sketchpadInternals().segVerBump()")
        c=js(ST+".strokes.length")
        # tap timing: pointerdown on empty canvas area -> measure main thread blocking via a rAF probe
        js("window.__sketchpadInternals().setMulti([],[],null);window.__sketchpadInternals().syncStrokeSelectionUI()");pg.wait_for_timeout(200)
        t0=js("performance.now()");pg.mouse.click(300,300);
        t1=js("performance.now()")
        pg.wait_for_timeout(200)
        print(f'dup#{n+1}: strokes={c} dup={t}ms tap-roundtrip={round(t1-t0)}ms sel={bool(js(ST+".selectedStrokeId"))}',flush=True)
        # reselect all family for next duplicate
        ids=js(ST+".strokes.map(s=>s.id)");js(f"window.__sketchpadInternals().setMulti({ids},[],null)")
    print(errs);b.close()
