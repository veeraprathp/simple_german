import time
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class CacheStrategy(ABC):
    """Abstract base class for cache strategies"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass


class LRUCacheStrategy(CacheStrategy):
    """In-process LRU cache strategy"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.access_times = {}
        self.ttl_map = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from LRU cache"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if key in self.ttl_map:
            if time.time() > self.ttl_map[key]:
                await self.delete(key)
                return None
        
        # Move to end (most recently used)
        value = self.cache.pop(key)
        self.cache[key] = value
        self.access_times[key] = time.time()
        
        return value
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in LRU cache"""
        try:
            # Remove if exists
            if key in self.cache:
                del self.cache[key]
            
            # Add to cache
            self.cache[key] = value
            self.access_times[key] = time.time()
            
            # Set TTL
            if ttl:
                self.ttl_map[key] = time.time() + ttl
            
            # Evict if over capacity
            while len(self.cache) > self.max_size:
                oldest_key = next(iter(self.cache))
                await self.delete(oldest_key)
            
            return True
        except Exception as e:
            logger.error(f"LRU cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from LRU cache"""
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
            if key in self.ttl_map:
                del self.ttl_map[key]
            return True
        except Exception as e:
            logger.error(f"LRU cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in LRU cache"""
        return key in self.cache
    
    def get_stats(self) -> Dict[str, Any]:
        """Get LRU cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_ratio": getattr(self, 'hits', 0) / max(getattr(self, 'requests', 1), 1),
            "oldest_access": min(self.access_times.values()) if self.access_times else None,
            "newest_access": max(self.access_times.values()) if self.access_times else None
        }


class MultiLayerCacheStrategy(CacheStrategy):
    """Multi-layer cache strategy combining LRU and Redis"""
    
    def __init__(self, l1_cache: LRUCacheStrategy, l2_cache: Any):
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
        self.hits = 0
        self.misses = 0
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from multi-layer cache"""
        # L1: Check in-process cache
        value = await self.l1_cache.get(key)
        if value is not None:
            self.hits += 1
            return value
        
        # L2: Check Redis cache
        value = await self.l2_cache.get(key)
        if value is not None:
            # Promote to L1 cache
            await self.l1_cache.set(key, value)
            self.hits += 1
            return value
        
        self.misses += 1
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in multi-layer cache"""
        # Set in both layers
        l1_success = await self.l1_cache.set(key, value, ttl)
        l2_success = await self.l2_cache.set(key, value, ttl)
        return l1_success and l2_success
    
    async def delete(self, key: str) -> bool:
        """Delete key from multi-layer cache"""
        l1_success = await self.l1_cache.delete(key)
        l2_success = await self.l2_cache.delete(key)
        return l1_success and l2_success
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in multi-layer cache"""
        return await self.l1_cache.exists(key) or await self.l2_cache.exists(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get multi-layer cache statistics"""
        total_requests = self.hits + self.misses
        return {
            "l1_stats": self.l1_cache.get_stats(),
            "l2_stats": getattr(self.l2_cache, 'get_stats', lambda: {})(),
            "total_hits": self.hits,
            "total_misses": self.misses,
            "hit_ratio": self.hits / max(total_requests, 1),
            "total_requests": total_requests
        }
