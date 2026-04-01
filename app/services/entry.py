from fastapi import HTTPException
from sqlalchemy.orm import Session
from google import genai
import json

from app.schemas.entry import EntryCreate, EntryResponse, EntryAnalysisResponse
from app.models.entry import Entry
from app.core.config import settings

# Инициализация клиента Gemini
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """Ты — Thought Agent, умный ИИ-аналитик. 
Твоя цель — проанализировать текст пользователя и вернуть структурированный JSON с результатами. 
Обязательно извлеки:
1. summary: краткое изложение мысли (1-2 предложения).
2. tags: список из 2-5 ключевых тегов (например, "work", "stress", "idea").
3. emotion: преобладающая эмоция (одно слово).
4. intent: скрытое намерение или потребность (например, "venting", "planning", "seeking clarity").
5. insight: глубокий аналитический инсайт по поводу этой мысли.
Формат ответа должен строго соответствовать заданной схеме.
"""

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
    
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=stripped_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=EntryAnalysisResponse,
                temperature=0.7,
            ),
        )
        data = json.loads(response.text)
        analysis = EntryAnalysisResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate or parse LLM response: {str(e)}")
    
    db_entry = Entry(
        original_text=stripped_text,
        summary=analysis.summary,
        tags=analysis.tags,
        emotion=analysis.emotion,
        intent=analysis.intent,
        insight=analysis.insight
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return analysis
