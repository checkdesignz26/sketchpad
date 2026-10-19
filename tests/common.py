from playwright.sync_api import sync_playwright
import json,math
def boot(p):
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':1180,'height':820}).new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8790/index.html'); pg.wait_for_timeout(2000)
    pg.locator('button:has-text("New Project"):visible').first.click(); pg.wait_for_timeout(600)
    pg.locator('button:has-text("Start drawing")').click(); pg.wait_for_timeout(2500)
    return b,pg,errs
def deselect(pg):
    # leave and re-enter Edit mode: clears any selection / group-edit state
    pg.evaluate("document.getElementById('drawModeBtn').click()");pg.wait_for_timeout(250)
    pg.evaluate("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
def pick_petal(pg,x=None,y=None):
    # a flower made with Make copies is one group: tap = whole flower, double-tap = one petal. Clear any selection, then double-tap the middle of the source petal.
    if x is None:
        x,y=pg.evaluate("""()=>{const S=window.__sketchpadGetState().strokes;const s=S.find(q=>q.radial)||S[0];let X=0,Y=0;s.points.forEach(q=>{X+=q.x;Y+=q.y});const p={x:X/s.points.length,y:Y/s.points.length};const r=document.getElementById('canvas').getBoundingClientRect();return [r.left+p.x*r.width/1800,r.top+p.y*r.height/1800]}""")
    deselect(pg);pg.mouse.click(x,y);pg.wait_for_timeout(150);pg.mouse.click(x,y);pg.wait_for_timeout(500)
if __name__=='__main__':
  with sync_playwright() as p:
    b,pg,errs=boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    print(js("window.__sketchpadGetState().strokes.map(s=>[s.shape&&s.shape.type,s.closed,s.points.length,!!s.nodes])"))
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    print('sel',js("window.__sketchpadGetState().selectedStrokeId"))
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(500)
    print('nodes',js("document.getElementById('pathNodeOverlay').children.length"), js("[...document.getElementById('pathNodeOverlay').children].slice(0,4).map(e=>e.className+':'+Math.round(e.getBoundingClientRect().x)+','+Math.round(e.getBoundingClientRect().y))"))
    pg.screenshot(path='t500a.png')
    print(errs);b.close()
