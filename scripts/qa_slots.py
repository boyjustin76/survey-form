# survey-form 스킬 QA 예시(assets/survey_template.html 예시 기준). 클릭하는 이름·보기 글자를 새 설문에 맞게 바꿔 쓴다.
import sys, pathlib
from playwright.sync_api import sync_playwright
url = pathlib.Path(sys.argv[1]).resolve().as_uri(); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(exist_ok=True); IMG=sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge"); ctx=b.new_context(viewport={"width":1280,"height":900}); errs=[]
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.click("text=시작하기"); pg.click("#who-list >> text=오서연 선배님"); pg.click("#who-next"); pg.wait_for_timeout(200)
    pg.click("#s-task [data-field=kind] >> text=숫자 정리(엑셀·지표)"); pg.fill("#f-tools","Excel"); pg.set_input_files("#f-file", IMG); pg.wait_for_timeout(800)
    pg.click("#save-btn"); pg.wait_for_timeout(200); pg.screenshot(path=str(OUT/"a_save_empty.png"))
    pg.locator("#slots .slot").nth(0).click(); pg.wait_for_timeout(600); print("저장 알림:", pg.inner_text(".toast"))
    pg.fill("#f-tools","Excel, Notion"); pg.click("#save-btn"); pg.wait_for_timeout(200)
    pg.locator("#slots .slot").nth(0).click(); pg.wait_for_timeout(200); print("덮어쓰기 경고:", pg.locator("#slots .slot").nth(0).inner_text().replace(chr(10)," "))
    pg.locator("#slots .slot").nth(1).click(); pg.wait_for_timeout(600); print("2번 칸 저장:", pg.inner_text(".toast"))
    pg.reload(); pg.wait_for_timeout(500); pg.click("#load-start"); pg.wait_for_timeout(200)
    print("불러오기 칸:", [pg.locator("#slots .slot").nth(i).inner_text().replace(chr(10)," ") for i in range(3)])
    pg.screenshot(path=str(OUT/"b_load.png"))
    pg.locator("#slots .slot").nth(0).click(); pg.wait_for_timeout(600)
    print("1번 불러옴:", pg.inner_text(".toast"), "/ 툴:", pg.input_value("#f-tools"), "/ 캡처:", pg.locator("#s-task .thumb").count(), "/ 이름표:", pg.inner_text("#brand"))
    pg.click("#load-btn"); pg.wait_for_timeout(200); pg.keyboard.press("Escape"); pg.wait_for_timeout(200); print("Esc 닫힘:", not pg.is_visible("#slots"))
    m = ctx.new_page(); m.set_viewport_size({"width":390,"height":844}); m.emulate_media(color_scheme="dark"); m.goto(url); m.wait_for_timeout(300); m.click("#load-start"); m.wait_for_timeout(200)
    print("폰 넘침:", m.evaluate("document.documentElement.scrollWidth")); m.screenshot(path=str(OUT/"c_mobile.png"))
    print("오류:", errs or "없음"); b.close()
