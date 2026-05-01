from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.database import SessionLocal
from app.models.user_model import User
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


# 🧾 REQUEST SCHEMA
class UserRequest(BaseModel):
    email: EmailStr
    password: str


# 🚀 REGISTER USER
@router.post("/register")
def register(request: UserRequest):
    db = SessionLocal()

    try:
        # 🔍 Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # 🔐 Hash password
        hashed_password = hash_password(request.password)

        # 💾 Create user
        new_user = User(
            email=request.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()

        return {
            "message": "User registered successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


# 🔑 LOGIN USER
@router.post("/login")
def login(request: UserRequest):
    db = SessionLocal()

    try:
        # 🔍 Find user
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # 🔐 Verify password
        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # 🎟️ Generate token
        token = create_token({"sub": user.email})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()