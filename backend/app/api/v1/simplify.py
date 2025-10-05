from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.translation import SimplifyRequest, SimplifyResponse
from app.services.translation import TranslationService
from app.api.dependencies import get_api_key_user
from app.database import get_db
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/simplify", response_model=SimplifyResponse)
async def simplify_text(
    request: SimplifyRequest,
    current_user: dict = Depends(get_api_key_user),
    db: Session = Depends(get_db)
):
    """
    Simplify German text using AI model.
    
    This endpoint takes German text and returns a simplified version using
    the DEplain/mt5-simple-german-corpus model.
    """
    try:
        logger.info(f"Translation request received for user {current_user.get('user_id')}")
        
        # Create translation service
        translation_service = TranslationService()
        
        # Process the translation
        result = await translation_service.simplify_text(request)
        
        # Log the result
        logger.info(f"Translation completed: {result.status}, time: {result.processing_time_ms}ms")
        
        return result
        
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "translation-api"}
