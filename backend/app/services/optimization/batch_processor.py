import asyncio
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BatchRequest:
    """Represents a request in a batch"""
    request_id: str
    input_text: str
    mode: str
    format: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class BatchResult:
    """Represents a result from batch processing"""
    request_id: str
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    cache_hit: bool = False


class BatchProcessor:
    """Batch processing service for efficient translation requests"""
    
    def __init__(self, translation_service, cache_manager, max_batch_size: int = 10, batch_timeout: float = 5.0):
        self.translation_service = translation_service
        self.cache_manager = cache_manager
        self.max_batch_size = max_batch_size
        self.batch_timeout = batch_timeout
        self.pending_requests = []
        self.processing = False
    
    async def add_request(self, request: BatchRequest) -> BatchResult:
        """Add a request to the batch queue"""
        self.pending_requests.append(request)
        
        # If batch is full or timeout reached, process immediately
        if len(self.pending_requests) >= self.max_batch_size:
            return await self.process_batch()
        
        # Otherwise, wait for batch to fill or timeout
        return await self._wait_for_batch_completion(request.request_id)
    
    async def process_batch(self) -> List[BatchResult]:
        """Process all pending requests in batch"""
        if not self.pending_requests:
            return []
        
        start_time = time.time()
        self.processing = True
        
        try:
            # Group requests by model version and mode for efficiency
            grouped_requests = self._group_requests(self.pending_requests)
            results = []
            
            # Process each group in parallel
            tasks = []
            for group_key, group_requests in grouped_requests.items():
                task = self._process_group(group_requests)
                tasks.append(task)
            
            group_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Flatten results
            for group_result in group_results:
                if isinstance(group_result, Exception):
                    logger.error(f"Batch processing error: {group_result}")
                    continue
                results.extend(group_result)
            
            processing_time = time.time() - start_time
            logger.info(f"Batch processed {len(results)} requests in {processing_time:.2f}s")
            
            return results
            
        finally:
            self.pending_requests.clear()
            self.processing = False
    
    async def _process_group(self, requests: List[BatchRequest]) -> List[BatchResult]:
        """Process a group of similar requests"""
        results = []
        
        for request in requests:
            try:
                result = await self._process_single_request(request)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing request {request.request_id}: {e}")
                results.append(BatchResult(
                    request_id=request.request_id,
                    success=False,
                    error=str(e)
                ))
        
        return results
    
    async def _process_single_request(self, request: BatchRequest) -> BatchResult:
        """Process a single request with caching"""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self.cache_manager.generate_key(
                "mt5-v1.0",  # model_version
                "default",   # glossary_version
                request.mode,
                request.input_text
            )
            
            cached_result = await self.cache_manager.get(cache_key)
            if cached_result:
                processing_time = time.time() - start_time
                return BatchResult(
                    request_id=request.request_id,
                    success=True,
                    result=cached_result.get('output', ''),
                    processing_time=processing_time,
                    cache_hit=True
                )
            
            # Process with translation service
            from app.schemas.translation import SimplifyRequest
            simplify_request = SimplifyRequest(
                input=request.input_text,
                format=request.format,
                mode=request.mode
            )
            
            translation_result = await self.translation_service.simplify_text(simplify_request)
            
            # Cache the result
            cache_data = {
                'output': translation_result.output,
                'model_version': translation_result.model_version,
                'processing_time_ms': translation_result.processing_time_ms
            }
            await self.cache_manager.set(cache_key, cache_data, ttl=3600*24)
            
            processing_time = time.time() - start_time
            return BatchResult(
                request_id=request.request_id,
                success=translation_result.status == "done",
                result=translation_result.output,
                processing_time=processing_time,
                cache_hit=False
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return BatchResult(
                request_id=request.request_id,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    def _group_requests(self, requests: List[BatchRequest]) -> Dict[str, List[BatchRequest]]:
        """Group requests by model version and mode for efficiency"""
        groups = {}
        
        for request in requests:
            # Group by mode and format for now
            group_key = f"{request.mode}:{request.format}"
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(request)
        
        return groups
    
    async def _wait_for_batch_completion(self, request_id: str) -> BatchResult:
        """Wait for batch to complete and return result for specific request"""
        # This is a simplified implementation
        # In production, you'd use a more sophisticated queuing system
        
        start_time = time.time()
        
        while time.time() - start_time < self.batch_timeout:
            if not self.processing and len(self.pending_requests) >= self.max_batch_size:
                break
            await asyncio.sleep(0.1)
        
        # Process the batch
        results = await self.process_batch()
        
        # Find the result for this request
        for result in results:
            if result.request_id == request_id:
                return result
        
        # If not found, return error
        return BatchResult(
            request_id=request_id,
            success=False,
            error="Request not found in batch results"
        )
    
    def get_batch_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics"""
        return {
            'pending_requests': len(self.pending_requests),
            'max_batch_size': self.max_batch_size,
            'batch_timeout': self.batch_timeout,
            'processing': self.processing
        }
    
    async def flush_pending_requests(self) -> List[BatchResult]:
        """Force process all pending requests"""
        if not self.pending_requests:
            return []
        
        return await self.process_batch()
