import requests
import json
import re
import time

# Toggle LLM usage
USE_LLM = False  # set False for deployment if needed


def extract_json_strict(text):
    """
    Extract valid JSON object from messy LLM output
    """
    try:
        # Remove markdown if present
        text = text.replace("```json", "").replace("```", "")

        # Extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return None


def validate_with_llm_local(record):
    if not USE_LLM:
        return record

    prompt = f"""
    You MUST return ONLY valid JSON.

    No explanation.
    No extra text.
    No markdown.

    Format:
    {{
      "title": string,
      "price": float,
      "availability": string
    }}

    Data:
    {record}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",   # or "llama3"
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )

        result = response.json()["response"].strip()

        # Strict JSON extraction
        parsed = extract_json_strict(result)

        if parsed:
            return parsed
        else:
            return record  # silent fallback (no errors)

    except:
        return record

    finally:
        time.sleep(0.5)  # prevent overload


def clean_data(data):
    cleaned = []

    for i, d in enumerate(data):
        try:
            d["price"] = float(d["price"].replace("£", ""))
        except:
            d["price"] = None

        # Apply LLM only to first 500
        if i < 500:
            validated = validate_with_llm_local(d)
        else:
            validated = d

        cleaned.append(validated)

    return cleaned