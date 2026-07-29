"""
Gemini sometimes wraps JSON in ```json fences or adds a stray sentence
before/after the object. This helper extracts and parses the JSON safely
so routes never crash on a malformed model response.
"""
import json
import re
from fastapi import HTTPException


def extract_json(raw_text: str) -> dict:
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=502, detail="Empty response from AI model.")

    text = raw_text.strip()

    # Strip ```json ... ``` or ``` ... ``` fences
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    # Fall back to grabbing the outermost { ... } block
    if not text.startswith("{"):
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not parse AI response as JSON: {exc}",
        ) from exc
