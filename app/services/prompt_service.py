def build_prompt(category: str, subject: str, body: str) -> str:

    if category == "complaint":
        tone = "apologetic and empathetic"
    elif category == "request":
        tone = "helpful and professional"
    elif category == "inquiry":
        tone = "informative and friendly"
    elif category == "feedback":
        tone = "appreciative and positive"
    else:
        tone = "professional"

    return f"""
    You are a professional email assistant.

    The email category is: {category}.
    Respond in a {tone} tone.

    Subject: {subject}
    Email: {body}

    Generate a clear and professional reply.
    """