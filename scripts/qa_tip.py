# survey-form 스킬 QA 예시(assets/survey_template.html 예시 기준). 클릭하는 이름·보기 글자를 새 설문에 맞게 바꿔 쓴다.
import sys, pathlib
from playwright.sync_api import sync_playwright
url = pathlib.Path(sys.argv[1]).resolve().as_uri(); OUT = pathlib.Path(sys.argv[2])
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge"); errs=[]
    pg = b.new_page(viewport={"width":1280,"height":900}); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT/"t1_start.png"))
    pg.click("text=시작하기"); pg.click("#who-list >> text=오서연 선배님"); pg.click("#who-next"); pg.wait_for_timeout(300)
    print("말풍선 처음:", pg.is_visible("#rec-tip"))
    pg.hover(".hlp-b"); pg.wait_for_timeout(200); print("물음표 올림:", pg.is_visible("#rec-tip"))
    pg.screenshot(path=str(OUT/"t2_hover.png"), clip={"x":250,"y":0,"width":780,"height":460})
    pg.mouse.move(5,5); pg.wait_for_timeout(200); print("내림:", pg.is_visible("#rec-tip"))
    m = b.new_page(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True, color_scheme="dark"); m.on("pageerror", lambda e: errs.append(str(e)))
    m.goto(url); m.click("text=시작하기"); m.click("#who-list >> text=오서연 선배님"); m.click("#who-next"); m.wait_for_timeout(300)
    m.tap(".hlp-b"); m.wait_for_timeout(200); print("폰 탭:", m.is_visible("#rec-tip"), "| 추천 켜짐:", m.get_attribute("[data-m=rec]","aria-pressed"), "| 넘침:", m.evaluate("document.documentElement.scrollWidth"))
    m.screenshot(path=str(OUT/"t3_mobile.png"))
    m.tap("#q-name .att-btn"); m.wait_for_timeout(200); print("다른 데 탭 닫힘:", not m.is_visible("#rec-tip"))
    print("오류:", errs or "없음"); b.close()
