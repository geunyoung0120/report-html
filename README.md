# report-html

Claude Code 스킬. 조사·분석·프로젝트 결과를 **로컬 HTML 파일 하나**로 된 읽기 전용 보고서로 만든다.

- 요약(핵심 결론·핵심 수치) → 본론(그림·발견 카드·확인 정도 표시) → 결론과 제언 → 부록(출처) 구조
- 왼쪽 벽 목차 서랍, 오른쪽 벽 용어 서랍, 용어 툴팁, 다크 배경
- 출처 번호 `[n]` 미리보기와 부록으로 이동, 그림·표 번호 자동
- 실제 사진(Wikimedia Commons), SVG 도식, 직접 눌러 보는 위젯
- 인쇄하면 모든 장과 접힌 상자를 펼쳐 장마다 새 쪽으로 출력(PDF 저장 가능)

## 설치

```
git clone https://github.com/geunyoung0120/report-html ~/.claude/skills/report-html
```

Claude Code에서 "보고서 만들어줘", "보고서 html로" 같은 요청을 하면 이 스킬이 쓰인다.

## 필요한 것

- 다른 스킬 없이 이 레포만으로 동작한다.
- Python 3와 Pillow(`pip install pillow`, 사진 받기·줄이기), Node.js(검사 스크립트)
- 위젯 클릭 시험(`scripts/test_note.py`)을 쓰려면 Playwright와 Google Chrome이 필요하다(준비 방법은 파일 머리말).

## 파일

| 파일 | 역할 |
|---|---|
| `SKILL.md` | 스킬 지침 |
| `assets/template.html` | 보고서 틀(CSS·JS 포함) |
| `scripts/report_visual.py` | 사진·위젯 조립(`embed_report`) |
| `scripts/check_report.js` | 넘기기 전 검사 |
| `scripts/note_visual.py` | 사진·인물 카드·가로 배치 HTML 조각 |
| `scripts/fig.py` | SVG 그림 도우미 |
| `scripts/fetch_images.py` | Wikimedia Commons 사진 받기·WebP 변환·출처 기록 |
| `scripts/test_note.py` | 크롬으로 위젯을 눌러 오류·가로 넘침 찾기 |
| `assets/visual-kit.css`, `assets/visual-kit.js` | 사진·위젯 공용 스타일과 함수 |
| `assets/widget-gallery.js` | 위젯 예시 모음 |
