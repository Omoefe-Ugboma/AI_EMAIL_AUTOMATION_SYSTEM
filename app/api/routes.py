from fastapi import APIRouter, HTTPException
from app.schemas.email_schema import EmailRequest
from app.services.ai_service import generate_reply

router = APIRouter()

@router.post("/generate-reply")
def generate_email_reply(request: EmailRequest):
    try:
        reply = generate_reply(request.subject, request.body)
        return {
            "status": "success",
            "data": {"reply": reply}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
