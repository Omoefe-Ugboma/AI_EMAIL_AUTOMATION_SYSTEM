from app.core.database import engine
from app.models.email_model import Base

Base.metadata.create_all(bind=engine)