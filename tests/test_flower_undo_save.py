from playwright.sync_api import sync_playwright
import common as t500, linked_repeat_helpers as t501, json
SNAP="window.__sketchpadGetState().strokes.map(s=>({k:s.radial?'src':(s.radialOf?'kid'+s.radialK:'-'),p:s.points.map(q=>[q.x,q.y]),fill:s.fillColor||null,w:s.settings&&s.settings.size}))"
def dev(a,b):
    if len(a)!=len(b):return 'count %d vs %d'%(len(a),len(b))
    m=0
    for x,y in zip(a,b):
        if len(x['p'])!=len(y['p']):return 'pts %s %d vs %d'%(x['k'],len(x['p']),len(y['p']))
        for p,q in zip(x['p'],y['p']):m=max(m,abs(p[0]-q[0]),abs(p[1]-q[1]))
        if x['fill']!=y['fill']:return 'fill differs'
    return 'maxdev %.2f'%m
if __name__=='__main__':
  with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    t501.editsrc(pg,-50,-70)
    js("(()=>{document.getElementById('repeatCount').value=6;document.getElementById('repeatCount').dispatchEvent(new Event('input'));})()")
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(600)
    made=js(SNAP)
    t500.pick_petal(pg);pg.wait_for_timeout(400)
    t501.editsrc(pg,30,60,3)
    e2=js(SNAP);print('edit2 vs made',dev(made,e2),js(t501.CHECK)['worst'])
    pg.locator('#undoBtn').click();pg.wait_for_timeout(500)
    u=js(SNAP);print('undo vs made',dev(made,u),'| check',js(t501.CHECK)['worst'] if u[0]['k']=='src' else '')
    pg.locator('#redoBtn').click();pg.wait_for_timeout(500)
    r=js(SNAP);print('redo vs edit2',dev(e2,r),'| check',js(t501.CHECK)['worst'])
    pg.wait_for_timeout(2500);pg.reload();pg.wait_for_timeout(2500)
    print('after reload',dev(e2,js(SNAP)))
    t500.pick_petal(pg);pg.wait_for_timeout(500)
    print('sel after reload',js("(()=>{const s=window.__sketchpadGetState();const x=s.strokes.find(q=>q.id===s.selectedStrokeId);return x&&[!!x.radial,x.radialOf||null]})()"))
    before=js(SNAP)
    t501.editsrc(pg,-40,40,2)
    after=js(SNAP);print('edit after reload vs before',dev(before,after),'| check',js(t501.CHECK)['worst'],js(t501.CHECK)['kids'])
    print(errs);b.close()
