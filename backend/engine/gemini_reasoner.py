from google import genai


client = genai.Client(
    api_key="AIzaSyDRknSuXKdf-UVfhi9GdlVec-94gw3v-BI"
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