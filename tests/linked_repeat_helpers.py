from playwright.sync_api import sync_playwright
import common as t500, json, math
CHECK="""()=>{const S=window.__sketchpadGetState().strokes;const src=S.find(s=>s.radial);if(!src)return 'no source';
 const R=src.radial;const kids=S.filter(c=>c.radialOf===src.id);let worst=0,bad=[];
 kids.forEach(c=>{const a=R.step*c.radialK*Math.PI/180,co=Math.cos(a),si=Math.sin(a);
   let w=0;if(c.points.length!==src.points.length){bad.push(['len',c.radialK,c.points.length,src.points.length]);return;}
   src.points.forEach((p,i)=>{const x=R.cx+(p.x-R.cx)*co-(p.y-R.cy)*si,y=R.cy+(p.x-R.cx)*si+(p.y-R.cy)*co;w=Math.max(w,Math.hypot(x-c.points[i].x,y-c.points[i].y));});
   worst=Math.max(worst,w);if(w>1)bad.push([c.radialK,Math.round(w)]);});
 return {kids:kids.length,worst:Math.round(worst*10)/10,bad,shapeOnSrc:!!src.shape,nodesOnSrc:!!src.nodes,nodesOnKid:kids.map(k=>!!k.nodes),shapeOnKid:kids.map(k=>!!k.shape),pivot:[Math.round(R.cx),Math.round(R.cy)]}}"""
def editsrc(pg,dx,dy,idx=0):
    js=pg.evaluate
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    r=js("(()=>{const e=document.getElementById('pathNodeOverlay').children[%d].getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]})()"%idx)
    pg.mouse.move(r[0],r[1]);pg.mouse.down();pg.mouse.move(r[0]+dx,r[1]+dy,steps=8);pg.mouse.up();pg.wait_for_timeout(300)
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(500)
if __name__=='__main__':
  with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    editsrc(pg,-50,-70)
    S=js("window.__sketchpadGetState().strokes.map(s=>[s.id.slice(0,4),!!s.shape,!!s.nodes,s.points.length])");print('after edit',S)
    js("(()=>{document.getElementById('repeatCount').value=6;document.getElementById('repeatCount').dispatchEvent(new Event('input'));})()")
    print('angle',js("document.getElementById('repeatAngle').value"))
    print('sel',js("window.__sketchpadGetState().selectedStrokeId"))
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(500)
    print('make',js(CHECK))
    pg.screenshot(path='t501a.png')
    # edit source again (select source first)
    sid=js("window.__sketchpadGetState().strokes.find(s=>s.radial).id")
    js("(id)=>{const I=window.__sketchpadInternals();}",sid)
    t500.pick_petal(pg);pg.wait_for_timeout(400)
    print('sel2',js("(()=>{const s=window.__sketchpadGetState();const x=s.strokes.find(q=>q.id===s.selectedStrokeId);return x&&[!!x.radial,x.radialOf]})()"))
    editsrc(pg,30,60,3)
    print('after 2nd edit',js(CHECK))
    pg.screenshot(path='t501b.png')
    print(errs);b.close()
