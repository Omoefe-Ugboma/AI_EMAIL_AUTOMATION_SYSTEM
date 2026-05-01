from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def classify_email_rule(subject: str, body: str) -> str:
    text = (subject + " " + body).lower()

    if any(word in text for word in ["complaint", "not happy", "bad service", "angry"]):
        return "complaint"

    elif any(word in text for word in ["invoice", "payment", "bill", "request"]):
        return "request"

    elif any(word in text for word in ["how", "what", "can you", "help"]):
        return "inquiry"

    elif any(word in text for word in ["feedback", "suggestion"]):
        return "feedback"

    return "general"

def classify_email_ai(subject: str, body: str) -> str:
    prompt = f"""
    Classify this email into one category:
    complaint, request, inquiry, feedback, general.

    Subject: {subject}
    Body: {body}

    Return only one word.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()

def classify_email(subject: str, body: str) -> str:
    rule_result = classify_email_rule(subject, body)

    # If rule is confident, use it
    if rule_result != "general":
        return rule_result

    # Otherwise fallback to AI
    return classify_email_ai(subject, body)