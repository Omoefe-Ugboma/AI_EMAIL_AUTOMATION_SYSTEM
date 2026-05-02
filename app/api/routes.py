from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.email_schema import EmailRequest
from app.services.classifier import classify_email
from app.services.ai_service import generate_reply
from app.services.db_service import save_email
from app.utils.helpers import normalize_category

from app.core.security import verify_token
from app.core.database import SessionLocal

from app.models.user_model import User
from app.models.email_model import EmailLog


router = APIRouter(tags=["Email"])

# 🔐 Security setup
security = HTTPBearer()


# 🔐 AUTH DEPENDENCY (USED BY ALL PROTECTED ROUTES)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# 🚀 GENERATE EMAIL REPLY (PROTECTED)
@router.post("/generate-reply")
def generate_email_reply(
    request: EmailRequest,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    try:
        # 🔐 Get current user from token
        user_email = user.get("sub")

        db_user = db.query(User).filter(User.email == user_email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # 🧠 Classify email
        raw_category = classify_email(request.subject, request.body)
        category = normalize_category(raw_category)

        # 🤖 Generate reply
        reply = generate_reply(
            category,
            request.subject,
            request.body
        )

        # 💾 Save email (linked to user)
        save_email(
            request.subject,
            request.body,
            category,
            reply,
            db_user.id
        )

        # 📊 Logging
        print(f"[INFO] User: {user_email} | Category: {category}")

        # 📦 Response
        return {
            "status": "success",
            "user": user_email,
            "category": category,
            "meta": {
                "model": "gpt-4o-mini"
            },
            "data": {
                "subject": request.subject,
                "reply": reply
            }
        }

    except Exception as e:
        print("ERROR:", str(e))  # 👈 VERY IMPORTANT
        raise HTTPException(status_code=500, detail=str(e))

    finally:
            db.close()


# 📥 GET USER'S EMAILS ONLY (MULTI-USER SYSTEM)
@router.get("/my-emails")
def get_my_emails(user=Depends(get_current_user)):
    db = SessionLocal()

    try:
        user_email = user.get("sub")

        db_user = db.query(User).filter(User.email == user_email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        emails = db.query(EmailLog).filter(
            EmailLog.user_id == db_user.id
        ).all()

        results = []
        for email in emails:
            results.append({
                "subject": email.subject,
                "category": email.category,
                "reply": email.reply
            })

        return {
            "status": "success",
            "data": results
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        db.close()