import json
import os
from typing import Any

from groq import Groq

SYSTEM_PROMPT = """You are a technical assistant that writes concise, professional summaries of detected differences between two versions of a CAD/engineering drawing. Given structured difference statistics, output a JSON object with two keys:
1. "overall_summary": ONE paragraph (3-5 sentences) describing the overall comparison result, major changed regions, and severity. Do not invent details not present in the input data.
2. "region_descriptions": An array of objects where each object has:
   - "number": the region's assigned number.
   - "description": one short sentence describing the region using its type, location, and stats.

Output ONLY valid JSON. Do not include any markdown wrappers like ```json."""


def generate_summary(stats: dict[str, Any]) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"overall_summary": "AI summary unavailable because GROQ_API_KEY is not configured.", "region_descriptions": []}

    client = Groq(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(stats)},
            ],
            temperature=0.3,
            max_tokens=600,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error generating summary: {e}")
        return {"overall_summary": "Error generating AI summary.", "region_descriptions": []}
