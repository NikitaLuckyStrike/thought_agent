from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EntryCreate(BaseModel):
    original_text: str = Field(..., min_length=1, max_length=10000)

class EntryResponse(BaseModel):
    original_text: str

class EntryAnalysisResponse(BaseModel):
    original_text: str
    summary: str
    tags: list[str]
    emotion: str
    intent: str
    insight: str

class EntryRead(BaseModel):
    id: int
    original_text: str
    summary: str | None
    tags: list[str] | None
    emotion: str | None
    intent: str | None
    insight: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
