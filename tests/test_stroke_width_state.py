from playwright.sync_api import sync_playwright
import common as t500
RD="""()=>{const e=document.getElementById('tbSizeNum');const s=window.__sketchpadGetState();return {val:e.value,ph:e.placeholder,sizes:s.strokes.map(x=>x.settings.size),brush:document.getElementById('brushSize').value}}"""
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    def setsize(v):
        pg.locator('#tbSizeNum').fill(str(v));pg.locator('#tbSizeNum').press('Enter');pg.locator('#tbSizeNum').blur();pg.wait_for_timeout(200)
    def draw(x0,y0,x1,y1):
        js("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(150)
        js("document.querySelector('.shape-btn[data-shape=ellipse]').click()");pg.wait_for_timeout(150)
        pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
    def deselect():
        js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(200);js("document.getElementById('strokeActionsDoneBtn').click()");pg.wait_for_timeout(300)
    setsize(4);draw(300,250,450,400);deselect();setsize(12);draw(600,250,750,400)
    print('two drawn',js(RD))
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(200)
    js("(()=>{const I=window.__sketchpadInternals();I.setMulti(I.strokes.map(s=>s.id),[],null);I.syncStrokeSelectionUI();})()");pg.wait_for_timeout(300)
    print('multi mixed',js(RD))
    setsize(7);print('multi set 7',js(RD))
    js("(()=>{const I=window.__sketchpadInternals();I.setMulti(I.strokes.map(s=>s.id),[],null);I.syncStrokeSelectionUI();})()");pg.wait_for_timeout(300)
    print('multi same',js(RD))
    deselect();print('deselected',js(RD))
    pg.locator('#undoBtn').click();pg.wait_for_timeout(300);print('undo',js(RD))
    print(errs);b.close()
