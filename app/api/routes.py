from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.email_schema import EmailRequest
from app.services.classifier import classify_email
from app.services.ai_service import generate_reply
from app.services.rpa_service import route_email
from app.services.metrics_service import start_timer, end_timer
from app.services.db_service import save_email
from app.services.email_ingest_service import get_incoming_emails
from app.utils.privacy import anonymize_text

from app.core.security import verify_token
from app.core.database import SessionLocal
from app.models.user_model import User
from app.models.email_model import EmailLog

from app.services.gmail_auth import get_gmail_service
from app.services.gmail_reader import fetch_unread_emails
from app.services.gmail_sender import send_reply
import re



router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return verify_token(credentials.credentials)

def extract_email(sender):
    match = re.search(r"<(.+?)>", sender)
    if match:
        return match.group(1).lower()
    return sender.lower()

# 🔥 PROCESS SINGLE EMAIL
@router.post("/generate-reply")
def process_email(request: EmailRequest, user=Depends(get_current_user)):
    db = SessionLocal()

    user_email = user.get("sub")
    db_user = db.query(User).filter(User.email == user_email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    start = start_timer()

    clean_body = anonymize_text(request.body)
    category = classify_email(request.subject, clean_body)
    reply = generate_reply(category, request.subject, clean_body)
    action = route_email(category)

    response_time = end_timer(start)

    save_email(
        request.subject,
        clean_body,
        category,
        reply,
        action,
        response_time,
        db_user.id
    )

    db.close()

    return {
        "status": "success",
        "category": category,
        "action": action,
        "metrics": {"response_time": response_time},
        "data": {"reply": reply}
    }


# 🔥 PROCESS INCOMING EMAILS (SIMULATION)
@router.get("/process-inbox")
def process_inbox(user=Depends(get_current_user)):
    emails = get_incoming_emails()

    results = []
    for email in emails:
        result = process_email(EmailRequest(**email), user)
        results.append(result)

    return results


# 🔥 VIEW USER EMAILS
@router.get("/my-emails")
def get_my_emails(user=Depends(get_current_user)):
    db = SessionLocal()

    user_email = user.get("sub")
    db_user = db.query(User).filter(User.email == user_email).first()

    emails = db.query(EmailLog).filter(EmailLog.user_id == db_user.id).all()

    db.close()

    return [
        {
            "subject": e.subject,
            "category": e.category,
            "action": e.action,
            "reply": e.reply
        }
        for e in emails
    ]
    
@router.get("/gmail-process")
def process_gmail(user=Depends(get_current_user)):
    service = get_gmail_service()

    db = SessionLocal()
    user_email = user.get("sub")

    db_user = db.query(User).filter(User.email == user_email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    emails = fetch_unread_emails(service)

    if not emails:
        return {"message": "No unread emails found"}

    results = []

    for email in emails:
        subject = email["subject"]
        body = email["body"]
        sender = email["sender"]
        msg_id = email["id"]

        sender_email = extract_email(sender)
        user_email = user.get("sub").lower()

        # 🚨 Skip your own emails
        if sender_email == user_email:
            continue

        # 🚨 Prevent reply loops
        if subject.lower().startswith("re:"):
            continue

        # 🚨 Skip system emails
        if "no-reply" in sender_email or "noreply" in sender_email:
            continue

        recipient_name = email.get("name", "Customer")

        start = start_timer()

        category = classify_email(subject, body)
        reply = generate_reply(category, subject, body, recipient_name)
        action = route_email(category)

        send_reply(service, sender, subject, reply)

        # Mark as read
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

        response_time = end_timer(start)

        save_email(
            subject,
            body,
            category,
            reply,
            action,
            response_time,
            db_user.id
        )

        results.append({
            "subject": subject,
            "category": category,
            "action": action,
            "metrics": {
                "response_time": response_time
            }
        })

    db.close()

    return results