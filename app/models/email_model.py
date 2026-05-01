from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

user_id = Column(Integer, ForeignKey("users.id"))

class EmailLog(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    body = Column(Text)
    category = Column(String(50))
    reply = Column(Text)