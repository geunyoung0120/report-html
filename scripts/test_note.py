#!/usr/bin/env python3
"""실제 크롬으로 모든 페이지의 위젯 버튼·슬라이더를 눌러 본다. 데스크톱과 휴대폰 폭.
준비: python3 -m venv <스크래치>/pw && <스크래치>/pw/bin/pip install playwright
사용: <스크래치>/pw/bin/python test_note.py note.html [스크린샷폴더]"""
import sys,os,urllib.parse
from playwright.sync_api import sync_playwright
CH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
url='file://'+urllib.parse.quote(os.path.abspath(sys.argv[1])); shot=sys.argv[2] if len(sys.argv)>2 else None
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH)
    for vp,name in [((1280,900),'d'),((390,844),'m')]:
        pg=b.new_page(viewport={'width':vp[0],'height':vp[1]})
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
        pg.goto(url); pg.wait_for_timeout(800)
        ids=pg.eval_on_selector_all('section.page','e=>e.map(x=>x.id)')
        print(name,'페이지',len(ids),'위젯',pg.locator('.wg').count(),'빈 사진',pg.evaluate("[...document.querySelectorAll('img[data-i]')].filter(i=>!i.getAttribute('src')).map(i=>i.dataset.i)"))
        over=[]
        for i in ids:
            pg.evaluate(f"location.hash='{i}'"); pg.wait_for_timeout(60)
            d=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            if d>1: over.append((i,d))
            for c in pg.locator(f'#{i} .wg button').all():
                try:
                    if c.is_enabled(): c.click(timeout=800)
                except Exception as e: errs.append(f'{i} 클릭 실패 {str(e)[:60]}')
            for r in pg.locator(f'#{i} .wg input[type=range]').all(): r.fill(r.get_attribute('max'))
            if shot:
                os.makedirs(shot,exist_ok=True); pg.wait_for_timeout(300); pg.screenshot(path=f'{shot}/{name}_{i}.png',full_page=True)
        print('가로 넘침',over); pg.close()
    b.close()
print('오류',len(errs),errs[:10]); sys.exit(1 if errs else 0)
