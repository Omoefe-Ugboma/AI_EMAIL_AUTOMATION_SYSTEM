from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    subject: str = Field(..., min_length=3, max_length=200)
    body: str = Field(..., min_length=5)