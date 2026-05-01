from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class EmailLog(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    body = Column(Text)
    category = Column(String(50))
    reply = Column(Text)