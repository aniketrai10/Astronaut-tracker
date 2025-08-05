import asyncio
from playwright.async_api import async_playwright

MOBILE = "8787081154"
PASSWORD = "aniket10"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Login page open
        await page.goto("https://1wayez.life/")
        await page.fill("input[name='phone']", MOBILE)
        await page.fill("input[name='password']", PASSWORD)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)  # wait after login

        # 2. Astronaut game open
        await page.goto("https://1wayez.life/casino/play/v_100hp:Astronaut?sub1=9UzvI6q0P3")
        await page.wait_for_timeout(10000)  # wait to load game

        # 3. Fetch crash multiplier text (dummy selector - needs adjustment)
        try:
            element = await page.wait_for_selector("div.multiplier", timeout=10000)
            value = await element.inner_text()
            print(f"Current crash multiplier: {value}")
        except:
            print("Multiplier not found - may need different selector or verification blocked.")

        await browser.close()

asyncio.run(run())
