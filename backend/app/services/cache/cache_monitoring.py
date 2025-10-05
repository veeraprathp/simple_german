import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class CacheMetrics:
    """Cache performance metrics"""
    timestamp: datetime
    hit_count: int
    miss_count: int
    total_requests: int
    hit_ratio: float
    avg_response_time: float
    memory_usage: int
    key_count: int


class CacheMonitor:
    """Cache performance monitoring and alerting"""
    
    def __init__(self, cache_manager: Any):
        self.cache_manager = cache_manager
        self.metrics_history: List[CacheMetrics] = []
        self.alert_thresholds = {
            "hit_ratio_min": 0.7,  # Minimum hit ratio
            "response_time_max": 0.01,  # Maximum response time in seconds
            "memory_usage_max": 1024 * 1024 * 1024,  # 1GB max memory
            "error_rate_max": 0.05  # 5% max error rate
        }
        self.start_time = time.time()
        self.request_count = 0
        self.hit_count = 0
        self.miss_count = 0
        self.error_count = 0
        self.response_times = []
    
    async def record_hit(self, response_time: float):
        """Record a cache hit"""
        self.hit_count += 1
        self.request_count += 1
        self.response_times.append(response_time)
    
    async def record_miss(self, response_time: float):
        """Record a cache miss"""
        self.miss_count += 1
        self.request_count += 1
        self.response_times.append(response_time)
    
    async def record_error(self):
        """Record a cache error"""
        self.error_count += 1
    
    async def get_current_metrics(self) -> CacheMetrics:
        """Get current cache metrics"""
        current_time = datetime.now()
        
        # Calculate hit ratio
        hit_ratio = self.hit_count / max(self.request_count, 1)
        
        # Calculate average response time
        avg_response_time = sum(self.response_times) / max(len(self.response_times), 1)
        
        # Get cache stats
        cache_stats = await self.cache_manager.get_stats()
        memory_usage = cache_stats.get("used_memory", 0)
        key_count = cache_stats.get("keyspace_hits", 0) + cache_stats.get("keyspace_misses", 0)
        
        metrics = CacheMetrics(
            timestamp=current_time,
            hit_count=self.hit_count,
            miss_count=self.miss_count,
            total_requests=self.request_count,
            hit_ratio=hit_ratio,
            avg_response_time=avg_response_time,
            memory_usage=memory_usage,
            key_count=key_count
        )
        
        # Store in history
        self.metrics_history.append(metrics)
        
        # Keep only last 100 metrics
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return metrics
    
    async def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        alerts = []
        metrics = await self.get_current_metrics()
        
        # Check hit ratio
        if metrics.hit_ratio < self.alert_thresholds["hit_ratio_min"]:
            alerts.append({
                "type": "low_hit_ratio",
                "severity": "warning",
                "message": f"Cache hit ratio is {metrics.hit_ratio:.2%}, below threshold of {self.alert_thresholds['hit_ratio_min']:.2%}",
                "value": metrics.hit_ratio,
                "threshold": self.alert_thresholds["hit_ratio_min"]
            })
        
        # Check response time
        if metrics.avg_response_time > self.alert_thresholds["response_time_max"]:
            alerts.append({
                "type": "high_response_time",
                "severity": "warning",
                "message": f"Average response time is {metrics.avg_response_time:.4f}s, above threshold of {self.alert_thresholds['response_time_max']:.4f}s",
                "value": metrics.avg_response_time,
                "threshold": self.alert_thresholds["response_time_max"]
            })
        
        # Check memory usage
        if metrics.memory_usage > self.alert_thresholds["memory_usage_max"]:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "critical",
                "message": f"Memory usage is {metrics.memory_usage / (1024**3):.2f}GB, above threshold of {self.alert_thresholds['memory_usage_max'] / (1024**3):.2f}GB",
                "value": metrics.memory_usage,
                "threshold": self.alert_thresholds["memory_usage_max"]
            })
        
        # Check error rate
        error_rate = self.error_count / max(self.request_count, 1)
        if error_rate > self.alert_thresholds["error_rate_max"]:
            alerts.append({
                "type": "high_error_rate",
                "severity": "critical",
                "message": f"Error rate is {error_rate:.2%}, above threshold of {self.alert_thresholds['error_rate_max']:.2%}",
                "value": error_rate,
                "threshold": self.alert_thresholds["error_rate_max"]
            })
        
        return alerts
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        metrics = await self.get_current_metrics()
        alerts = await self.check_alerts()
        
        # Calculate uptime
        uptime = time.time() - self.start_time
        
        # Get cache health
        cache_health = await self.cache_manager.health_check()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime,
            "metrics": {
                "hit_count": metrics.hit_count,
                "miss_count": metrics.miss_count,
                "total_requests": metrics.total_requests,
                "hit_ratio": metrics.hit_ratio,
                "avg_response_time": metrics.avg_response_time,
                "memory_usage": metrics.memory_usage,
                "key_count": metrics.key_count,
                "error_count": self.error_count,
                "error_rate": self.error_count / max(self.request_count, 1)
            },
            "cache_health": cache_health,
            "alerts": alerts,
            "alert_count": len(alerts),
            "history_size": len(self.metrics_history)
        }
    
    async def reset_metrics(self):
        """Reset all metrics"""
        self.start_time = time.time()
        self.request_count = 0
        self.hit_count = 0
        self.miss_count = 0
        self.error_count = 0
        self.response_times = []
        self.metrics_history = []
        logger.info("Cache metrics reset")
    
    def get_metrics_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get metrics history"""
        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "hit_count": m.hit_count,
                "miss_count": m.miss_count,
                "total_requests": m.total_requests,
                "hit_ratio": m.hit_ratio,
                "avg_response_time": m.avg_response_time,
                "memory_usage": m.memory_usage,
                "key_count": m.key_count
            }
            for m in self.metrics_history[-limit:]
        ]
