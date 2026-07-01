import os
from typing import Any

from groq import Groq

SYSTEM_PROMPT = """You are a technical assistant that writes concise, professional summaries of detected differences between two versions of a CAD/engineering drawing. Given structured difference statistics, write ONE paragraph (3-5 sentences) describing: overall comparison result, major changed regions and their approximate location, severity/extent, and do not invent details not present in the input data. Do not use markdown formatting. Write plain prose."""


def generate_summary(stats: dict[str, Any]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "AI summary unavailable because GROQ_API_KEY is not configured."

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": str(stats)},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
