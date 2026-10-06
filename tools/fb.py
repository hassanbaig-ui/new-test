import sys, json, re, time
from playwright.sync_api import sync_playwright
def load_cookies(p):
    out=[]
    for l in open(p):
        if l.startswith('#') and not l.startswith('#HttpOnly_'): continue
        f=l.rstrip('\n').split('\t')
        if len(f)<7: continue
        d=f[0].replace('#HttpOnly_','')
        out.append(dict(name=f[5],value=f[6],domain=d,path=f[2],secure=f[3]=='TRUE',httpOnly=l.startswith('#HttpOnly_')))
    return out
def ctx(p, cookies):
    import os; b=p.chromium.launch(headless=True,executable_path='/opt/pw-browsers/chromium',proxy={'server':os.environ['HTTPS_PROXY']} if os.environ.get('HTTPS_PROXY') else None)
    c=b.new_context(viewport={'width':1280,'height':1600},locale='en-US',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36')
    c.add_cookies(load_cookies(cookies)); return b,c
mode=sys.argv[1]; cookies=sys.argv[2]
with sync_playwright() as p:
    b,c=ctx(p,cookies); pg=c.new_page()
    if mode=='probe':
        pg.goto(sys.argv[3],wait_until='domcontentloaded'); time.sleep(6)
        print(pg.url); print(pg.title())
        pg.screenshot(path=sys.argv[4])
        print(pg.inner_text('body')[:3000])
    elif mode=='search':
        out={}
        for q in sys.argv[3:]:
            for kind in ('pages','videos'):
                pg.goto('https://www.facebook.com/search/%s/?q=%s'%(kind,q.replace(' ','%20')),wait_until='domcontentloaded'); time.sleep(5)
                for _ in range(3): pg.mouse.wheel(0,3000); time.sleep(2)
                txt=pg.inner_text('body')
                links=pg.eval_on_selector_all('a[href]','els=>els.map(e=>[e.href,e.innerText.slice(0,80)])')
                out[q+'|'+kind]={'text':txt[:6000],'links':[l for l in links if l[1].strip()]}
        json.dump(out,sys.stdout,ensure_ascii=False)
    elif mode=='links':
        pg.goto(sys.argv[3],wait_until='domcontentloaded'); time.sleep(6)
        for h,t in pg.eval_on_selector_all('a[href]','els=>els.map(e=>[e.href,e.innerText.slice(0,60)])'):
            if t.strip(): print(h,'|',t.replace('\n',' '))
    elif mode=='reels':
        url=sys.argv[3]; pg.goto(url,wait_until='domcontentloaded'); time.sleep(6)
        seen={}; stale=0
        while stale<6:
            items=pg.eval_on_selector_all('a[href*="/reel/"]','els=>els.map(e=>[e.href,e.innerText])')
            n=len(seen)
            for h,t in items:
                m=re.search(r'/reel/(\d+)',h)
                if m: seen.setdefault(m.group(1),t.strip())
            stale = stale+1 if len(seen)==n else 0
            pg.mouse.wheel(0,4000); time.sleep(2.5)
        print(pg.url, file=sys.stderr)
        json.dump([{'id':k,'tile':v} for k,v in seen.items()],sys.stdout,ensure_ascii=False)
    b.close()
