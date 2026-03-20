from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS FIX (CRITICAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is live 🚀"}

# VERY IMPORTANT: allow POST
@app.post("/scrape")
def scrape():
    # TEMP TEST RESPONSE (to debug)
    return {
        "data": [
            {
                "title": "Test Book",
                "price": 20,
                "availability": "In stock"
            }
        ]
    }