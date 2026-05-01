from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_reply(subject: str, body: str) -> str:
    try:
        prompt = f"""
        You are a professional email assistant.

        Subject: {subject}
        Email: {body}

        Generate a clear, polite, and professional reply.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")