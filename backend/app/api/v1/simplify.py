from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.translation import SimplifyRequest, SimplifyResponse
from app.services.translation import TranslationService
from app.services.cache import RedisCacheManager
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
    Simplify German text using AI model with caching.
    
    This endpoint takes German text and returns a simplified version using
    the DEplain/mt5-simple-german-corpus model with Redis caching for performance.
    """
    try:
        logger.info(f"Translation request received for user {current_user.get('user_id')}")
        
        # Create cache manager and translation service
        cache_manager = RedisCacheManager()
        translation_service = TranslationService(cache_manager=cache_manager)
        
        # Process the translation
        result = await translation_service.simplify_text(request)
        
        # Log the result
        cache_status = "cache hit" if result.cache_hit else "cache miss"
        logger.info(f"Translation completed: {result.status}, time: {result.processing_time_ms}ms, {cache_status}")
        
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


@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache performance statistics"""
    try:
        cache_manager = RedisCacheManager()
        stats = await cache_manager.get_stats()
        health = await cache_manager.health_check()
        
        return {
            "cache_stats": stats,
            "cache_health": health,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.post("/cache/flush")
async def flush_cache():
    """Flush all cache data (use with caution)"""
    try:
        cache_manager = RedisCacheManager()
        success = await cache_manager.flush_cache()
        
        if success:
            return {"message": "Cache flushed successfully", "status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to flush cache"
            )
    except Exception as e:
        logger.error(f"Failed to flush cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to flush cache: {str(e)}"
        )
