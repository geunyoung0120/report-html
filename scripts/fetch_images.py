#!/usr/bin/env python3
"""Wikimedia Commons 사진을 내려받아 WebP로 줄이고 출처를 meta.json에 적는다.
사용: python3 fetch_images.py list.json 출력폴더
list.json: {"photo":{"key":"File 제목.jpg"}, "face":{"key":["File 제목.jpg",중심x,중심y,크기]}, "wiki":{"key":"위키백과 문서 제목"}}
face의 값은 0~1 비율이고 크기는 잘라 낼 정사각형 한 변/사진 너비다. 결과는 a_key.webp(360px).
화질 기준: 작은 축소본을 받지 않는다. 받기는 긴 변 1920px(원본이 작으면 원본), 사진 저장은 1600px·품질 80, 얼굴은 360px·품질 82. 화면 폭 980px를 고해상도 모니터에서 봐도 흐리지 않게 하는 값이다. 원본이 1000px 미만이면 그 값을 경고로 찍으니 더 큰 사진을 찾아 바꾼다.
먼저 위키백과 문서로 대표 사진 파일명을 찾을 수 있다. python의 SSL 인증서 문제를 피하려고 curl을 쓴다."""
import json,subprocess,sys,time,re,html,os,urllib.parse
from PIL import Image
UA='report-html-builder/1.0'
def get(u):
    for _ in range(4):
        o=subprocess.run(['curl','-sS','--max-time','30','-A',UA,u],capture_output=True,text=True).stdout
        try: return json.loads(o)
        except Exception: time.sleep(4)
def info(t):
    q=urllib.parse.urlencode({'action':'query','prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1920,'titles':'File:'+t,'format':'json'})
    r=get('https://commons.wikimedia.org/w/api.php?'+q); time.sleep(1.2)
    pg=list(r['query']['pages'].values())[0] if r else {}
    if 'imageinfo' not in pg: print('못 찾음',t); return None
    return pg['imageinfo'][0]
def lead(title):
    q=urllib.parse.urlencode({'action':'query','prop':'pageimages','piprop':'original','redirects':1,'format':'json','titles':title})
    r=get('https://en.wikipedia.org/w/api.php?'+q); time.sleep(1)
    for p in r['query']['pages'].values():
        s=p.get('original',{}).get('source')
        if s: return urllib.parse.unquote(s.split('?')[0].split('/')[-1]).replace('_',' ')
L=json.load(open(sys.argv[1],encoding='utf8')); out=sys.argv[2]; os.makedirs(out+'/raw',exist_ok=True); meta={}
for k,t in L.get('wiki',{}).items(): L.setdefault('photo',{})[k]=lead(t)
jobs=[(k,t,None) for k,t in L.get('photo',{}).items() if t]+[(k,v[0],v[1:]) for k,v in L.get('face',{}).items()]
for k,t,face in jobs:
    ii=info(t)
    if not ii: continue
    e=ii['extmetadata']; meta[k]=dict(title=t,page=ii['descriptionurl'],lic=e.get('LicenseShortName',{}).get('value',''),artist=html.unescape(re.sub('<[^>]+>','',e.get('Artist',{}).get('value','')))[:80].strip())
    f=f'{out}/raw/{k}.img'; subprocess.run(['curl','-sS','-L','--max-time','60','-A',UA,'-o',f,ii.get('thumburl') or ii['url']]); time.sleep(1.2)
    im=Image.open(f).convert('RGB')
    if face:
        cx,cy,s=face; W_,H=im.size; a=min(s,1)*W_; x=max(0,min(W_-a,cx*W_-a/2)); y=max(0,cy*H-a/2)
        im.crop((int(x),int(y),int(x+a),int(y+a))).resize((360,360),Image.LANCZOS).save(f'{out}/a_{k}.webp',quality=82,method=6)
    else:
        im.thumbnail((1600,1800),Image.LANCZOS); im.save(f'{out}/{k}.webp',quality=80,method=6)
    print(k,meta[k]['lic'],'|',meta[k]['artist'][:30],'| 원본',im.size,'← 저해상도: 더 큰 사진을 찾으세요' if max(im.size)<1000 else '')
json.dump(meta,open(out+'/meta.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
