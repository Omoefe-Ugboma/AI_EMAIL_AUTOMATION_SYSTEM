from fastapi import APIRouter, HTTPException
from app.schemas.email_schema import EmailRequest
from app.services.classifier import classify_email
from app.services.ai_service import generate_reply
from app.utils.helpers import normalize_category

router = APIRouter()


@router.post("/generate-reply")
def generate_email_reply(request: EmailRequest):
    try:
        # Step 1: classify
        raw_category = classify_email(request.subject, request.body)

        # Step 2: normalize
        category = normalize_category(raw_category)

        # Step 3: generate reply
        reply = generate_reply(
            category,
            request.subject,
            request.body
        )

        # Step 4: logging (important)
        print(f"[INFO] Category: {category} | Subject: {request.subject}")

        # Step 5: return structured response
        return {
            "status": "success",
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