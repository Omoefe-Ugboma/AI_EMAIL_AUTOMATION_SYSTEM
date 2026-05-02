from app.core.database import SessionLocal
from app.models.email_model import EmailLog

def save_email(subject, body, category, reply, action, response_time, user_id):
    db = SessionLocal()

    email = EmailLog(
        subject=subject,
        body=body,
        category=category,
        reply=reply,
        action=action,
        response_time=response_time,
        user_id=user_id
    )

    db.add(email)
    db.commit()
    db.close()