from openai import OpenAI
from app.core.config import settings
from app.services.prompt_service import build_prompt

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_reply(category: str, subject: str, body: str) -> str:
    try:
        prompt = build_prompt(category, subject, body)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")