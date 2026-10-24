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
    js("document.getElementById('repeatCount').value=12;document.getElementById('repeatCount').dispatchEvent(new Event('change',{bubbles:true}))")
    js("document.getElementById('repeatMakeBtn').click()");pg.wait_for_timeout(500)
    js("document.getElementById('editPathBtn').click()");pg.wait_for_timeout(400)
    pg.locator('#pathEditBar button:has-text("Fill:")').first.click();pg.wait_for_timeout(400)
    pg.locator('#pathEditDoneTopBtn').click();pg.wait_for_timeout(400)
    cdp=pg.context.new_cdp_session(pg);cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    def timed(label,expr):
        t=js("(()=>{const t=performance.now();"+expr+";return Math.round(performance.now()-t)})()");print(label,t,'ms');return t
    js("(()=>{const b=document.getElementById('tilingBtn');if(b&&/Off/.test(b.textContent))b.click()})()");pg.wait_for_timeout(400);print('tiling',js("document.getElementById('tilingBtn').textContent"))
    print('strokes',js(ST+".strokes.length"))
    pg.mouse.click(610,350);pg.wait_for_timeout(300)
    cdp.send('Profiler.enable');cdp.send('Profiler.start')
    timed('dup #1 (flower)',"document.getElementById('qaDup').click()")
    pg.wait_for_timeout(500)
    for i in range(2):
        timed('dup group %d'%(i+2),"document.getElementById('qaDup').click()");pg.wait_for_timeout(500)
        print(' strokes',js(ST+".strokes.length"))
    # frame times while dragging the group box
    js("window.__sketchpadInternals().segVerBump()");pg.wait_for_timeout(300)
    box=js("(()=>{const r=document.getElementById('groupBox').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    js("(()=>{const o=window.grpDragBegin;window.grpDragBegin=function(){const t=performance.now();const r=o.apply(this,arguments);window.__gdb=Math.round(performance.now()-t);return r;}})()")
    js("window.__ft=[];(function f(l){const n=performance.now();if(l)window.__ft.push(n-l);if(!window.__stop)requestAnimationFrame(()=>f(n))})(0)")
    pg.mouse.move(box[0],box[1]);pg.mouse.down()
    for i in range(20): pg.mouse.move(box[0]+i*8,box[1]+i*4)
    pg.wait_for_timeout(300)
    print('overlay nonblank px (mid-drag)',js("(()=>{const o=[...document.querySelectorAll('canvas')].filter(c=>c.style.display==='block'&&c!==document.getElementById('canvas'));return o.map(c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4*50)if(d[i]>10)n++;return n})})()"));pg.screenshot(path='middrag.png')
    pg.mouse.up();pg.wait_for_timeout(300);js("window.__stop=1")
    print('grpDragBegin ms',js('window.__gdb'),'canvas',js('[W,H]') if False else js('(()=>{const c=document.getElementById("canvas");return [c.width,c.height]})()'))
    ft=js("window.__ft");ft.sort();print('frames',len(ft),'median',round(ft[len(ft)//2]),'p90',round(ft[int(len(ft)*.9)]),'max',round(ft[-1]))
    prof=cdp.send('Profiler.stop')['profile']
    nodes={n['id']:n for n in prof['nodes']};self={}
    dts=prof['timeDeltas'];
    for sid,dt in zip(prof['samples'],dts):
        cf=nodes[sid]['callFrame'];k=cf['functionName']+':'+str(cf['lineNumber']);self[k]=self.get(k,0)+dt
    for k,v in sorted(self.items(),key=lambda x:-x[1])[:14]: print(round(v/1000),'ms',k)
    print(errs);b.close()
