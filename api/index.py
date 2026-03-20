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
def scrape():
    try:
        all_books = run_pipeline(BASE_URL)

        # Optional cleaning (LLM disabled or enabled)
        cleaned = clean_data(all_books[:50])  # limit for speed

        return {
            "count": len(cleaned),
            "data": cleaned
        }

    except Exception as e:
        return {"error": str(e)}