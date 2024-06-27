from typing import Optional
from pydantic import BaseModel


class SMemeBase(BaseModel):
    file_name: str
    text: Optional[str]


class SMemeRead(SMemeBase):
    id: int


class SAddedId(BaseModel):
    id_added_meme: int