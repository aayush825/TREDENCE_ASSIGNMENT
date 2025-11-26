from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.autocomplete_service import AutocompleteService
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/autocomplete", tags=["autocomplete"])

class AutocompleteRequest(BaseModel):
    language: str
    prefix: str
    room_id: str = None

class AutocompleteSuggestion(BaseModel):
    label: str
    kind: str
    detail: str
    insertText: str = None

@router.post("/suggestions", response_model=List[AutocompleteSuggestion])
def get_suggestions(request: AutocompleteRequest, db: Session = Depends(get_db)):
    """Get autocomplete suggestions."""
    try:
        suggestions = AutocompleteService.get_suggestions(request.language, request.prefix, db)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{room_id}/{line_number}")
def get_code_context(room_id: str, line_number: int, db: Session = Depends(get_db)):
    """Get code context at a specific line for autocomplete."""
    try:
        context = AutocompleteService.get_code_context(db, room_id, line_number)
        return {"context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
