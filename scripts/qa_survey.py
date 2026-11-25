# survey-form 스킬 QA 예시(assets/survey_template.html 예시 기준). 클릭하는 이름·보기 글자를 새 설문에 맞게 바꿔 쓴다.
import sys, pathlib, base64
from playwright.sync_api import sync_playwright
from email import policy
from email.parser import BytesParser
F = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(exist_ok=True); IMG = sys.argv[3]
url = F.resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, accept_downloads=True)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(400)
    pg.screenshot(path=str(OUT / "1_start.png"), full_page=True)
    pg.click("text=시작하기"); pg.wait_for_timeout(200)
    print("시작 → 본인 확인 화면:", pg.is_visible("#s-who"), "| 탭:", pg.inner_text(".steps").replace(chr(10)," "))
    pg.click("#who-next"); pg.wait_for_timeout(200)
    print("이름 없이 다음 막힘:", pg.is_visible("#q-who .err-msg"))
    pg.click("#who-list >> text=최유나 선배님"); print("위 이름표:", pg.inner_text("#brand"))
    pg.screenshot(path=str(OUT / "1b_who.png"), full_page=True)
    pg.click("#who-next"); pg.wait_for_timeout(300)
    # 이름 없이 다음 → 오류
    pg.click("#task-next"); pg.wait_for_timeout(200)
    print("이름 없을 때 오류 표시:", pg.is_visible("#q-name .err-msg"))
    pg.click("#s-task [data-field=kind] >> text=문서·보고서 만들기")
    pg.click("#s-task [data-field=way] >> text=기타"); pg.fill("#s-task [data-etc=way]", "데이터 받으면 정해진 틀대로, 해석은 판단")
    pg.fill("#f-tools", "Excel, Teams, Figma")
    pg.click("#s-task [data-field=where] >> text=내 PC"); pg.click("#s-task [data-field=where] >> text=기타"); pg.fill("#s-task [data-etc=where]", "카톡방")
    pg.click("#s-task [data-field=help] >> text=크다")
    # 파일 고르기
    pg.click(".att[data-q=kind] .att-btn") if False else None; pg.set_input_files("#f-file", IMG); pg.wait_for_timeout(800)
    # 붙여 넣기(Ctrl+V) 흉내
    b64 = base64.b64encode(open(IMG, 'rb').read()).decode()
    pg.evaluate("""async (b64) => { const bin=atob(b64); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
      const f=new File([u],'clip.png',{type:'image/png'}); const dt=new DataTransfer(); dt.items.add(f);
      document.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true})); }""", b64)
    pg.wait_for_timeout(800)
    # 끌어 놓기 흉내
    pg.evaluate("""async (b64) => { const bin=atob(b64); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
      const f=new File([u],'drag.png',{type:'image/png'}); const dt=new DataTransfer(); dt.items.add(f);
      document.querySelector('.att[data-q=where]').closest('.q').dispatchEvent(new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true})); }""", b64)
    pg.wait_for_timeout(800)
    print("일 1 스크린샷 수(파일·붙여넣기·끌어놓기):", pg.locator("#s-task .thumb").count(), "| 문항별:", {q: pg.locator(f".att[data-q={q}] .thumb").count() for q in ["kind","tools","where"]})
    pg.screenshot(path=str(OUT / "2_task1.png"), full_page=True)
    pg.click("#add-task"); pg.wait_for_timeout(300); print("아래 버튼 추가 후 탭:", pg.inner_text(".steps").replace(chr(10)," "), "/ 일2에서 아래 버튼 보임:", pg.is_visible("#add-task"))
    print("두 번째 일 제목:", pg.inner_text("#t-task"))
    pg.click("#s-task .mtg [data-m=rec]"); pg.wait_for_timeout(200); print("추천 개수(최유나):", pg.locator("#rec-grid .chip").count()); pg.screenshot(path=str(OUT / "2b_rec.png"), full_page=True); pg.locator("#rec-grid .chip").nth(1).click(); pg.click("#s-task [data-field=way] >> text=매번 같은 방식으로 한다"); pg.click("#s-task [data-field=help] >> text=작다")
    pg.click("#task-next"); pg.wait_for_timeout(300)
    pg.locator("#check-list .chip").nth(1).click(); pg.wait_for_timeout(200); pg.locator("#check-list .man-row").nth(1).locator("input").fill("번역 최종본은 직접 한 줄씩 대조"); print("손으로 칸 보임(일2):", pg.locator("#check-list .man-row").nth(1).locator("input").is_visible(), "/ 일1 칸 숨김:", not pg.locator("#check-list .man-row").nth(0).locator("input").is_visible()); pg.screenshot(path=str(OUT / "3a_last.png"), full_page=True)
    print("보내기 화면 바로:", pg.is_visible("#s-send"), "| 탭:", pg.inner_text(".steps").replace(chr(10)," ")); pg.wait_for_timeout(200)
    pg.screenshot(path=str(OUT / "3_send.png"), full_page=True)
    pg.locator("#summary .imgs img").first.click(); pg.wait_for_timeout(200); print("크게 보기 열림:", pg.is_visible("#zoom img")); pg.screenshot(path=str(OUT / "3z_zoom.png")); pg.keyboard.press("Escape"); pg.wait_for_timeout(200); print("Esc 닫힘:", not pg.is_visible("#zoom"))
    pg.click(".steps >> text=일 1"); pg.wait_for_timeout(300); a=pg.inner_text("#t-task")
    pg.click(".steps >> text=일 2"); pg.wait_for_timeout(300); b2=pg.inner_text("#t-task")
    pg.click(".steps >> text=보내기"); pg.wait_for_timeout(300)
    print("탭 이동:", a, "→", b2, "→ 보내기 화면:", pg.is_visible("#s-send"))
    with pg.expect_download() as dl:
        pg.click("#make-eml")
    d = dl.value; print("저장 파일 이름:", d.suggested_filename); d.save_as(str(OUT / "answer.eml")); pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "4_done.png"))
    # 뒤로 가기 확인
    print("오류:", errs or "없음")
    m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, color_scheme="dark")
    m.goto(url); m.wait_for_timeout(300); m.screenshot(path=str(OUT / "5a_mobile_start.png"), full_page=True); m.click("text=시작하기"); m.click("#who-list >> text=임태오 선배님"); m.click("#who-next"); m.wait_for_timeout(300)
    m.click("#s-task .mtg [data-m=rec]"); m.wait_for_timeout(200)
    print("휴대폰 가로 넘침:", m.evaluate("document.documentElement.scrollWidth"))
    m.screenshot(path=str(OUT / "5_mobile_dark.png"), full_page=True)
    b.close()
msg = BytesParser(policy=policy.default).parsebytes((OUT / "answer.eml").read_bytes())
print("메일 받는 사람:", msg["To"], "| 제목:", msg["Subject"], "| X-Unsent:", msg["X-Unsent"])
print("첨부:", [a.get_filename() for a in msg.iter_attachments()])
print(msg.get_body(("plain",)).get_content())
