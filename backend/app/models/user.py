from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    roles = Column(JSONB, default=list)  # List of roles like ["admin", "editor", "viewer"]
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    translations = relationship("Translation", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, org_id={self.org_id})>"
