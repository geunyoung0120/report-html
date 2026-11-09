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

## 의존성

그림·사진·위젯 도구는 같은 사용자의 공부 노트 스킬 `study-note-artifact`의 파일을 그대로 가져다 쓴다(`~/.claude/skills/study-note-artifact/scripts/fig.py`, `note_visual.py`, `fetch_images.py`, `test_note.py`, `assets/visual-kit.*`, `assets/widget-gallery.js`). 그 스킬이 없으면 `report_visual.py`의 import가 실패한다. 템플릿(`assets/template.html`)과 검사 스크립트(`scripts/check_report.js`)는 단독으로 동작한다.

## 파일

| 파일 | 역할 |
|---|---|
| `SKILL.md` | 스킬 지침 |
| `assets/template.html` | 보고서 틀(CSS·JS 포함) |
| `scripts/report_visual.py` | 사진·위젯 조립(`embed_report`) |
| `scripts/check_report.js` | 넘기기 전 검사 |
