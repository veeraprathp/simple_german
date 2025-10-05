from pydantic import BaseModel, Field
from typing import Optional, Literal
import uuid


class SimplifyRequest(BaseModel):
    input: str = Field(..., description="German text to simplify", min_length=1, max_length=10000)
    format: Literal["text", "html"] = Field(default="text", description="Input format")
    mode: Literal["easy", "light"] = Field(default="easy", description="Simplification mode")
    glossary_id: Optional[str] = Field(default=None, description="Custom glossary ID")
    preserve_html_tags: bool = Field(default=True, description="Preserve HTML tags in output")
    max_output_chars: int = Field(default=2000, description="Maximum output characters", ge=100, le=10000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "input": "Der komplizierte deutsche Text, der vereinfacht werden soll.",
                "format": "text",
                "mode": "easy",
                "glossary_id": None,
                "preserve_html_tags": True,
                "max_output_chars": 2000
            }
        }


class SimplifyResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: Literal["done", "processing", "failed"] = Field(..., description="Job status")
    model_version: str = Field(..., description="Model version used")
    output: Optional[str] = Field(None, description="Simplified text output")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    cache_hit: bool = Field(..., description="Whether result was served from cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "done",
                "model_version": "mt5-v1.0",
                "output": "Der einfache deutsche Text.",
                "processing_time_ms": 1500,
                "cache_hit": False
            }
        }
