from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.entry import EntryCreate, EntryResponse
from app.services.entry import create_entry

router = APIRouter()

@router.post("/entries", response_model=EntryResponse)
def create_new_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    return create_entry(db=db, entry_in=entry)

@router.get("/health")
def health_check():
    return {"status": "ok"}
