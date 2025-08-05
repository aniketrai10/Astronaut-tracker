from playwright.sync_api import sync_playwright

USERNAME = "8787081154"
PASSWORD = "aniket10"
LOGIN_URL = "https://1wayez.life/"
GAME_URL = "https://1wayez.life/casino/play/v_100hp:Astronaut?sub1=9UzvI6q0P3"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Login
    page.goto(LOGIN_URL)
    page.fill('input[name="phone"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)  # wait for login

    # Open Game
    page.goto(GAME_URL)
    print("Game page opened successfully!")
    page.wait_for_timeout(10000)  # keep it open for 10 sec

    browser.close()
