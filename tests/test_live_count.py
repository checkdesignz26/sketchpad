from playwright.sync_api import sync_playwright
import common as t500, linked_repeat_helpers as t501, test_flower_undo_save as t505
ST="(()=>{const S=window.__sketchpadGetState().strokes;const src=S.find(s=>s.radial);return src?{total:S.length,kids:S.filter(c=>c.radialOf===src.id).length,step:src.radial.step,n:src.radial.n,even:src.radial.even,field:document.getElementById('repeatCount').value,angle:document.getElementById('repeatAngle').value}:{total:S.length}})()"
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    t501.editsrc(pg,-50,-70)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(400)
    print('6',js(ST),js(t501.CHECK)['worst'])
    for lab,btn in (('7','repeatPlus'),('8','repeatPlus'),('5','repeatMinus')):
        if lab=='5':
            pg.locator('#repeatMinus').click();pg.wait_for_timeout(200);pg.locator('#repeatMinus').click();pg.wait_for_timeout(200);pg.locator('#repeatMinus').click()
        else: pg.locator('#'+btn).click()
        pg.wait_for_timeout(300);c=js(t501.CHECK);print(lab,js(ST),'worst',c['worst'])
    # custom angle
    pg.locator('#repeatEven').uncheck();js("(()=>{const a=document.getElementById('repeatAngle');a.value=40;a.dispatchEvent(new Event('input',{bubbles:true}));a.dispatchEvent(new Event('change',{bubbles:true}))})()");pg.wait_for_timeout(300)
    print('custom 40',js(ST),js(t501.CHECK)['worst'])
    pg.locator('#repeatPlus').click();pg.wait_for_timeout(300);print('+1 keeps custom',js(ST),js(t501.CHECK)['worst'])
    pg.locator('#repeatEven').check();pg.wait_for_timeout(300);print('even again',js(ST))
    # Edit Path with panel open
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(500)
    print('panel open during edit path',js("document.getElementById('rotatePanel').style.display"),'marker',js("document.getElementById('pivotMarker').style.display"))
    r=js("(()=>{const e=document.getElementById('pathNodeOverlay').children[3].getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]})()")
    s0=js(t505.SNAP)
    pg.mouse.move(r[0],r[1]);pg.mouse.down();pg.mouse.move(r[0]+40,r[1]+50,steps=8);pg.wait_for_timeout(300)
    print('dragged: kids moved',t505.dev(s0,js(t505.SNAP)))
    pg.mouse.up()
    pg.locator('#repeatPlus').click();pg.wait_for_timeout(500);print('count+1 during edit path',js(ST))
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(500)
    c=js(t501.CHECK);print('after Done',js(ST),'worst',c['worst'],'bad',c['bad'])
    snap=js(t505.SNAP)
    pg.locator('#undoBtn').click();pg.wait_for_timeout(400);print('undo',js(ST),'worst',js(t501.CHECK)['worst'])
    pg.locator('#redoBtn').click();pg.wait_for_timeout(400);print('redo',js(ST),t505.dev(snap,js(t505.SNAP)))
    pg.wait_for_timeout(2500);pg.reload();pg.wait_for_timeout(2500)
    print('reload',js(ST),t505.dev(snap,js(t505.SNAP)))
    __import__("common").pick_petal(pg);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    print('panel reflects saved flower',js("[document.getElementById('repeatCount').value,document.getElementById('repeatAngle').value,document.getElementById('repeatEven').checked]"))
    pg.locator('#repeatMinus').click();pg.wait_for_timeout(300);print('minus after reload',js(ST),js(t501.CHECK)['worst'])
    print(errs);b.close()
