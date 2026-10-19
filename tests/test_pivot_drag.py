from playwright.sync_api import sync_playwright
import common as t500, linked_repeat_helpers as t501, test_flower_undo_save as t505,json
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    t501.editsrc(pg,-50,-70)
    # counts/angles
    for n,ang in ((3,120),(4,90),(5,72),(6,60),(8,45),(12,30)):
        js("(n)=>{const c=document.getElementById('repeatCount');c.value=n;c.dispatchEvent(new Event('input'))}",n)
        a=js("document.getElementById('repeatAngle').value")
        js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(300)
        c=js(t501.CHECK);tot=js("window.__sketchpadGetState().strokes.length")
        print(n,'angle field',a,'strokes',tot,'worst',c['worst'],'bad',c['bad'])
    # live follow during drag: 6 petals, drag a node and read kids mid-drag
    js("(n)=>{const c=document.getElementById('repeatCount');c.value=n;c.dispatchEvent(new Event('input'))}",6)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(300)
    t500.pick_petal(pg);pg.wait_for_timeout(300)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    r=js("(()=>{const e=document.getElementById('pathNodeOverlay').children[3].getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]})()")
    s0=js(t505.SNAP)
    pg.mouse.move(r[0],r[1]);pg.mouse.down();pg.mouse.move(r[0]+40,r[1]+50,steps=10);pg.wait_for_timeout(400)
    s1=js(t505.SNAP);print('MID-DRAG (not committed) kids moved vs before:',t505.dev(s0,s1))
    pg.mouse.up();pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(500)
    s2=js(t505.SNAP);print('after Done vs mid-drag',t505.dev(s1,s2),js(t501.CHECK)['worst'])
    # pivot drag
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(500)
    mk="(()=>{const m=document.getElementById('pivotMarker');const b=m.getBoundingClientRect();return [m.style.display,b.x+b.width/2,b.y+b.height/2,b.width]})()"
    print('marker',js(mk))
    d,mx,my,w=js(mk)
    c0=js(t501.CHECK)['pivot']
    pg.mouse.move(mx,my);pg.mouse.down();pg.mouse.move(mx+30,my+120,steps=10);pg.wait_for_timeout(300)
    print('mid-drag worst',js(t501.CHECK)['worst'],'pivot',js(t501.CHECK)['pivot'])
    pg.mouse.up();pg.wait_for_timeout(400)
    c=js(t501.CHECK);print('pivot before',c0,'after',c['pivot'],'worst',c['worst'],'bad',c['bad'])
    print('marker after',js(mk))
    pg.screenshot(path='t520a.png')
    pg.locator('#undoBtn').click();pg.wait_for_timeout(400);c=js(t501.CHECK);print('undo pivot',c['pivot'],c['worst'])
    errs and print(errs);b.close()
