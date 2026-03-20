from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper.fetcher import fetch_page
from scraper.parser import parse_books
from scraper.pipeline import scrape_all
from scraper.validator import clean_data
from scraper.config import BASE_URL

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is live 🚀"}


@app.post("/scrape")
async def scrape():
    try:
        data = await scrape_all()

        if not data:
            return {"data": []}

        return {"data": data[:50]}

    except Exception as e:
        print("SCRAPE ERROR:", e)
        return {"data": []}