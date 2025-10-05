from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    scopes = Column(JSONB, default=list)  # List of scopes like ["read", "write", "admin"]
    rate_limit = Column(Integer, default=60)  # Requests per minute
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, org_id={self.org_id}, rate_limit={self.rate_limit})>"
