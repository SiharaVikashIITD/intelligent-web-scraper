# Intelligent Web Scraper with LLM Validation

An advanced Python-based web scraping system that extracts structured data from dynamic, multi-level websites and optionally enhances it using a local LLM (Ollama).

---

## 🚀 Features

- Multi-page web scraping (50+ pages)
- Async processing with concurrency control
- Dynamic content handling
- Structured data output (CSV, JSON)
- Logging & debugging support
- Optional AI-based validation using Ollama (local LLM)
- Fault-tolerant pipeline (LLM failures do not break system)

---

## 🧠 Architecture

Scraper → Parser → Data Cleaner → LLM Validation (Optional) → Output

---

## 📊 Output

- `output/data.csv`
- `output/data.json`

---

## ⚙️ Installation

```bash
git clone https://github.com/SiharaVikashIITD/intelligent-web-scraper.git
cd intelligent-web-scraper
pip install -r requirements.txt
playwright install

▶️ Run Scraper
python main.py
🤖 Optional: LLM Validation (Local)

Install Ollama:

https://ollama.com

Run:

ollama run mistral
🌐 API
uvicorn api.index:app --reload

🛠 Tech Stack

Python
Playwright
BeautifulSoup
Pandas
FastAPI

Ollama (Local LLM)

💡 Highlights

Handles multi-level site structures

Implements resilient scraping strategies

Integrates AI with fallback-safe design

Designed for scalability and production use

📌 Future Improvements

Proxy rotation

CAPTCHA handling

Database integration

Frontend dashboard