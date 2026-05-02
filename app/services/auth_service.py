from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔐 Hash password safely (avoid bcrypt 72-byte limit)
def hash_password(password: str):
    safe_password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(safe_password)


# 🔍 Verify password
def verify_password(plain: str, hashed: str):
    safe_password = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(safe_password, hashed)