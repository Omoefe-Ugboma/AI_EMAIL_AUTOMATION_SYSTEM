from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.core.database import SessionLocal
from app.models.user_model import User
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_token
from app.api.routes import get_current_user  # reuse auth dependency

router = APIRouter(prefix="/auth", tags=["Authentication"])


# 🧾 Request Schema
class UserRequest(BaseModel):
    email: EmailStr
    password: str


# 🚀 REGISTER
@router.post("/register")
def register(request: UserRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == request.email).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Account already exists. Please login instead."
            )

        new_user = User(
            email=request.email,
            password=hash_password(request.password)
        )

        db.add(new_user)
        db.commit()

        return {
            "status": "success",
            "message": "User registered successfully"
        }

    finally:
        db.close()


# 🔑 LOGIN
@router.post("/login")
def login(request: UserRequest):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == request.email).first()

        if not user or not verify_password(request.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = create_token({"sub": user.email})

        return {
            "status": "success",
            "data": {
                "access_token": token,
                "token_type": "bearer"
            }
        }

    finally:
        db.close()


# 👤 GET CURRENT USER (STANDARD API ENDPOINT)
@router.get("/me")
def get_current_user_info(user=Depends(get_current_user)):
    return {
        "status": "success",
        "data": {
            "email": user.get("sub")
        }
    }