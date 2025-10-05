# TICKET 002: Core FastAPI Backend with /v1/simplify Endpoint

## Overview
Implement the core FastAPI backend service with the primary `/v1/simplify` endpoint, database models, and basic authentication system.

## Priority: HIGH
## Estimated Time: 5-7 days
## Dependencies: TICKET_001 (Infrastructure Foundation)

---

## Acceptance Criteria

### 1. FastAPI Application Structure
- [ ] Create FastAPI application with proper project structure
- [ ] Implement database models using SQLAlchemy
- [ ] Set up database migrations with Alembic
- [ ] Create API route structure with proper organization
- [ ] Implement request/response models with Pydantic

### 2. Core /v1/simplify Endpoint
- [ ] Implement POST /v1/simplify endpoint
- [ ] Add input validation and error handling
- [ ] Integrate with Hugging Face model inference
- [ ] Implement response formatting
- [ ] Add request logging and monitoring

### 3. Database Integration
- [ ] Set up PostgreSQL connection
- [ ] Create database models for translations, jobs, users
- [ ] Implement database session management
- [ ] Add database health checks
- [ ] Set up connection pooling

### 4. Authentication & Authorization
- [ ] Implement JWT-based authentication
- [ ] Create API key management system
- [ ] Add rate limiting per API key
- [ ] Implement organization-based access control
- [ ] Add request validation middleware

---

## Technical Requirements

### API Endpoint Specification

#### POST /v1/simplify
```json
{
  "input": "Der komplizierte deutsche Text...",
  "format": "text|html",
  "mode": "easy|light",
  "glossary_id": "uuid|null",
  "preserve_html_tags": true,
  "max_output_chars": 2000
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "done",
  "model_version": "mt5-v1.0",
  "output": "Der vereinfachte Text...",
  "processing_time_ms": 1500,
  "cache_hit": false
}
```

### Database Models
```python
# Core models to implement
class Organization(Base):
    id: UUID
    name: str
    plan: str
    dpa_signed: bool
    created_at: datetime

class User(Base):
    id: UUID
    org_id: UUID
    email: str
    roles: List[str]
    created_at: datetime

class APIKey(Base):
    id: UUID
    org_id: UUID
    key_hash: str
    scopes: List[str]
    rate_limit: int
    created_at: datetime

class Translation(Base):
    id: UUID
    org_id: UUID
    user_id: UUID
    job_id: UUID
    input_hash: str
    input_snippet: str
    output_snippet: str
    model_version: str
    status: str
    created_at: datetime
```

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── translation.py
│   │   └── api_key.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── translation.py
│   │   └── auth.py
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── simplify.py
│   │   │   └── auth.py
│   │   └── dependencies.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── translation.py
│   │   ├── model_inference.py
│   │   └── auth.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── logging.py
│       └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   ├── test_models/
│   └── test_services/
├── alembic/                   # Database migrations
├── requirements.txt
└── Dockerfile
```

---

## Implementation Steps

### Step 1: FastAPI Application Setup (Day 1)
1. Create FastAPI application with proper structure
2. Set up configuration management with environment variables
3. Implement database connection and session management
4. Create basic middleware for logging and error handling
5. Set up CORS and security headers

### Step 2: Database Models (Day 1-2)
1. Create SQLAlchemy models for all entities
2. Set up Alembic for database migrations
3. Implement database session management
4. Add database health check endpoint
5. Create initial migration scripts

### Step 3: Authentication System (Day 2-3)
1. Implement JWT token generation and validation
2. Create API key management system
3. Add rate limiting middleware
4. Implement organization-based access control
5. Add request validation and authentication

### Step 4: Core Translation Service (Day 3-4)
1. Create translation service with Hugging Face integration
2. Implement input validation and preprocessing
3. Add model inference with error handling
4. Implement response formatting and logging
5. Add basic caching mechanism

### Step 5: API Endpoints (Day 4-5)
1. Implement POST /v1/simplify endpoint
2. Add comprehensive error handling
3. Implement request/response validation
4. Add API documentation with OpenAPI
5. Create health check endpoints

### Step 6: Testing and Documentation (Day 5-7)
1. Write comprehensive unit tests
2. Create integration tests for API endpoints
3. Add API documentation and examples
4. Implement logging and monitoring
5. Create deployment scripts

---

## Code Examples

### FastAPI Application Setup
```python
# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import get_db
from app.api.v1 import simplify, auth

app = FastAPI(
    title="German Simplification API",
    description="API for simplifying German text",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1", tags=["auth"])
app.include_router(simplify.router, prefix="/v1", tags=["simplify"])
```

### Translation Service
```python
# app/services/translation.py
from typing import Dict, Any
import requests
from app.config import settings
from app.models.translation import Translation
from app.schemas.translation import SimplifyRequest, SimplifyResponse

class TranslationService:
    def __init__(self):
        self.hf_api_url = f"https://api-inference.huggingface.co/models/{settings.MODEL_NAME}"
        self.hf_token = settings.HF_API_TOKEN
    
    async def simplify_text(self, request: SimplifyRequest) -> SimplifyResponse:
        # Prepare input for model
        prompt = self._prepare_prompt(request.input, request.mode)
        
        # Call Hugging Face API
        response = requests.post(
            self.hf_api_url,
            headers={"Authorization": f"Bearer {self.hf_token}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": request.max_output_chars,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Model inference failed")
        
        result = response.json()
        output = result[0].get("generated_text") if isinstance(result, list) else result.get("generated_text", "")
        
        return SimplifyResponse(
            job_id=str(uuid.uuid4()),
            status="done",
            model_version=settings.MODEL_VERSION,
            output=output,
            processing_time_ms=0,  # Calculate actual time
            cache_hit=False
        )
    
    def _prepare_prompt(self, text: str, mode: str) -> str:
        mode_text = "Leichte Sprache" if mode == "light" else "Einfache Sprache"
        return f"Vereinfache den folgenden Text in {mode_text}:\n\n{text}"
```

### API Endpoint Implementation
```python
# app/api/v1/simplify.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.translation import SimplifyRequest, SimplifyResponse
from app.services.translation import TranslationService
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/simplify", response_model=SimplifyResponse)
async def simplify_text(
    request: SimplifyRequest,
    current_user = Depends(get_current_user),
    translation_service: TranslationService = Depends()
):
    try:
        result = await translation_service.simplify_text(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Testing Requirements

### Unit Tests
- [ ] Test database models and relationships
- [ ] Test authentication and authorization
- [ ] Test translation service logic
- [ ] Test API endpoint validation
- [ ] Test error handling scenarios

### Integration Tests
- [ ] Test database operations
- [ ] Test Hugging Face API integration
- [ ] Test authentication flow
- [ ] Test rate limiting
- [ ] Test error responses

### API Tests
- [ ] Test /v1/simplify endpoint with valid requests
- [ ] Test error handling for invalid requests
- [ ] Test authentication requirements
- [ ] Test rate limiting behavior
- [ ] Test response formatting

---

## Performance Requirements

### Response Time
- [ ] API response time < 2 seconds for typical requests
- [ ] Database query time < 100ms
- [ ] Model inference time < 3 seconds
- [ ] Total request processing < 5 seconds

### Throughput
- [ ] Support 100+ concurrent requests
- [ ] Handle 1000+ requests per minute
- [ ] Maintain performance under load
- [ ] Implement proper connection pooling

---

## Security Requirements

### Authentication
- [ ] JWT tokens with proper expiration
- [ ] API key validation and rate limiting
- [ ] Request signing for sensitive operations
- [ ] Secure token storage and transmission

### Data Protection
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] Secure error messages

---

## Monitoring and Logging

### Logging
- [ ] Request/response logging
- [ ] Error logging with stack traces
- [ ] Performance metrics logging
- [ ] Security event logging

### Metrics
- [ ] Request count and response times
- [ ] Error rates by endpoint
- [ ] Database connection metrics
- [ ] Model inference metrics

---

## Success Criteria

### Functional Success
- [ ] API endpoint responds correctly to valid requests
- [ ] Authentication and authorization work properly
- [ ] Database operations are reliable
- [ ] Model inference produces quality results
- [ ] Error handling is comprehensive

### Performance Success
- [ ] Response times meet requirements
- [ ] System handles expected load
- [ ] Database performance is optimal
- [ ] Memory usage is reasonable

### Quality Success
- [ ] Code follows best practices
- [ ] Tests provide good coverage
- [ ] Documentation is complete
- [ ] Security requirements are met

---

## Dependencies

### External Services
- **Hugging Face API:** For model inference
- **PostgreSQL:** For data storage
- **Redis:** For caching (future ticket)

### Internal Dependencies
- **TICKET_001:** Infrastructure foundation
- **Database setup:** From infrastructure ticket
- **Model access:** Hugging Face account and API key

---

## Next Steps After Completion

1. **TICKET_003:** Add Redis caching and chunking logic
2. **TICKET_004:** Create browser extension
3. **TICKET_005:** Build React dashboard
4. **TICKET_006:** Implement glossary management

---

## Notes

- Ensure proper error handling for all external API calls
- Implement comprehensive logging for debugging
- Set up proper database indexing for performance
- Consider implementing request queuing for high load
- Plan for model versioning and updates

