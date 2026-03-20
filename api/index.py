from fastapi import FastAPI
import asyncio
from scraper.pipeline import scrape_all
from scraper.validator import clean_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is live 🚀"}

@app.get("/scrape")
async def scrape():
    data = await scrape_all()
    data = clean_data(data)

    return {
        "total": len(data),
        "sample": data[:10]
    }