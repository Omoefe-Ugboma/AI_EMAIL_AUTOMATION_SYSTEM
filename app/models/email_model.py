from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from app.core.database import Base

class EmailLog(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    body = Column(Text)
    category = Column(String)
    reply = Column(Text)
    action = Column(String)
    response_time = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))