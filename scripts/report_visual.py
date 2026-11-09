"""보고서 사진·위젯 조립 도구. 공부 노트 스킬의 note_visual.py를 그대로 빌려 쓰되, 필기 도구·계산기는 넣지 않는다.
사용:
  import sys,os; sys.path.insert(0,os.path.expanduser('~/.claude/skills/report-html/scripts'))
  from report_visual import *   # PH, PH2, HERO, PEOPLE, QUOTE, CASES, W, chip, chip_names, side_by_side, F(그림)
  html = embed_report(html, 사진폴더, who=WHO, widgets_js=위젯코드, extra_keys=())"""
import os,sys,re,json,base64
NV=os.path.expanduser('~/.claude/skills/study-note-artifact/scripts')
sys.path.insert(0,NV)
from note_visual import *          # noqa: F401,F403  PH, HERO, PEOPLE, W, side_by_side …
from note_visual import USED, ASSETS
from fig import F                  # noqa: F401  SVG 그림 도우미
def KEY(x): return f'<p class="gotit"><b>요점</b> {x}</p>'
def embed_report(t,img_dir=None,who=None,widgets_js='',extra_keys=()):
    """visual-kit CSS·JS, 사진(data URI), 위젯 JS를 마지막 <script> 앞에 넣는다. 필기·계산기는 넣지 않는다."""
    t=t.replace('</style>',open(os.path.join(ASSETS,'visual-kit.css'),encoding='utf8').read()+'</style>',1)
    keys=set(re.findall(r'data-i="(\w+)"',t))|USED|set(extra_keys); IMG={}
    for k in sorted(keys):
        p=os.path.join(img_dir or '',k+'.webp')
        if img_dir and os.path.exists(p): IMG[k]='data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode()
        else: print('사진 없음:',k)
    js='<script>window.IMG='+json.dumps(IMG)+';window.WHO='+json.dumps(who or {},ensure_ascii=False)+';</script><script>'+open(os.path.join(ASSETS,'visual-kit.js'),encoding='utf8').read()+'</script>'
    if widgets_js: js+='<script>'+widgets_js+'</script>'
    i=t.rindex('<script'); return t[:i]+js+t[i:]
