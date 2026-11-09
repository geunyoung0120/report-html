"""공부 노트용 인라인 SVG 그림 도우미. 색은 페이지 CSS 클래스(테마 대응)로 칠한다."""
import html as _h, os as _os
_n = [0]
# 실행마다 다른 접두어: 여러 번에 나눠 만든 그림을 한 페이지에 모아도 화살표 마커 id가 겹치지 않게 한다
# (id가 겹치면 숨겨진 다른 페이지의 마커를 가리켜 화살표 머리가 사라진다)
_PREFIX = "f" + _os.urandom(3).hex()

def esc(s):
    return _h.escape(str(s), quote=True)

class F:
    def __init__(self, w, h):
        _n[0] += 1
        self.id = f"{_PREFIX}g{_n[0]}"
        self.w, self.h, self.items = w, h, []

    def raw(self, s):
        self.items.append(s); return self

    def rect(self, x, y, w, h, cls="b", rx=6, style=""):
        st = f' style="{style}"' if style else ""
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"{st}/>'); return self

    def text(self, x, y, t, cls="", anchor="middle", size=None):
        st = f' style="font-size:{size}px"' if size else ""
        self.items.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{st}>{esc(t)}</text>'); return self

    def box(self, x, y, w, h, title, sub=None, cls="b", tcls="bo", scls="sm mu"):
        self.rect(x, y, w, h, cls)
        subs = [] if not sub else (sub if isinstance(sub, list) else [sub])
        # 제목 1줄 + 부제 n줄을 상자 세로 가운데에 놓는다 (줄 간격 14px)
        top = y + h / 2 - (1 + len(subs)) * 14 / 2 + 11
        self.text(x + w / 2, top, title, tcls)
        for i, s in enumerate(subs):
            self.text(x + w / 2, top + 14 * (i + 1), s, scls)
        return self

    def line(self, x1, y1, x2, y2, cls="ln", dash=False):
        d = ' stroke-dasharray="4 4"' if dash else ""
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{d}/>'); return self

    def arrow(self, x1, y1, x2, y2, label=None, acc=False, dash=False, lx=None, ly=None, lcls="sm mu", anchor="middle"):
        cls = "lnA" if acc else "ln"
        m = f"{self.id}{'b' if acc else 'a'}"
        d = ' stroke-dasharray="4 4"' if dash else ""
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#{m})"{d}/>')
        if label:
            lx = (x1 + x2) / 2 if lx is None else lx
            ly = (y1 + y2) / 2 - 7 if ly is None else ly
            self.text(lx, ly, label, lcls, anchor)
        return self

    def bracket(self, x1, x2, y, label, acc=True, down=True):
        c = "lnA" if acc else "ln"
        t = 7 if down else -7
        self.items.append(f'<polyline points="{x1},{y + t} {x1},{y} {x2},{y} {x2},{y + t}" class="{c}"/>')
        self.text((x1 + x2) / 2, y - 6 if down else y + 16, label, "sm bo " + ("ac" if acc else "mu"))
        return self

    def row(self, x0, y, w, h, gap, items, label_gap=None):
        """items: [(title, sub, cls)] 가로로 늘어놓고 화살표로 잇는다. 상자 오른쪽 끝 좌표 목록을 돌려준다."""
        xs = []
        for i, it in enumerate(items):
            title, sub, cls = (list(it) + [None, "b"])[:3]
            x = x0 + i * (w + gap)
            self.box(x, y, w, h, title, sub, cls or "b")
            xs.append(x)
            if i:
                self.arrow(x - gap + 2, y + h / 2, x - 3, y + h / 2)
        return xs

    def svg(self, label):
        defs = (f'<defs><marker id="{self.id}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
                f'<marker id="{self.id}b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" class="ahA"/></marker></defs>')
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg">'
                + defs + "".join(self.items) + "</svg>")

def fig(f, caption, wide=True):
    cls = "fig wide" if wide else "fig"
    return f'<figure class="{cls}">{f.svg(caption)}<figcaption>{esc(caption)}</figcaption></figure>'
