from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY"
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