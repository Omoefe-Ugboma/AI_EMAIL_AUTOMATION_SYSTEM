from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_department_config(category: str):
    """Return department name + signature based on category."""
    mapping = {
        "finance": {
            "department": "Finance Department",
            "signature": "Finance Support Team\nUniversity Finance Office\nfinance@university.com"
        },
        "admissions": {
            "department": "Admissions Office",
            "signature": "Admissions Team\nUniversity Admissions Office\nadmissions@university.com"
        },
        "academic": {
            "department": "Academic Affairs",
            "signature": "Academic Support Team\nUniversity Academic Office\nacademic@university.com"
        },
        "complaint": {
            "department": "Support Team",
            "signature": "Customer Support Team\nUniversity Help Desk\nsupport@university.com"
        },
        "inquiry": {
            "department": "General Enquiries",
            "signature": "Information Desk\nUniversity Support Center\ninfo@university.com"
        },
        "general": {
            "department": "Support Team",
            "signature": "Support Team\nUniversity Support\nsupport@university.com"
        }
    }

    return mapping.get(category, mapping["general"])


def generate_reply(
    category: str,
    subject: str,
    body: str,
    recipient_name: str = "Customer",
    tone: str = "professional"
):
    config = get_department_config(category)
    department = config["department"]
    signature = config["signature"]

    prompt = f"""
You are a professional AI assistant working in the {department}.

Write a clear, human-like email reply.

RULES:
- Address recipient by name: {recipient_name}
- Do NOT use placeholders like [Your Name]
- Do NOT use brackets anywhere
- Keep response natural and realistic
- Be helpful and specific
- Match this tone: {tone}

STRUCTURE:
1. Greeting using name
2. Acknowledge the issue clearly
3. Provide helpful response or next steps
4. Offer further assistance
5. End with signature

SIGNATURE:
Best regards,
{signature}

EMAIL:
Subject: {subject}
Body: {body}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()