from app.db.session import SessionLocal
from app.schemas.entry import EntryCreate
from app.services.entry import analyze_entry

def test():
    db = SessionLocal()
    try:
        print("Testing analyze_entry with Gemini...")
        payload = EntryCreate(
            original_text="Сегодня я понял, что слишком много работаю и совершенно не обращаю внимание на свое здоровье. Надо начать бегать по утрам и больше отдыхать."
        )
        result = analyze_entry(db, payload)
        print("\n--- Result ---")
        print(f"Summary: {result.summary}")
        print(f"Tags:    {result.tags}")
        print(f"Emotion: {result.emotion}")
        print(f"Intent:  {result.intent}")
        print(f"Insight: {result.insight}")
        print("--------------")
    finally:
        db.close()

if __name__ == "__main__":
    test()
