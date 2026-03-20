import asyncio
from urllib.parse import urljoin
from scraper.fetcher import fetch_page
from scraper.parser import extract_book_links, parse_book, next_page
from utils.logger import setup_logger

logger = setup_logger()

async def scrape_all():
    # STARTING POINT
    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    current_url = urljoin(base_url, "page-1.html")
    all_data = []
    
    # Limit concurrency to 10 requests at a time
    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            return await fetch_page(url)

    while current_url:
        logger.info(f"Processing Index: {current_url}")
        html = await fetch_page(current_url)
        
        if not html:
            logger.error(f"Failed to load page: {current_url}")
            break

        # FIX #2 & #3: Extract links and add Debugging
        raw_links = extract_book_links(html)
        links = [urljoin(current_url, link) for link in raw_links]
        
        # DEBUG LOGGING (Fix #3)
        logger.info(f"Extracted {len(links)} links")
        if links:
            print("Sample links:", links[:3])

        # Fetch all books on this page concurrently
        tasks = [sem_fetch(link) for link in links]
        pages = await asyncio.gather(*tasks, return_exceptions=True)
        
        for p in pages:
            if p and not isinstance(p, Exception):
                data = parse_book(p)
                if data:
                    all_data.append(data)

        # FIX #4: Updated Next Page Logic
        # We pass the current_url as the base to the parser's logic
        next_rel_path = next_page(html) 
        if next_rel_path:
            # Resolves paths like 'page-2.html' against the current full URL
            current_url = urljoin(current_url, next_rel_path)
        else:
            logger.info("No more pages found. Finishing...")
            current_url = None 

    logger.info(f"Scraping complete. Total books: {len(all_data)}")
    return all_data
