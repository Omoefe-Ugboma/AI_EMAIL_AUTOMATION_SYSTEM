from openai import OpenAI
from app.core.config import settings
from app.services.prompt_service import build_prompt

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_reply(category, subject, body, recipient_name="Customer"):
    prompt = f"""
You are a professional university support assistant.

Write a clear, polite, and human-like email reply.

Rules:
- Address the recipient by name: {recipient_name}
- Do NOT use placeholders like [Your Name]
- Do NOT use brackets anywhere
- Keep it professional and concise
- Tailor the response to the category: {category}

Signature:
Best regards,
AI Support Team
University Support Department
support@university.com

Email Subject: {subject}
Email Content: {body}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content