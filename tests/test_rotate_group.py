# Rotate & Repeat auto-group: Make groups the flower; tap = whole flower, double-tap = one petal; links and group are independent.
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
import common as t500
from playwright.sync_api import sync_playwright
ST="window.__sketchpadGetState()"
res=[]
def ok(n,c,extra=''):
    res.append(bool(c));print(('PASS ' if c else 'FAIL ')+n,extra)
FL="""(()=>{const S=window.__sketchpadGetState().strokes;const srcs=S.filter(s=>s.radial);
 return srcs.map(src=>{const R=src.radial;const pet=[src,...S.filter(c=>c.radialOf===src.id)];
  const d=pet.map(o=>{const n=o.points.length;let x=0,y=0;o.points.forEach(p=>{x+=p.x;y+=p.y});return Math.hypot(x/n-R.cx,y/n-R.cy)});
  return {cx:Math.round(R.cx),cy:Math.round(R.cy),petals:pet.length,spread:Math.round((Math.max(...d)-Math.min(...d))*10)/10,gids:[...new Set(pet.map(o=>o.groupId||''))],fills:pet.filter(o=>S.find(f=>f.fillOf===o.id)).length}})})()"""
with sync_playwright() as p:
    b,pg,errs=t500.boot(p);js=pg.evaluate
    # an unrelated group first (two plain strokes)
    for (x0,y0,x1,y1) in [(300,300,380,330),(300,380,380,420)]:
        pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x1,y1,steps=6);pg.mouse.up();pg.wait_for_timeout(250)
    other=js(ST+".strokes.map(s=>s.id)")
    js("(ids)=>window.__sketchpadInternals().setMulti(ids,[],null)",other);js("document.getElementById('editModeBtn')&&0");
    js("document.getElementById('groupBtn').click()");pg.wait_for_timeout(300)
    og=js(ST+".strokes.map(s=>s.groupId||'')");ok('setup: other group made',len(set(og))==1 and og[0])
    js("window.__sketchpadInternals().setMulti([],[],null)")
    # flower
    js("document.querySelector('.shape-btn[data-shape=teardrop]').click()");pg.wait_for_timeout(200)
    pg.mouse.move(560,250);pg.mouse.down();pg.mouse.move(660,450,steps=8);pg.mouse.up();pg.wait_for_timeout(400)
    js("document.getElementById('editModeBtn').click()");pg.wait_for_timeout(300)
    pg.mouse.click(610,350);pg.wait_for_timeout(400)
    js("document.getElementById('openRotatePanelBtn').click()");pg.wait_for_timeout(400)
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(600)
    r=js(FL);print(r)
    ok('Make: one flower of 6 petals, all in ONE group',len(r)==1 and r[0]['petals']==6 and len(r[0]['gids'])==1 and r[0]['gids'][0]!='',r)
    ok('Make: the petal being edited stays selected (Edit Path / Fill still work)',js("!!window.__sketchpadGetState().selectedStrokeId"))
    ok('other group untouched',js(ST+".strokes.filter(s=>!s.radial&&!s.radialOf).map(s=>s.groupId||'')").count(og[0])==2)
    flowerG=r[0]['gids'][0]
    js("document.getElementById('rotatePanel').style.display='none'")
    # deselect, then tap a petal
    js("(()=>{const I=window.__sketchpadInternals();I.setMulti([],[],null);I.syncStrokeSelectionUI();I.segVerBump();})()");pg.mouse.click(1050,700);pg.wait_for_timeout(500)
    pts=js("(()=>{const S=window.__sketchpadGetState().strokes.filter(s=>s.radialOf||s.radial);return S.map(s=>{const p=s.points[Math.floor(s.points.length/2)];return [p.x,p.y,s.id]})})()")
    # screen position of canvas point: use bounding box maths
    pos=js("""(pts)=>{const c=document.getElementById('canvas').getBoundingClientRect();const k=c.width/1800;return pts.map(p=>[c.left+p[0]*k,c.top+p[1]*k])}""",pts)
    print('state',js("(()=>{const g=document.getElementById('groupBox');const m=window.__sketchpadGetState().multiSel;return [g.style.display,getComputedStyle(g).display,JSON.stringify(m)&&JSON.stringify(m).slice(0,80),window.__sketchpadGetState().selectedStrokeId]})()"))
    print('tap at',pos[1],js('([x,y])=>{const e=document.elementFromPoint(x,y);return e.id||e.className}',pos[1]))
    pg.mouse.click(pos[1][0],pos[1][1]);pg.wait_for_timeout(500)
    m=js("(()=>{const s=window.__sketchpadGetState();return {g:s.multiSel&&s.multiSel.groupId,n:s.multiSel&&s.multiSel.strokeIds.length,sel:s.selectedStrokeId}})()")
    ok('single tap on a petal selects the WHOLE flower',m['g']==flowerG and m['n']==6,m)
    # double tap on a petal -> one petal
    pg.mouse.click(pos[1][0],pos[1][1]);pg.wait_for_timeout(120);pg.mouse.click(pos[1][0],pos[1][1]);pg.wait_for_timeout(500)
    m=js("(()=>{const s=window.__sketchpadGetState();return {g:s.multiSel&&s.multiSel.groupId,sel:s.selectedStrokeId,inside:s.groupInsideId}})()")
    ok('double-tap did NOT duplicate anything',len(js(FL))==1 and js(ST+".strokes.length")==6+2,js(ST+".strokes.length"))
    ok('double-tap selects just one petal',m['sel'] and not m['g'],m)
    # edit source petal path -> copies follow (links intact)
    srcid=js(ST+".strokes.find(s=>s.radial).id")
    js("(id)=>{const S=window.__sketchpadGetState();}",srcid)
    before=js(FL)
    # turn the whole group 30 degrees through the group panel (reselect group)
    js("(()=>{const I=window.__sketchpadInternals();const S=window.__sketchpadGetState().strokes.filter(s=>s.radial||s.radialOf).map(s=>s.id);I.setMulti(S,[],%s)})()"%repr(flowerG).replace("'",'"'))
    pg.wait_for_timeout(200)
    js("document.getElementById('grpTurnDeg').value=30");js("document.getElementById('grpTurnBtn').click()");pg.wait_for_timeout(400)
    r2=js(FL);ok('turn whole group: still one even flower, centre kept',len(r2)==1 and r2[0]['petals']==6 and r2[0]['spread']<1.5 and abs(r2[0]['cx']-before[0]['cx'])<3,r2)
    # duplicate keeps group + links
    js("document.getElementById('tbDupBtn').click()");pg.wait_for_timeout(700)
    r3=js(FL);print(r3)
    ok('duplicate: two even flowers of 6',len(r3)==2 and all(x['petals']==6 and x['spread']<1.5 and len(x['gids'])==1 and x['gids'][0] for x in r3),r3)
    ok('duplicate: its OWN new group',len(r3)==2 and r3[0]['gids'][0]!=r3[1]['gids'][0])
    ok('duplicate: other group still 2 members',js(ST+".strokes.filter(s=>!s.radial&&!s.radialOf).map(s=>s.groupId||'')").count(og[0])==2)
    ok('duplicate selected as one group',js("(()=>{const m=window.__sketchpadGetState().multiSel;return !!(m&&m.groupId&&m.strokeIds.length===6)})()"))
    # ungroup keeps repeat links
    js("document.getElementById('ungroupBtn').click()");pg.wait_for_timeout(400)
    r4=js(FL);ok('ungroup keeps links (petals still linked, no group)',len(r4)==2 and all(x['petals']==6 for x in r4) and any(x['gids']==[''] for x in r4),r4)
    # regroup the copy then unlink: group stays, links go
    ids=js("(()=>{const S=window.__sketchpadGetState().strokes;const src=S.filter(s=>s.radial).pop();return S.filter(s=>s.id===src.id||s.radialOf===src.id).map(s=>s.id)})()")
    js("(ids)=>{const I=window.__sketchpadInternals();I.setMulti(ids,[],null);I.syncStrokeSelectionUI();I.segVerBump();}",ids);pg.wait_for_timeout(500);print('groupBtn disabled',js("document.getElementById('groupBtn').disabled"),len(ids));js("document.getElementById('groupBtn').click()");pg.wait_for_timeout(300)
    js("document.getElementById('repeatUnlinkBtn').click()");pg.wait_for_timeout(400)
    r5=js(ST+".strokes.filter(s=>ids.includes?0:0).length") if False else js("(ids)=>window.__sketchpadGetState().strokes.filter(s=>ids.includes(s.id)).map(s=>[!!s.radial,!!s.radialOf,s.groupId||''])",ids)
    ok('unlink: no repeat links left, still grouped',all((not a) and (not b_) and g for a,b_,g in r5) and len(set(x[2] for x in r5))==1,r5)
    pg.screenshot(path='rotgroup.png');print(errs);ok('no page errors',not errs)
    print('ALL PASS' if all(res) else 'SOME FAILED');b.close()
