import redis
import json
import hashlib
import logging
from typing import Optional, Any, Dict, Union
from app.config import settings

logger = logging.getLogger(__name__)


class RedisCacheManager:
    """Redis cache manager with connection pooling and error handling"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            socket_connect_timeout=settings.REDIS_CONNECTION_TIMEOUT,
            socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
            retry_on_timeout=True,
            health_check_interval=30
        )
        self.default_ttl = 3600 * 24  # 24 hours
        self._connection_pool = None
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from Redis cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except redis.RedisError as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for key {key}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set value in Redis cache with TTL"""
        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value, ensure_ascii=False)
            result = self.redis_client.setex(key, ttl, serialized)
            return bool(result)
        except redis.RedisError as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False
        except json.JSONEncodeError as e:
            logger.error(f"JSON encode error for key {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis cache"""
        try:
            result = self.redis_client.delete(key)
            return bool(result)
        except redis.RedisError as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache"""
        try:
            return bool(self.redis_client.exists(key))
        except redis.RedisError as e:
            logger.error(f"Redis exists error for key {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error checking key {key}: {e}")
            return False
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for existing key"""
        try:
            return bool(self.redis_client.expire(key, ttl))
        except redis.RedisError as e:
            logger.error(f"Redis expire error for key {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting TTL for key {key}: {e}")
            return False
    
    def generate_key(self, model_version: str, glossary_version: str, 
                    mode: str, input_text: str) -> str:
        """Generate cache key for translation request"""
        input_hash = hashlib.sha256(input_text.encode('utf-8')).hexdigest()[:16]
        return f"cache:{model_version}:{glossary_version}:{mode}:{input_hash}"
    
    def generate_input_hash(self, text: str) -> str:
        """Generate hash for input text"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Redis connection health"""
        try:
            info = self.redis_client.info()
            return {
                "status": "healthy",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "keyspace": info.get("db0", {}).get("keys", 0),
                "uptime": info.get("uptime_in_seconds", 0)
            }
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Redis statistics"""
        try:
            info = self.redis_client.info()
            return {
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "used_memory": info.get("used_memory", 0),
                "connected_clients": info.get("connected_clients", 0),
                "uptime": info.get("uptime_in_seconds", 0)
            }
        except Exception as e:
            logger.error(f"Failed to get Redis stats: {e}")
            return {}
    
    async def flush_cache(self) -> bool:
        """Flush all cache data (use with caution)"""
        try:
            self.redis_client.flushdb()
            logger.warning("Redis cache flushed")
            return True
        except Exception as e:
            logger.error(f"Failed to flush cache: {e}")
            return False
