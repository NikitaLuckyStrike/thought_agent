from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.entry import EntryCreate, EntryResponse, EntryAnalysisResponse
from app.models.entry import Entry

def _normalize_text(text: str) -> str:
    stripped_text = text.strip()
    if not stripped_text:
        raise HTTPException(
            status_code=422,
            detail="original_text must not be empty"
        )
    return stripped_text

def process_entry(db: Session, payload: EntryCreate) -> EntryResponse:
    stripped_text = _normalize_text(payload.original_text)
    
    db_entry = Entry(original_text=stripped_text)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return EntryResponse(original_text=db_entry.original_text)

def analyze_entry(db: Session, payload: EntryCreate) -> EntryAnalysisResponse:
    stripped_text = _normalize_text(payload.original_text)
    
    summary = f"Stub summary: {stripped_text}"
    tags = ["thought", "stub", "analysis"]
    emotion = "neutral"
    intent = "reflection"
    insight = "This is a stub analysis result."
    
    db_entry = Entry(
        original_text=stripped_text,
        summary=summary,
        tags=tags,
        emotion=emotion,
        intent=intent,
        insight=insight
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return EntryAnalysisResponse(
        original_text=db_entry.original_text,
        summary=db_entry.summary,
        tags=db_entry.tags,
        emotion=db_entry.emotion,
        intent=db_entry.intent,
        insight=db_entry.insight
    )
