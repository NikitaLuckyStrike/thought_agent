from pydantic import BaseModel
from datetime import datetime

class EntryCreate(BaseModel):
    original_text: str

class EntryResponse(BaseModel):
    id: int
    original_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
