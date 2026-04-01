from pydantic import BaseModel, Field

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
