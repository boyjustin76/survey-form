# 틀 갈아 끼우기 표 (assets/survey_template.html)

찾을 때는 줄 번호 대신 아래 '찾는 글'로 grep 한다(줄 번호는 고칠 때마다 바뀜).

| 바꿀 것 | 찾는 글 | 메모 |
|---|---|---|
| 창 제목 | `<title>` | 2~4단어 |
| 첫 화면 제목·안내 4줄 | `id="t-start"`, `class="notes"` | 평가 무관·걸리는 시간·캡처 안내·메일로 끝 |
| 받는 메일 주소 | `var TO=` | 사용자에게 확인. 외부 주소 금지 |
| 보기 목록 | `var OPT={` | kind(어떤 일)·way·where·help. 각 끝에 '기타' |
| 조직도 맨 위(실장) | `var HEAD=` | team·name·role·색 |
| 조직도 팀·사람 | `var PEOPLE=` | 팀마다 team·role·색·names. 설문 만든 사람은 빼기 |
| 맞춤 보기 | `var REC={` | 이름 → [[일 이름, kind 보기 글자], …]. kind 글자는 `OPT.kind`에 있는 것만. 위 주석에 근거 자료 적기 |
| 맞춤 말풍선 글·자료 목록 | `id="rec-tip"` | 자료 이름만(날짜·작성자 없이) |
| 일 개수·캡처 장수 | `MAXT=`, `MAXI=` | 기본 3·3 |
| 문항 글 | `id="l-kind"`, `for="f-tools"`, `data-field=way` 근처 `ql` | 문항 추가·삭제 시 `QS`·`QN`·`newTask`·`textAnswer`·`renderSummary` 같이 |
| 캡처 받는 문항 | `var QS=` 와 `class="att" data-q=` | 둘이 맞아야 함 |
| 마지막 질문 | `id="l-check"`, `function renderLast` | 보내기 페이지 요약 아래 |
| 메일 제목 | `'Subject: =?UTF-8?B?'+b64utf8(` | |
| 답 파일 이름 | `function emlName` | 완료 화면 `id="done-lead"` 글도 같이 |
| 저장 키 | `'ax-survey8'`, `'ax-slot'`, `indexedDB.open('ax-survey'`, `'ax-draft1'` | **설문마다 새 접두어로** (예: `hr2027-`) |

## 맞춤 보기(REC) 뽑는 법

1. 사내 R&R·업무 보드(담당 R·책임 A)·Teams/메일 아카이브를 읽는다. 아카이브 `00_주의사항` 먼저.
2. 사담·민감 메시지 제외, 메시지 수로 사람 비교 금지, '공유한 사람 = 담당' 단정 금지.
3. 사람당 5~9개, 일 이름은 짧게. 협력사 이름은 원자료(업무 보드)에 있던 것만.
4. 공통 보기(`OPT.kind`)에 없는 일 유형이 자료에 자주 나오면 공통 보기에 더한다(예: '계약·구매·비용 처리', '심의·등급·스토어 등록').
