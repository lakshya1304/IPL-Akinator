import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(
    api_key=api_key
)


def generate_reasoning(
    player,
    confidence,
    remaining
):

    prompt = f"""
You are an IPL analyst AI.

Top predicted player:
{player}

Confidence:
{confidence}

Remaining candidates:
{remaining}

Generate:
- one short reasoning line
- sound like cricket expert
- under 20 words
"""

    try:

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except:

        return (
            "Analyzing IPL player patterns..."
        )