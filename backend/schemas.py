from pydantic import BaseModel
from typing import Optional

class RecipientBase(BaseModel):
    name: str
    phone_number: str
    group_id: Optional[int] = None

class RecipientCreate(RecipientBase):
    pass

class RecipientUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    group_id: Optional[int] = None

class RecipientOut(RecipientBase):
    id: int

    class Config:
        orm_mode = True 