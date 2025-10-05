import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read: int
    disk_io_write: int
    network_sent: int
    network_recv: int
    active_connections: int
    request_count: int
    avg_response_time: float


class PerformanceMonitor:
    """System performance monitoring and alerting"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.start_time = time.time()
        self.request_count = 0
        self.response_times = []
        self.alert_thresholds = {
            "cpu_percent_max": 80.0,
            "memory_percent_max": 85.0,
            "response_time_max": 5.0,
            "disk_io_max": 1000,  # MB/s
            "network_io_max": 1000  # MB/s
        }
    
    async def record_request(self, response_time: float):
        """Record a request for performance tracking"""
        self.request_count += 1
        self.response_times.append(response_time)
        
        # Keep only last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
    
    async def get_current_metrics(self) -> PerformanceMetrics:
        """Get current system performance metrics"""
        current_time = datetime.now()
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        network_io = psutil.net_io_counters()
        
        # Calculate average response time
        avg_response_time = sum(self.response_times) / max(len(self.response_times), 1)
        
        metrics = PerformanceMetrics(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            disk_io_read=disk_io.read_bytes if disk_io else 0,
            disk_io_write=disk_io.write_bytes if disk_io else 0,
            network_sent=network_io.bytes_sent if network_io else 0,
            network_recv=network_io.bytes_recv if network_io else 0,
            active_connections=len(psutil.net_connections()),
            request_count=self.request_count,
            avg_response_time=avg_response_time
        )
        
        # Store in history
        self.metrics_history.append(metrics)
        
        # Keep only last 100 metrics
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return metrics
    
    async def check_performance_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        alerts = []
        metrics = await self.get_current_metrics()
        
        # Check CPU usage
        if metrics.cpu_percent > self.alert_thresholds["cpu_percent_max"]:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"CPU usage is {metrics.cpu_percent:.1f}%, above threshold of {self.alert_thresholds['cpu_percent_max']:.1f}%",
                "value": metrics.cpu_percent,
                "threshold": self.alert_thresholds["cpu_percent_max"]
            })
        
        # Check memory usage
        if metrics.memory_percent > self.alert_thresholds["memory_percent_max"]:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "critical",
                "message": f"Memory usage is {metrics.memory_percent:.1f}%, above threshold of {self.alert_thresholds['memory_percent_max']:.1f}%",
                "value": metrics.memory_percent,
                "threshold": self.alert_thresholds["memory_percent_max"]
            })
        
        # Check response time
        if metrics.avg_response_time > self.alert_thresholds["response_time_max"]:
            alerts.append({
                "type": "high_response_time",
                "severity": "warning",
                "message": f"Average response time is {metrics.avg_response_time:.2f}s, above threshold of {self.alert_thresholds['response_time_max']:.2f}s",
                "value": metrics.avg_response_time,
                "threshold": self.alert_thresholds["response_time_max"]
            })
        
        return alerts
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        metrics = await self.get_current_metrics()
        alerts = await self.check_performance_alerts()
        
        # Calculate uptime
        uptime = time.time() - self.start_time
        
        # Get historical trends
        if len(self.metrics_history) > 1:
            recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
            cpu_trend = self._calculate_trend([m.cpu_percent for m in recent_metrics])
            memory_trend = self._calculate_trend([m.memory_percent for m in recent_metrics])
            response_time_trend = self._calculate_trend([m.avg_response_time for m in recent_metrics])
        else:
            cpu_trend = memory_trend = response_time_trend = 0
        
        return {
            "timestamp": metrics.timestamp.isoformat(),
            "uptime_seconds": uptime,
            "current_metrics": {
                "cpu_percent": metrics.cpu_percent,
                "memory_percent": metrics.memory_percent,
                "memory_used_mb": metrics.memory_used_mb,
                "avg_response_time": metrics.avg_response_time,
                "request_count": metrics.request_count,
                "active_connections": metrics.active_connections
            },
            "trends": {
                "cpu_trend": cpu_trend,
                "memory_trend": memory_trend,
                "response_time_trend": response_time_trend
            },
            "alerts": alerts,
            "alert_count": len(alerts),
            "history_size": len(self.metrics_history)
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend for a series of values"""
        if len(values) < 2:
            return 0
        
        # Simple linear trend calculation
        n = len(values)
        x = list(range(n))
        y = values
        
        # Calculate slope
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def get_metrics_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get performance metrics history"""
        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "cpu_percent": m.cpu_percent,
                "memory_percent": m.memory_percent,
                "memory_used_mb": m.memory_used_mb,
                "avg_response_time": m.avg_response_time,
                "request_count": m.request_count,
                "active_connections": m.active_connections
            }
            for m in self.metrics_history[-limit:]
        ]
    
    async def reset_metrics(self):
        """Reset all performance metrics"""
        self.start_time = time.time()
        self.request_count = 0
        self.response_times = []
        self.metrics_history = []
        logger.info("Performance metrics reset")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "memory_total_gb": psutil.virtual_memory().total / (1024 ** 3),
            "disk_usage": psutil.disk_usage('/')._asdict(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "platform": psutil.platform.platform(),
            "python_version": psutil.platform.python_version()
        }
