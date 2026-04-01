from sqlalchemy.orm import Session
from app.models.entry import Entry
from app.schemas.entry import EntryCreate

def create_entry(db: Session, entry_in: EntryCreate) -> Entry:
    db_entry = Entry(original_text=entry_in.original_text)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
