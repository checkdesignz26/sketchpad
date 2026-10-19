from playwright.sync_api import sync_playwright
import json,math
def boot(p):
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':1180,'height':820}).new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8790/index.html'); pg.wait_for_timeout(2000)
    pg.locator('button:has-text("New Project"):visible').first.click(); pg.wait_for_timeout(600)
    pg.locator('button:has-text("Start drawing")').click(); pg.wait_for_timeout(2500)
    return b,pg,errs
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
