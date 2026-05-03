from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def classify_email_rule(subject: str, body: str) -> str:
    text = (subject + " " + body).lower()

    # 💰 Finance
    if any(word in text for word in [
        "payment", "invoice", "fee", "tuition", "refund", "billing"
    ]):
        return "finance"

    # 🎓 Admissions
    if any(word in text for word in [
        "admission", "apply", "application", "enroll", "intake"
    ]):
        return "admissions"

    # 📚 Academic
    if any(word in text for word in [
        "course", "exam", "lecture", "result", "assignment"
    ]):
        return "academic"

    # ⚠️ Complaint
    if any(word in text for word in [
        "complaint", "bad", "issue", "problem", "not happy"
    ]):
        return "complaint"

    # ❓ Inquiry
    if any(word in text for word in [
        "help", "question", "information", "details"
    ]):
        return "inquiry"

    return "general"

def classify_email_ai(subject: str, body: str) -> str:
    prompt = f"""
Classify this email into ONE of the following categories ONLY:

finance
admissions
academic
complaint
inquiry
general

Do NOT return anything else.

Email:
Subject: {subject}
Body: {body}

Return ONLY the category.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content.strip().lower()

    allowed = ["finance", "admissions", "academic", "complaint", "inquiry", "general"]

    if result in allowed:
        return result

    return "general"

def classify_email(subject: str, body: str) -> str:
    rule_result = classify_email_rule(subject, body)

    # If rule is confident, use it
    if rule_result != "general":
        return rule_result

    # Otherwise fallback to AI
    return classify_email_ai(subject, body)


def rule_based_classification(text: str):
    text = text.lower()

    if any(x in text for x in ["invoice", "payment", "fee"]):
        return "finance"

    if "admission" in text or "apply" in text:
        return "admissions"

    if any(x in text for x in ["exam", "result", "course"]):
        return "academic"

    if any(x in text for x in ["not happy", "bad", "complaint"]):
        return "complaint"

    return None