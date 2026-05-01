from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas.email_schema import EmailRequest
from app.services.classifier import classify_email
from app.services.ai_service import generate_reply
from app.services.db_service import save_email
from app.utils.helpers import normalize_category
from app.core.security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

# 🔐 AUTH FUNCTION
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# 🚀 PROTECTED ROUTE
@router.post("/generate-reply")
def generate_email_reply(
    request: EmailRequest,
    user=Depends(get_current_user)
):
    try:
        # 🧠 Step 1: classify email
        raw_category = classify_email(request.subject, request.body)

        # 🔧 Step 2: normalize category
        category = normalize_category(raw_category)

        # 🤖 Step 3: generate AI reply
        reply = generate_reply(
            category,
            request.subject,
            request.body
        )

        # 💾 Step 4: save to database
        save_email(
            request.subject,
            request.body,
            category,
            reply
        )

        # 📊 Step 5: logging
        print(f"[INFO] User: {user.get('sub')} | Category: {category}")

        # 📦 Step 6: return response
        return {
            "status": "success",
            "user": user.get("sub"),
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
        raise HTTPException(status_code=500, detail=str(e))