from app.core.database import engine
from app.models.email_model import Base
from app.models.user_model import User

Base.metadata.create_all(bind=engine)