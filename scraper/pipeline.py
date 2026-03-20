import asyncio
from urllib.parse import urljoin
from scraper.config import MAX_BOOKS
from scraper.fetcher import fetch_page
from scraper.parser import extract_book_links, parse_book, next_page
from utils.logger import setup_logger

logger = setup_logger()


async def scrape_all():
    # ✅ Correct starting URL
    current_url = "https://books.toscrape.com/catalogue/page-1.html"

    all_data = []

    # ✅ Limit concurrency (important for Render)
    semaphore = asyncio.Semaphore(5)

    async def sem_fetch(url):
        async with semaphore:
            try:
                return await asyncio.wait_for(fetch_page(url), timeout=10)
            except Exception as e:
                logger.error(f"Timeout/Error fetching {url}: {e}")
                return None

    while current_url:
        logger.info(f"Processing Index: {current_url}")

        html = await sem_fetch(current_url)

        if not html:
            logger.error(f"Failed to load page: {current_url}")
            break

        # ✅ Extract links
        raw_links = extract_book_links(html)
        links = [urljoin(current_url, link) for link in raw_links]

        logger.info(f"Extracted {len(links)} links")
        if links:
            print("Sample links:", links[:3])

        # ✅ Fetch book pages concurrently
        tasks = [sem_fetch(link) for link in links]
        pages = await asyncio.gather(*tasks)

        for p in pages:
            if p:
                try:
                    data = parse_book(p)
                    if data:
                        all_data.append(data)
                except Exception as e:
                    logger.error(f"Parsing error: {e}")
        # ✅ ADD THIS BLOCK HERE (VERY IMPORTANT POSITION)
        if len(all_data) >=MAX_BOOKS:
            logger.info("Stopping early (limit reached)")
            break

        # ✅ FIXED pagination (NO urljoin needed)
        current_url = next_page(html)

        if not current_url:
            logger.info("No more pages found. Finishing...")

    logger.info(f"Scraping complete. Total books: {len(all_data)}")

    return all_data