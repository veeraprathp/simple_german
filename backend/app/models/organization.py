from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    plan = Column(String(50), default="starter")
    dpa_signed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="organization")
    api_keys = relationship("APIKey", back_populates="organization")
    translations = relationship("Translation", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name}, plan={self.plan})>"
