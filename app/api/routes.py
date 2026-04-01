from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.entry import EntryCreate, EntryResponse, EntryAnalysisResponse
from app.services.entry import process_entry, analyze_entry

router = APIRouter()

@router.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    return process_entry(db, entry)

@router.post("/entries/analyze", response_model=EntryAnalysisResponse)
def analyze_thought_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    return analyze_entry(db, entry)
