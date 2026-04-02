from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.entry import EntryCreate, EntryResponse, EntryAnalysisResponse, EntryRead
from app.services.entry import process_entry, analyze_entry, get_all_entries

router = APIRouter()

@router.get("/entries", response_model=list[EntryRead])
def get_entries(limit: int = 50, db: Session = Depends(get_db)):
    return get_all_entries(db=db, limit=limit)

@router.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    return process_entry(db, entry)

@router.post("/entries/analyze", response_model=EntryAnalysisResponse)
def analyze_thought_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    return analyze_entry(db, entry)
