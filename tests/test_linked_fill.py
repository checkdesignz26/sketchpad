from playwright.sync_api import sync_playwright
import common as t500, linked_repeat_helpers as t501, test_flower_undo_save as t505
FILL="""(()=>{const S=window.__sketchpadGetState().strokes;const src=S.find(s=>s.radial);if(!src)return 'no flower';
 const petals=[src,...S.filter(c=>c.radialOf===src.id)];const out=[];
 petals.forEach(o=>{const f=S.find(x=>x.fillOf===o.id);const on=!!(o.fill&&o.fill.on);
   let dev=null;if(f){const g=(o.nodes||o.points);const pts=f.points;dev=pts.length;}
   out.push([o.radialK||0,on,f?f.fillColor:null,dev])});
 return out})()"""
GEOM="""(()=>{const S=window.__sketchpadGetState().strokes;const src=S.find(s=>s.radial);
 const petals=[src,...S.filter(c=>c.radialOf===src.id)];let worst=0,missing=0;
 petals.forEach(o=>{const f=S.find(x=>x.fillOf===o.id);if(!f){missing++;return;}
   // fill outline must lie on the petal outline (every fill point within 1.5px of some outline point)
   const op=o.points;f.points.forEach(p=>{let m=1e9;for(const q of op){const d=Math.hypot(p.x-q.x,p.y-q.y);if(d<m)m=d;}worst=Math.max(worst,m)})});
 return {petals:petals.length,missing,worst:Math.round(worst*10)/10,fills:S.filter(x=>x.fillOf).length}})()"""
def fillbtn(pg): return pg.locator('#pathEditBar button:has-text("Fill:")').first
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(500)
    print('panel+editpath',js("document.getElementById('rotatePanel').style.display"))
    fillbtn(pg).click();pg.wait_for_timeout(500)
    print('FILL ON  ',js(GEOM),[x[1:3] for x in js(FILL)])
    # drag node live, check fills while dragging
    r=js("(()=>{const e=document.getElementById('pathNodeOverlay').children[3].getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]})()")
    pg.mouse.move(r[0],r[1]);pg.mouse.down();pg.mouse.move(r[0]+40,r[1]+50,steps=8);pg.wait_for_timeout(300)
    print('MID-DRAG ',js(GEOM))
    pg.mouse.up();pg.wait_for_timeout(300)
    pg.locator('#repeatPlus').click();pg.wait_for_timeout(300);pg.locator('#repeatPlus').click();pg.wait_for_timeout(300)
    print('COUNT 8  ',js(GEOM))
    # colour change via fill colour input in Edit Path panel
    js("(()=>{const ci=[...document.querySelectorAll('#pathEditBar input[type=color]')].pop();ci.value='#ff3366';ci.dispatchEvent(new Event('input',{bubbles:true}));ci.dispatchEvent(new Event('change',{bubbles:true}))})()");pg.wait_for_timeout(400)
    print('COLOUR   ',js(GEOM),set(x[2] for x in js(FILL)))
    pg.screenshot(path='fill_a.png')
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(500)
    print('AFTER DONE',js(GEOM),set(x[2] for x in js(FILL)))
    pg.wait_for_timeout(2500);pg.reload();pg.wait_for_timeout(2500)
    print('RELOADED ',js(GEOM),set(x[2] for x in js(FILL)))
    pg.locator('#undoBtn').click();pg.wait_for_timeout(400)
    print('UNDO     ',js(GEOM))
    pg.locator('#redoBtn').click();pg.wait_for_timeout(400)
    t500.pick_petal(pg);pg.wait_for_timeout(300)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    fillbtn(pg).click();pg.wait_for_timeout(500)
    print('FILL OFF ',js(GEOM),js(FILL))
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(300)
    print(errs);b.close()
