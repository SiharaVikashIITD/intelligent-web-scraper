from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://books.toscrape.com/"

# ✅ Extract links from listing page
def extract_book_links(html):
    soup = BeautifulSoup(html, "lxml")
    links = []

    for a in soup.select("h3 a"):
        href = a["href"]
        links.append(href)  # keep relative links

    return links


# ✅ Parse single book page
def parse_book(html):
    soup = BeautifulSoup(html, "lxml")

    title = soup.select_one("h1").text
    price = soup.select_one(".price_color").text
    availability = soup.select_one(".availability").text.strip()

    return {
        "title": title,
        "price": price,
        "availability": availability
    }


# ✅ NEW: Parse multiple books (for pipeline compatibility)
def parse_books(html_list):
    books = []

    for html in html_list:
        try:
            book = parse_book(html)
            books.append(book)
        except Exception:
            continue  # skip bad pages

    return books


# ✅ Pagination
def next_page(html):
    soup = BeautifulSoup(html, "lxml")
    nxt = soup.select_one(".next a")

    if nxt:
        return urljoin(BASE + "catalogue/", nxt["href"])

    return None