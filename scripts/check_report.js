#!/usr/bin/env node
// 보고서 HTML을 넘기기 전에 흔한 실수를 잡는다.
// 사용: node check_report.js path/to/report.html
const fs = require("fs");
const file = process.argv[2];
if (!file) { console.error("사용법: node check_report.js <html 파일>"); process.exit(2); }
const h = fs.readFileSync(file, "utf8");
const problems = [], notes = [];

// 1) 마지막 <script> 문법
const js = h.split("<script>").pop().split("</script>")[0];
try { new Function(js); } catch (e) { problems.push("JS 문법 오류: " + e.message); }

// 2) 툴팁 용어
let gloss = {};
const gm = js.match(/const GLOSS = (\{[\s\S]*?\n\});/);
if (!gm) problems.push("GLOSS 객체를 찾지 못함");
else { try { gloss = eval("(" + gm[1] + ")"); } catch (e) { problems.push("GLOSS 파싱 실패: " + e.message); } }
let m, used = 0; const missing = new Set();
const re = /<span class="t"(?: data-k="([^"]+)")?>([^<]+)<\/span>/g;
while ((m = re.exec(h))) { used++; const k = m[1] || m[2].trim(); if (!gloss[k]) missing.add(k); }
if (missing.size) problems.push("GLOSS에 없는 툴팁 용어: " + [...missing].join(", "));
if ((h.match(/<span class="t">[^<]*<span/g) || []).length) problems.push("툴팁 span 안에 다른 태그가 있음");

// 3) 페이지 구조
const secs = [...h.matchAll(/<section class="page[^"]*" id="([^"]+)"[^>]*data-group="([^"]+)"[^>]*>([\s\S]*?)<\/section>/g)];
const ids = secs.map(s => s[1]);
const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
if (dup.length) problems.push("중복된 페이지 id: " + [...new Set(dup)].join(", "));
const bad = ids.filter(x => !/^[A-Za-z0-9-]+$/.test(x));
if (bad.length) problems.push("id는 영문·숫자·하이픈만: " + bad.join(", "));
if (!ids.includes("summary")) problems.push('요약 장(id="summary")이 없음');
if (!/class="tldr"/.test(h)) problems.push("핵심 결론(.tldr)이 없음");
if (!ids.includes("appendix")) notes.push('부록(id="appendix")이 없음');

// 4) 출처 번호가 목록 안에 있는지
const nSrc = ((h.match(/<ol class="sources"[^>]*>([\s\S]*?)<\/ol>/) || [, ""])[1].match(/<li[\s>]/g) || []).length;
const refs = [...h.matchAll(/class="ref" data-src="(\d+)"/g)].map(x => +x[1]);
const outRef = [...new Set(refs.filter(n => n < 1 || n > nSrc))];
if (outRef.length) problems.push(`출처 목록(${nSrc}개) 밖의 출처 번호: ${outRef.join(", ")}`);
const unused = []; for (let i = 1; i <= nSrc; i++) if (!refs.includes(i)) unused.push(i);
if (unused.length) notes.push("본문에서 한 번도 인용하지 않은 출처: " + unused.join(", "));

// 5) 본론 장: 그림, 근거
const strip = s => s.replace(/<figure[\s\S]*?<\/figure>/g, "").replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/g, " ").replace(/\s+/g, " ").trim();
const noFig = [], noRef = [], thin = [];
for (const [, id, group, body] of secs) {
  if (!/^[A-Z]\./.test(group)) continue;
  if (!/<figure class="fig|class="wg"|data-i="/.test(body)) noFig.push(id);
  if (!/class="ref"/.test(body)) noRef.push(id);
  if (strip(body).length < 600) thin.push(`${id}(${strip(body).length}자)`);
}
if (noFig.length) notes.push("그림·사진·위젯이 하나도 없는 장: " + noFig.join(", "));
if (noRef.length) notes.push("출처 번호가 하나도 없는 장: " + noRef.join(", "));
if (thin.length) notes.push("본문이 짧은 장(600자 미만): " + thin.join(", "));
const figBad = (h.match(/<figure class="fig[^"]*">(?:(?!<\/figure>)[\s\S])*<\/figure>/g) || []).filter(f => !/<figcaption>/.test(f) || !/role="img"/.test(f)).length;
if (figBad) problems.push(`figcaption 또는 role="img"가 빠진 그림: ${figBad}개`);
const o = (h.match(/<details[\s>]/g) || []).length, c = (h.match(/<\/details>/g) || []).length;
if (o !== c) problems.push(`<details> 짝이 안 맞음: ${o} / ${c}`);

// 6) 자리표시자, 외부 스크립트, 사진
const left = h.match(/\{\{[^}]*\}\}/g) || [];
if (left.length) problems.push(`채우지 않은 {{자리표시자}}: ${left.length}개 (예: ${left[0]})`);
for (const s of h.matchAll(/<script[^>]+src="([^"]+)"/g))
  if (!/^https:\/\/(cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net\/npm\/|unpkg\.com)/.test(s[1])) problems.push("허용 CDN 밖 외부 스크립트: " + s[1]);
const keys = [...new Set([...h.matchAll(/data-i="(\w+)"/g)].map(x => x[1]))];
const im = h.match(/window\.IMG=(\{.*?\});window\.WHO/);
if (keys.length && !im) problems.push("사진 키는 있는데 window.IMG가 없음: embed_report()를 실행하세요");
else if (im) { const miss = keys.filter(k => !im[1].includes('"' + k + '":')); if (miss.length) problems.push("IMG에 없는 사진 키: " + miss.join(", ")); }
if (/class="q[ "]|window\.NoteQ|claude\.use/.test(h)) problems.push("문제·채팅 코드가 들어 있음: 보고서에는 넣지 않는다");
if (!h.includes("TOC_EDGE") || !h.includes("glDraw") || !h.includes("setBtn")) problems.push("목차·용어 서랍이나 설정 버튼이 없음: template.html로 다시 만드세요");
{ const bare = (h.match(/<h2>그림 따라 읽기<\/h2>/g) || []).length - (h.match(/class="sbs-t"><h2>그림 따라 읽기<\/h2>/g) || []).length;
  if (bare > 0) notes.push(`그림과 나란히 배치되지 않은 "그림 따라 읽기": ${bare}곳 (side_by_side()를 쓰세요)`); }

console.log(`장 ${secs.length} · 그림 ${(h.match(/<figure class="fig/g) || []).length} · 사진 ${keys.length} · 위젯 ${(h.match(/class="wg"/g) || []).length} · 출처 ${nSrc}(인용 ${refs.length}회) · 툴팁 ${used}회 / 용어 ${Object.keys(gloss).length}개 · ${(h.length / 1024).toFixed(0)}KB`);
notes.forEach(n => console.log("참고: " + n));
if (problems.length) { problems.forEach(p => console.log("문제: " + p)); process.exit(1); }
console.log("통과");
