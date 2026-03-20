import asyncio
import pandas as pd
from scraper.pipeline import scrape_all
from scraper.validator import clean_data, USE_LLM

async def run():
    data = await scrape_all()
    data = clean_data(data)

    df = pd.DataFrame(data)
    df.to_csv("output/data.csv", index=False)
    df.to_json("output/data.json", orient="records")

    print("Scraping completed. Data saved.")
print(f"LLM Enabled: {USE_LLM}")
if __name__ == "__main__":
    asyncio.run(run())