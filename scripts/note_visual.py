"""사진·위젯 HTML 조각 도우미(study-note-artifact에서 가져옴). report_visual.py가 불러 쓴다.
필기 도구·계산기 관련 함수는 보고서에 쓰지 않아 뺐다."""
import re,os,html,json,base64
USED=set()
HERE=os.path.dirname(os.path.abspath(__file__)); ASSETS=os.path.join(HERE,'..','assets')
def _txt(s): return html.escape(re.sub('<[^>]+>','',s))
def W(name): return f'<div class="wg" data-w="{name}"></div>'
def PH(key,cap,cls=''):
    USED.add(key); return f'<figure class="ph {cls}"><img data-i="{key}" alt="{_txt(cap)}"><figcaption>{cap}</figcaption></figure>'
def PH2(*a): return '<div class="ph2">'+''.join(PH(k,c) for k,c in a)+'</div>'
def HERO(key,t,s):
    USED.add(key); return f'<div class="hero"><img data-i="{key}" alt=""><div><b>{t}</b><span>{s}</span></div></div>'
def PEOPLE(*l):
    o=''
    for k,n,r,d in l:
        USED.add('a_'+k); o+=f'<div class="person"><img data-i="a_{k}" alt="{n} 사진"><b>{n}</b><i>{r}</i><span>{d}</span></div>'
    return f'<div class="people">{o}</div>'
def QUOTE(k,t,w):
    USED.add('a_'+k); return f'<blockquote class="quote"><img data-i="a_{k}" alt=""><p>{t}<small>{w}</small></p></blockquote>'
def CASES(*l):
    o=''
    for k,t,d in l:
        USED.add(k); o+=f'<div class="case"><img data-i="{k}" alt=""><div><b>{t}</b><span>{d}</span></div></div>'
    return f'<div class="cases">{o}</div>'
def GOT(x): return f'<p class="gotit"><b>한 줄 정리</b> {x}</p>'
def PIC_CARD(href,key,k,t,d):
    USED.add(key); return f'<a class="card pic" href="#{href}"><img data-i="{key}" alt=""><span class="in"><span class="k">{k}</span><span class="tt">{t}</span><span class="d">{d}</span></span></a>'
def chip(s):
    """본문의 @{key|이름}을 얼굴 칩으로 바꾼다"""
    def f(m):
        USED.add('a_'+m[1]); return f'<span class="pc" data-who="{m[1]}" tabindex="0"><img data-i="a_{m[1]}" alt="">{m[2]}</span>'
    return re.sub(r'@\{(\w+)\|([^}]+)\}',f,s)
def chip_names(page,names):
    """페이지마다 <p> 안에서 처음 나오는 이름 하나를 자동으로 칩으로 바꾼다. names=[('피터 틸','thiel'),...]. 긴 이름을 앞에 둔다."""
    seen=set()
    def para(m):
        x=m[1]
        for n,k in names:
            if k in seen or n not in x: continue
            parts=re.split(r'(<[^>]+>)',x)
            for i,pp in enumerate(parts):
                if not pp.startswith('<') and n in pp:
                    parts[i]=pp.replace(n,'@{%s|%s}'%(k,n),1); seen.add(k); break
            x=''.join(parts)
        return '<p>'+x+'</p>'
    return re.sub(r'<p>(.*?)</p>',para,page,flags=re.S)
def side_by_side(items):
    """본문 조각 목록에서 그림과 바로 뒤의 설명을 가로 배치로 묶는다.
    그림(<figure class="fig) 다음에 <h2>그림 따라 읽기</h2>나 <p>가 이어지면 묶는다. 묶은 목록을 돌려준다.
    넓은 화면에서는 그림이 왼쪽, 설명 세로 중앙에 놓이고 좁은 화면에서는 세로로 쌓인다."""
    out=[];i=0
    while i<len(items):
        x=items[i]
        if isinstance(x,str) and x.startswith('<figure class="fig') and i+1<len(items) and isinstance(items[i+1],str) and (items[i+1].startswith('<p>') or items[i+1].startswith('<h2>그림 따라 읽기')):
            j=i+1;t=[]
            while j<len(items) and isinstance(items[j],str) and (items[j].startswith('<p>') or (j==i+1 and items[j].startswith('<h2>그림 따라 읽기'))):
                t.append(items[j]);j+=1
            out.append(f'<div class="sbs"><div class="sbs-in"><div class="sbs-f">{x}</div><div class="sbs-t">{"".join(t)}</div></div></div>');i=j
        else: out.append(x);i+=1
    return out
