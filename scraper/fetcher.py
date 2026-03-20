from playwright.async_api import async_playwright

# 🔥 Global browser instance
_browser = None
_playwright = None


async def get_browser():
    global _browser, _playwright

    if _browser is None:
        _playwright = await async_playwright().start()

        _browser = await _playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

    return _browser


async def fetch_page(url):
    try:
        browser = await get_browser()
        page = await browser.new_page()

        await page.goto(url, timeout=15000)
        content = await page.content()

        await page.close()
        return content

    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None