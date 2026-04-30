import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_reply(subject: str, body: str) -> str:
    try:
        prompt = f"""
        You are a professional email assistant.

        Subject: {subject}
        Email: {body}

        Generate a clear, polite, and professional reply.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error generating response: {str(e)}"