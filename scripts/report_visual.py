"""보고서 사진·위젯 조립 도구. 같은 폴더의 note_visual.py, fig.py를 쓴다. 필기 도구·계산기는 넣지 않는다.
사용:
  import sys,os; sys.path.insert(0,os.path.expanduser('~/.claude/skills/report-html/scripts'))
  from report_visual import *   # PH, PH2, HERO, PEOPLE, QUOTE, CASES, W, chip, chip_names, side_by_side, F(그림)
  html = embed_report(html, 사진폴더, who=WHO, widgets_js=위젯코드, extra_keys=())"""
import os,sys,re,json,base64
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from note_visual import *          # noqa: F401,F403  PH, HERO, PEOPLE, W, side_by_side …
from note_visual import USED, ASSETS
from fig import F                  # noqa: F401  SVG 그림 도우미
def KEY(x): return f'<p class="gotit"><b>요점</b> {x}</p>'
def embed_report(t,img_dir=None,who=None,widgets_js='',extra_keys=()):
    """visual-kit CSS·JS, 사진(data URI), 위젯 JS를 템플릿 스크립트 뒤(문서 맨 끝)에 넣는다. 필기·계산기는 넣지 않는다."""
    t=t.replace('</style>',open(os.path.join(ASSETS,'visual-kit.css'),encoding='utf8').read()+'</style>',1)
    keys=set(re.findall(r'data-i="(\w+)"',t))|USED|set(extra_keys); IMG={}
    for k in sorted(keys):
        p=os.path.join(img_dir or '',k+'.webp')
        if img_dir and os.path.exists(p): IMG[k]='data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode()
        else: print('사진 없음:',k)
    js='<script>window.IMG='+json.dumps(IMG)+';window.WHO='+json.dumps(who or {},ensure_ascii=False)+';</script><script>'+open(os.path.join(ASSETS,'visual-kit.js'),encoding='utf8').read()+'</script>'
    if widgets_js: js+='<script>'+widgets_js+'</script>'
    # 본문을 그리는 템플릿 스크립트를 먼저 돌리고, 용량이 큰 사진(data URI)은 맨 뒤에 둔다.
    # 느린 회선에서도 사진을 다 받기 전에 글과 목차가 먼저 보인다.
    i=t.rindex('</script>')+len('</script>'); return t[:i]+js+t[i:]
