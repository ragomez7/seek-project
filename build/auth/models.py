from pydantic import BaseModel
from datetime import datetime

class UserModel(BaseModel):
    email: str
    hashed_password: str
    created_at: datetime
