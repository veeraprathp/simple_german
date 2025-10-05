# TICKET 003: Redis Caching Layer and Chunking Logic

## Overview
Implement Redis caching layer for performance optimization and intelligent text chunking logic for handling large documents and web pages.

## Priority: HIGH
## Estimated Time: 4-6 days
## Dependencies: TICKET_002 (Core FastAPI Backend)

---

## Acceptance Criteria

### 1. Redis Caching Implementation
- [ ] Set up Redis connection and configuration
- [ ] Implement multi-layer caching strategy
- [ ] Add cache key generation and management
- [ ] Implement cache invalidation policies
- [ ] Add cache performance monitoring

### 2. Text Chunking System
- [ ] Implement intelligent text chunking algorithm
- [ ] Add HTML parsing and text extraction
- [ ] Create chunk size optimization logic
- [ ] Implement chunk reassembly system
- [ ] Add chunk caching and deduplication

### 3. Performance Optimization
- [ ] Implement request batching for efficiency
- [ ] Add cache hit/miss ratio monitoring
- [ ] Optimize memory usage and garbage collection
- [ ] Implement connection pooling for Redis
- [ ] Add performance metrics and alerting

### 4. Cache Management
- [ ] Implement cache warming strategies
- [ ] Add cache eviction policies
- [ ] Create cache health monitoring
- [ ] Implement cache backup and recovery
- [ ] Add cache analytics and reporting

---

## Technical Requirements

### Caching Strategy

#### Multi-Layer Caching
```python
# Cache layers to implement
class CacheManager:
    def __init__(self):
        self.l1_cache = {}  # In-process LRU cache
        self.l2_cache = redis.Redis()  # Redis cache
        self.l3_cache = S3Storage()  # Long-term storage
    
    async def get(self, key: str) -> Optional[str]:
        # L1: Check in-process cache
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # L2: Check Redis cache
        value = await self.l2_cache.get(key)
        if value:
            self.l1_cache[key] = value
            return value
        
        # L3: Check S3 storage
        value = await self.l3_cache.get(key)
        if value:
            await self.l2_cache.set(key, value, ex=3600*24)
            self.l1_cache[key] = value
            return value
        
        return None
```

#### Cache Key Strategy
```python
# Cache key generation
def generate_cache_key(
    model_version: str,
    glossary_version: str,
    mode: str,
    input_hash: str
) -> str:
    return f"cache:{model_version}:{glossary_version}:{mode}:{input_hash}"

def generate_input_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]
```

### Chunking System

#### Text Chunking Algorithm
```python
class TextChunker:
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.sentence_tokenizer = self._load_sentence_tokenizer()
    
    def chunk_text(self, text: str) -> List[Chunk]:
        # Split into sentences
        sentences = self.sentence_tokenizer.tokenize(text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.max_chunk_size:
                if current_chunk:
                    chunks.append(Chunk(
                        text=" ".join(current_chunk),
                        start_pos=0,  # Calculate actual position
                        end_pos=0,    # Calculate actual position
                        chunk_id=str(uuid.uuid4())
                    ))
                    current_chunk = []
                    current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add remaining sentences
        if current_chunk:
            chunks.append(Chunk(
                text=" ".join(current_chunk),
                start_pos=0,
                end_pos=0,
                chunk_id=str(uuid.uuid4())
            ))
        
        return chunks
```

#### HTML Parsing and Extraction
```python
class HTMLProcessor:
    def __init__(self):
        self.parser = BeautifulSoup
    
    def extract_text_nodes(self, html: str) -> List[TextNode]:
        soup = self.parser(html, 'html.parser')
        nodes = []
        
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']):
            if element.get_text(strip=True):
                nodes.append(TextNode(
                    element=element,
                    text=element.get_text(strip=True),
                    xpath=self._get_xpath(element),
                    css_selector=self._get_css_selector(element),
                    node_id=str(uuid.uuid4())
                ))
        
        return nodes
    
    def reconstruct_html(self, original_html: str, translations: Dict[str, str]) -> str:
        soup = self.parser(original_html, 'html.parser')
        
        for element in soup.find_all():
            xpath = self._get_xpath(element)
            if xpath in translations:
                element.string = translations[xpath]
        
        return str(soup)
```

### Project Structure Updates
```
backend/
├── app/
│   ├── services/
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── redis_manager.py
│   │   │   ├── cache_strategies.py
│   │   │   └── cache_monitoring.py
│   │   ├── chunking/
│   │   │   ├── __init__.py
│   │   │   ├── text_chunker.py
│   │   │   ├── html_processor.py
│   │   │   └── chunk_assembler.py
│   │   └── optimization/
│   │       ├── __init__.py
│   │       ├── batch_processor.py
│   │       └── performance_monitor.py
│   ├── models/
│   │   ├── chunk.py
│   │   └── cache_entry.py
│   └── utils/
│       ├── text_utils.py
│       └── performance_utils.py
```

---

## Implementation Steps

### Step 1: Redis Integration (Day 1-2)
1. Set up Redis connection and configuration
2. Implement basic cache operations (get, set, delete)
3. Add connection pooling and error handling
4. Implement cache key generation and management
5. Add Redis health monitoring

### Step 2: Multi-Layer Caching (Day 2-3)
1. Implement in-process LRU cache
2. Add Redis cache layer with TTL
3. Implement S3 long-term storage
4. Create cache fallback mechanisms
5. Add cache performance monitoring

### Step 3: Text Chunking System (Day 3-4)
1. Implement sentence-based chunking algorithm
2. Add HTML parsing and text extraction
3. Create chunk size optimization logic
4. Implement chunk reassembly system
5. Add chunk caching and deduplication

### Step 4: Performance Optimization (Day 4-5)
1. Implement request batching for efficiency
2. Add cache hit/miss ratio monitoring
3. Optimize memory usage and garbage collection
4. Implement connection pooling for Redis
5. Add performance metrics and alerting

### Step 5: Cache Management (Day 5-6)
1. Implement cache warming strategies
2. Add cache eviction policies
3. Create cache health monitoring
4. Implement cache backup and recovery
5. Add cache analytics and reporting

---

## Code Examples

### Redis Cache Manager
```python
# app/services/cache/redis_manager.py
import redis
import json
import hashlib
from typing import Optional, Any, Dict
from app.config import settings

class RedisCacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            max_connections=20
        )
        self.default_ttl = 3600 * 24  # 24 hours
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            # Log error but don't fail the request
            print(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value)
            return self.redis_client.setex(key, ttl, serialized)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def generate_key(self, model_version: str, glossary_version: str, 
                    mode: str, input_text: str) -> str:
        input_hash = hashlib.sha256(input_text.encode()).hexdigest()[:16]
        return f"cache:{model_version}:{glossary_version}:{mode}:{input_hash}"
```

### Text Chunking Service
```python
# app/services/chunking/text_chunker.py
import re
import uuid
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    start_pos: int
    end_pos: int
    chunk_id: str
    metadata: Dict[str, Any] = None

class TextChunker:
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.sentence_pattern = re.compile(r'[.!?]+\s+')
    
    def chunk_text(self, text: str) -> List[Chunk]:
        # Split into sentences
        sentences = self.sentence_pattern.split(text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_size = 0
        start_pos = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.max_chunk_size and current_chunk:
                # Create chunk
                chunk_text = " ".join(current_chunk)
                chunks.append(Chunk(
                    text=chunk_text,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    chunk_id=str(uuid.uuid4()),
                    metadata={
                        'sentence_count': len(current_chunk),
                        'char_count': len(chunk_text)
                    }
                ))
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = overlap_sentences + [sentence]
                current_size = sum(len(s) for s in current_chunk)
                start_pos += len(chunk_text) - len(" ".join(overlap_sentences))
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        # Add remaining sentences
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(Chunk(
                text=chunk_text,
                start_pos=start_pos,
                end_pos=start_pos + len(chunk_text),
                chunk_id=str(uuid.uuid4()),
                metadata={
                    'sentence_count': len(current_chunk),
                    'char_count': len(chunk_text)
                }
            ))
        
        return chunks
```

### Batch Processing Service
```python
# app/services/optimization/batch_processor.py
import asyncio
from typing import List, Dict, Any
from app.services.translation import TranslationService
from app.services.cache.redis_manager import RedisCacheManager

class BatchProcessor:
    def __init__(self, translation_service: TranslationService, cache_manager: RedisCacheManager):
        self.translation_service = translation_service
        self.cache_manager = cache_manager
        self.batch_size = 10
        self.batch_timeout = 5.0  # seconds
    
    async def process_batch(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Group requests by model version and mode for efficiency
        grouped_requests = self._group_requests(requests)
        results = []
        
        for group_key, group_requests in grouped_requests.items():
            # Process group in parallel
            tasks = [
                self._process_single_request(req) 
                for req in group_requests
            ]
            group_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(group_results)
        
        return results
    
    def _group_requests(self, requests: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        groups = {}
        for req in requests:
            key = f"{req.get('model_version', 'default')}:{req.get('mode', 'easy')}"
            if key not in groups:
                groups[key] = []
            groups[key].append(req)
        return groups
    
    async def _process_single_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Check cache first
        cache_key = self.cache_manager.generate_key(
            request.get('model_version', 'default'),
            request.get('glossary_version', 'default'),
            request.get('mode', 'easy'),
            request['input']
        )
        
        cached_result = await self.cache_manager.get(cache_key)
        if cached_result:
            return {**cached_result, 'cache_hit': True}
        
        # Process with translation service
        result = await self.translation_service.simplify_text(request)
        
        # Cache the result
        await self.cache_manager.set(cache_key, result, ttl=3600*24)
        
        return {**result, 'cache_hit': False}
```

---

## Testing Requirements

### Unit Tests
- [ ] Test Redis cache operations
- [ ] Test text chunking algorithm
- [ ] Test HTML parsing and extraction
- [ ] Test cache key generation
- [ ] Test batch processing logic

### Integration Tests
- [ ] Test cache hit/miss scenarios
- [ ] Test chunking with various text sizes
- [ ] Test HTML processing with complex documents
- [ ] Test batch processing with multiple requests
- [ ] Test cache invalidation policies

### Performance Tests
- [ ] Test cache performance under load
- [ ] Test chunking performance with large documents
- [ ] Test batch processing efficiency
- [ ] Test memory usage optimization
- [ ] Test Redis connection pooling

---

## Performance Requirements

### Cache Performance
- [ ] Cache hit ratio > 70% for repeated requests
- [ ] Cache response time < 10ms
- [ ] Redis connection pool utilization < 80%
- [ ] Memory usage < 1GB for cache operations

### Chunking Performance
- [ ] Chunking time < 100ms for 10KB documents
- [ ] Chunking time < 1s for 100KB documents
- [ ] Memory usage < 500MB for large documents
- [ ] Chunk size optimization within 10% of target

### Batch Processing Performance
- [ ] Batch processing time < 2s for 10 requests
- [ ] Parallel processing efficiency > 80%
- [ ] Error rate < 1% for batch operations
- [ ] Memory usage < 1GB for batch operations

---

## Monitoring and Metrics

### Cache Metrics
- [ ] Cache hit/miss ratios
- [ ] Cache response times
- [ ] Redis memory usage
- [ ] Cache eviction rates
- [ ] Cache key distribution

### Chunking Metrics
- [ ] Chunking processing times
- [ ] Chunk size distributions
- [ ] HTML parsing success rates
- [ ] Text extraction accuracy
- [ ] Chunk reassembly success rates

### Performance Metrics
- [ ] Batch processing times
- [ ] Parallel processing efficiency
- [ ] Memory usage patterns
- [ ] Error rates by operation type
- [ ] System resource utilization

---

## Success Criteria

### Functional Success
- [ ] Caching system works reliably
- [ ] Chunking produces accurate results
- [ ] HTML processing preserves structure
- [ ] Batch processing is efficient
- [ ] Cache invalidation works properly

### Performance Success
- [ ] Cache hit ratios meet targets
- [ ] Processing times are acceptable
- [ ] Memory usage is optimized
- [ ] System handles expected load
- [ ] Error rates are minimal

### Quality Success
- [ ] Code follows best practices
- [ ] Tests provide good coverage
- [ ] Documentation is complete
- [ ] Monitoring is comprehensive
- [ ] Error handling is robust

---

## Dependencies

### External Services
- **Redis:** For caching layer
- **S3:** For long-term storage
- **PostgreSQL:** For metadata storage

### Internal Dependencies
- **TICKET_002:** Core FastAPI backend
- **Translation Service:** From previous ticket
- **Database Models:** From previous ticket

---

## Next Steps After Completion

1. **TICKET_004:** Create browser extension
2. **TICKET_005:** Build React dashboard
3. **TICKET_006:** Implement glossary management
4. **TICKET_007:** Add monitoring and production deployment

---

## Notes

- Ensure proper error handling for all cache operations
- Implement comprehensive monitoring for cache performance
- Consider implementing cache warming strategies
- Plan for cache scaling and sharding
- Document cache invalidation policies clearly

