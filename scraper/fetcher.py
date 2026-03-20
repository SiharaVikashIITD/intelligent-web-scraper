from playwright.async_api import async_playwright

async def fetch_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content