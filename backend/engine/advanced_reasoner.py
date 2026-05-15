import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(
    api_key=api_key
)


def generate_contextual_reasoning(
    memory,
    candidates
):

    prompt = f"""
You are an elite IPL analyst AI.

Current deduction path:
{memory}

Top candidates:
{candidates}

Generate:
- expert reasoning
- intelligent deduction
- short analysis
- sound highly analytical
"""

    try:

        response = client.models.generate_content(

            model="gemini-1.5-flash",

            contents=prompt
        )

        return response.text.strip()

    except:

        return (
            "Analyzing tactical IPL patterns..."
        )