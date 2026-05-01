from app.core.database import SessionLocal
from app.models.email_model import EmailLog

def save_email(subject, body, category, reply):
    db = SessionLocal()

    email = EmailLog(
        subject=subject,
        body=body,
        category=category,
        reply=reply
    )

    db.add(email)
    db.commit()
    db.close()