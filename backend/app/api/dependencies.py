from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.auth import TokenData

# Security scheme
security = HTTPBearer()

# Auth service instance
auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> TokenData:
    """Get current user from JWT token"""
    token = credentials.credentials
    token_data = auth_service.verify_token(token)
    return token_data


def get_api_key_user(
    api_key: str,
    db: Session = Depends(get_db)
) -> dict:
    """Get user from API key"""
    # This is a simplified version - in production you'd validate the API key
    # against the database and check rate limits
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    # For now, return a mock user
    return {
        "org_id": "mock-org-id",
        "user_id": "mock-user-id",
        "scopes": ["read", "write"]
    }
