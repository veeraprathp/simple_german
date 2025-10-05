from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base


class Translation(Base):
    __tablename__ = "translations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    job_id = Column(UUID(as_uuid=True), nullable=True)
    input_hash = Column(String(64), nullable=False)
    input_snippet = Column(Text, nullable=False)
    output_snippet = Column(Text, nullable=True)
    model_version = Column(String(50), default="mt5-v1.0")
    status = Column(String(20), default="pending")  # pending, processing, done, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="translations")
    user = relationship("User", back_populates="translations")
    
    def __repr__(self):
        return f"<Translation(id={self.id}, status={self.status}, model_version={self.model_version})>"
