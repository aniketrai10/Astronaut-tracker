import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://1wayez.life/casino/play/v_100hp:Astronaut?sub1=9UzvI6q0P3"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = await browser.new_page()
        await page.goto(url)
        await asyncio.sleep(5)  # Page ko load hone do
        content = await page.content()
        print(content[:1000])  # Sirf test ke liye first 1000 chars print karenge
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
