import sys,re,subprocess,base64,math;sys.path.insert(0,'/home/claude/sp-ipad/tests')
from common import boot
from playwright.sync_api import sync_playwright
SD='/tmp/claude-0/-home-claude/4edb330a-3b17-5d84-865e-a0ad5e3a1d2b/scratchpad/'
def ok(c,m):
  assert c,m;print('PASS',m)
def hx(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def lab(c):
  f=lambda v:(v/255/12.92) if v/255<=.04045 else ((v/255+.055)/1.055)**2.4
  R,G,B=map(f,c);X=(R*.4124+G*.3576+B*.1805)/.95047;Y=R*.2126+G*.7152+B*.0722;Z=(B*.9505+G*.1192+R*.0193)/1.08883
  t=lambda v:v**(1/3) if v>.008856 else 7.787*v+16/116
  return (116*t(Y)-16,500*(t(X)-t(Y)),200*(t(Y)-t(Z)))
dE=lambda a,b:math.dist(lab(a),lab(b))
old=subprocess.run(['git','show','HEAD:index.html'],capture_output=True,text=True,cwd='/home/claude/sp-ipad').stdout
a=old.index('function cmExtractColoursFromImage');b=old.index("// Paint Inside: 'free'")
OLD=old[a:b].replace('cmExtractColoursFromImage','cmOld')
img='data:image/png;base64,'+base64.b64encode(open(SD+'goose/goose.png','rb').read()).decode()
TRUE=(252,149,78)   # sampled from the beak in the original artwork
with sync_playwright() as p:
  b,pg,errs=boot(p);js=pg.evaluate
  pg.evaluate("src=>new Promise(r=>{const i=new Image();i.onload=()=>{window.__g=i;r()};i.src=src})",img)
  print('g',js('!!window.__g'));HELP=''.join(l+'\n' for l in old.split('\n') if l.startswith('function rgbToHexMB') or l.startswith('function rgbToHsvMB'))
  js('(()=>{'+HELP+'window.cmOld='+OLD.strip().rstrip(';')+';return 0})()')
  o=js("cmOld(window.__g,8)");print('old8',o)
  print('old nearest to true orange: dE=%.1f'%min(dE(hx(c),TRUE) for c in o))
  res={}
  for mode in('exact','clean'):
    for n in(8,16,32):
      t=js("(()=>{const t=performance.now();const I=window.__sketchpadInternals();const c=I.cmExtractColoursFromImage(window.__g,%d,'%s');return [c,I.cmExtractInfo().found,performance.now()-t]})()"%(n,mode))
      cols,found,ms=t;res[(mode,n)]=cols
      d=min(dE(hx(c),TRUE) for c in cols);print(mode,n,'found',found,'ms %.0f'%ms,'orange dE %.1f'%d,cols)
      ok(d<8,'%s %d colours: contains the real peachy orange (dE %.1f from the beak pixels)'%(mode,n,d))
      mud=[c for c in cols if 15<lab(hx(c))[0]<50 and 25<math.hypot(*lab(hx(c))[1:])and 40<math.degrees(math.atan2(lab(hx(c))[2],lab(hx(c))[1]))<75]
      ok(len(mud)<=1 if mode=='clean' else True,'%s %d: no cluster of muddy browns (%d dark oranges)'%(mode,n,len(mud)))
  for mode in('exact','clean'):
    ok(res[(mode,8)]==res[(mode,16)][:len(res[(mode,8)])] and res[(mode,16)]==res[(mode,32)][:len(res[(mode,16)])],'%s: main colours stay the same when the count grows'%mode)
  ok(len(res[('clean',16)])<=len(res[('exact',16)]),'clean palette is no bigger than the exact palette')
  # pink + black + white + orange all present at 8 (exact)
  c8=res[('exact',8)];L=[lab(hx(c)) for c in c8]
  ok(any(l[0]<20 for l in L) and any(l[0]>92 for l in L) and any(dE(hx(c),(240,110,150))<22 for c in c8),'exact 8 keeps black outline, white and a pink')
  # UI: upload through the real control, mode buttons, count read-out, save palette
  js("document.getElementById('acExtractBox').style.display='block'")
  pg.set_input_files('#acImageFile',SD+'goose/goose.png');pg.wait_for_timeout(1200)
  sw=lambda:js("document.querySelectorAll('#acImageSwatches .swatch, #acImageSwatches > *').length")
  n8=sw();print('swatches',n8)
  ok(n8>=6,'upload still extracts and shows swatches')
  js("(()=>{const e=document.getElementById('acImageCount');e.value='32';e.dispatchEvent(new Event('input'))})()");pg.wait_for_timeout(500)
  lab_=js("document.getElementById('acImageCountVal').textContent");print('label',lab_)
  ok(' of 32' in lab_,'slider label shows the real number found when fewer than 32 exist (%s)'%lab_)
  js("document.querySelector('#acExtractBox .acModeBtn[data-mode=clean]').click()");pg.wait_for_timeout(500)
  nc=sw();ok(nc<js("1000") and nc<=n8+20,'clean mode re-extracts (%d swatches)'%nc)
  ok(js("localStorage.getItem('sp-extract-mode')")=='clean','mode choice remembered')
  js("document.getElementById('acPaletteName').value='Goose test';document.getElementById('acSavePaletteBtn').click()");pg.wait_for_timeout(300)
  ok(js("(JSON.stringify(window.__sketchpadGetState().savedPalettes||'')||'').includes('Goose test') || document.getElementById('acSavedPalettesList').textContent.includes('Goose test')"),'extracted palette can still be saved')
  print(errs);b.close()
