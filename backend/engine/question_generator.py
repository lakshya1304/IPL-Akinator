import os
import google.generativeai as genai
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(
    api_key=api_key
)


def generate_dynamic_question(memory, candidates, asked_questions):

    import random

    prompt = f"""
You are an IPL AI expert.

Conversation:
{memory}

Top candidates:
{candidates}

Rules:
- Ask ONE yes/no question
- Avoid repetition
- Be strategic
- Be slightly unpredictable (not obvious sequence)
- Mix logic + intuition
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        q = response.text.strip()

        # 🔥 avoid repeat
        if q in asked_questions:
            return random.choice([
                "Is your player known for aggressive batting?",
                "Has your player played for multiple IPL teams?",
                "Is your player under 30 years old?",
                "Is your player a match winner?",
                "Is your player popular among fans?"
            ])

        return q

    except:
        return "Is your player currently active in IPL?"