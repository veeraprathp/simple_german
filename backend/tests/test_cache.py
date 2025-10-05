import pytest
import asyncio
from unittest.mock import Mock, patch
from app.services.cache import RedisCacheManager, LRUCacheStrategy, MultiLayerCacheStrategy
from app.services.cache.cache_monitoring import CacheMonitor


class TestRedisCacheManager:
    """Test Redis cache manager functionality"""
    
    @pytest.fixture
    def cache_manager(self):
        return RedisCacheManager()
    
    @pytest.mark.asyncio
    async def test_cache_operations(self, cache_manager):
        """Test basic cache operations"""
        key = "test_key"
        value = {"output": "test output", "model_version": "v1.0"}
        
        # Test set
        result = await cache_manager.set(key, value)
        assert result is True
        
        # Test get
        retrieved = await cache_manager.get(key)
        assert retrieved == value
        
        # Test exists
        exists = await cache_manager.exists(key)
        assert exists is True
        
        # Test delete
        deleted = await cache_manager.delete(key)
        assert deleted is True
        
        # Test get after delete
        retrieved_after_delete = await cache_manager.get(key)
        assert retrieved_after_delete is None
    
    def test_generate_key(self, cache_manager):
        """Test cache key generation"""
        key = cache_manager.generate_key("v1.0", "default", "easy", "test input")
        assert key.startswith("cache:v1.0:default:easy:")
        assert len(key) > 20  # Should include hash
    
    def test_generate_input_hash(self, cache_manager):
        """Test input hash generation"""
        text = "test input text"
        hash1 = cache_manager.generate_input_hash(text)
        hash2 = cache_manager.generate_input_hash(text)
        
        assert hash1 == hash2  # Same input should produce same hash
        assert len(hash1) == 16  # Should be 16 characters


class TestLRUCacheStrategy:
    """Test LRU cache strategy"""
    
    @pytest.fixture
    def lru_cache(self):
        return LRUCacheStrategy(max_size=3)
    
    @pytest.mark.asyncio
    async def test_lru_operations(self, lru_cache):
        """Test LRU cache operations"""
        # Test set and get
        await lru_cache.set("key1", "value1")
        result = await lru_cache.get("key1")
        assert result == "value1"
        
        # Test exists
        exists = await lru_cache.exists("key1")
        assert exists is True
        
        # Test delete
        deleted = await lru_cache.delete("key1")
        assert deleted is True
        
        # Test get after delete
        result_after_delete = await lru_cache.get("key1")
        assert result_after_delete is None
    
    @pytest.mark.asyncio
    async def test_lru_eviction(self, lru_cache):
        """Test LRU eviction when cache is full"""
        # Fill cache to capacity
        await lru_cache.set("key1", "value1")
        await lru_cache.set("key2", "value2")
        await lru_cache.set("key3", "value3")
        
        # Add one more item (should evict key1)
        await lru_cache.set("key4", "value4")
        
        # key1 should be evicted
        assert await lru_cache.get("key1") is None
        assert await lru_cache.get("key2") == "value2"
        assert await lru_cache.get("key3") == "value3"
        assert await lru_cache.get("key4") == "value4"
    
    @pytest.mark.asyncio
    async def test_lru_access_order(self, lru_cache):
        """Test LRU access order affects eviction"""
        # Fill cache
        await lru_cache.set("key1", "value1")
        await lru_cache.set("key2", "value2")
        await lru_cache.set("key3", "value3")
        
        # Access key1 to make it most recently used
        await lru_cache.get("key1")
        
        # Add new item (should evict key2, not key1)
        await lru_cache.set("key4", "value4")
        
        assert await lru_cache.get("key1") == "value1"  # Should still be there
        assert await lru_cache.get("key2") is None  # Should be evicted
        assert await lru_cache.get("key3") == "value3"
        assert await lru_cache.get("key4") == "value4"


class TestMultiLayerCacheStrategy:
    """Test multi-layer cache strategy"""
    
    @pytest.fixture
    def l1_cache(self):
        return LRUCacheStrategy(max_size=10)
    
    @pytest.fixture
    def l2_cache(self):
        # Mock Redis cache
        mock_cache = Mock()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = True
        mock_cache.delete.return_value = True
        mock_cache.exists.return_value = False
        return mock_cache
    
    @pytest.fixture
    def multi_layer_cache(self, l1_cache, l2_cache):
        return MultiLayerCacheStrategy(l1_cache, l2_cache)
    
    @pytest.mark.asyncio
    async def test_l1_cache_hit(self, multi_layer_cache):
        """Test L1 cache hit"""
        # Set value in L1 cache
        await multi_layer_cache.set("key1", "value1")
        
        # Get value (should hit L1)
        result = await multi_layer_cache.get("key1")
        assert result == "value1"
    
    @pytest.mark.asyncio
    async def test_l2_cache_hit(self, multi_layer_cache, l2_cache):
        """Test L2 cache hit"""
        # Mock L2 cache to return value
        l2_cache.get.return_value = "value2"
        
        # Get value (should hit L2 and promote to L1)
        result = await multi_layer_cache.get("key2")
        assert result == "value2"
        
        # Verify it was promoted to L1
        l1_result = await multi_layer_cache.l1_cache.get("key2")
        assert l1_result == "value2"
    
    @pytest.mark.asyncio
    async def test_cache_miss(self, multi_layer_cache, l2_cache):
        """Test cache miss"""
        # Mock L2 cache to return None
        l2_cache.get.return_value = None
        
        # Get value (should miss both layers)
        result = await multi_layer_cache.get("key3")
        assert result is None


class TestCacheMonitor:
    """Test cache monitoring functionality"""
    
    @pytest.fixture
    def cache_monitor(self):
        mock_cache_manager = Mock()
        return CacheMonitor(mock_cache_manager)
    
    @pytest.mark.asyncio
    async def test_record_hit(self, cache_monitor):
        """Test recording cache hit"""
        await cache_monitor.record_hit(0.001)
        assert cache_monitor.hit_count == 1
        assert cache_monitor.request_count == 1
        assert len(cache_monitor.response_times) == 1
    
    @pytest.mark.asyncio
    async def test_record_miss(self, cache_monitor):
        """Test recording cache miss"""
        await cache_monitor.record_miss(0.002)
        assert cache_monitor.miss_count == 1
        assert cache_monitor.request_count == 1
        assert len(cache_monitor.response_times) == 1
    
    @pytest.mark.asyncio
    async def test_record_error(self, cache_monitor):
        """Test recording cache error"""
        await cache_monitor.record_error()
        assert cache_monitor.error_count == 1
    
    @pytest.mark.asyncio
    async def test_get_current_metrics(self, cache_monitor):
        """Test getting current metrics"""
        # Record some activity
        await cache_monitor.record_hit(0.001)
        await cache_monitor.record_miss(0.002)
        await cache_monitor.record_error()
        
        metrics = await cache_monitor.get_current_metrics()
        
        assert metrics.hit_count == 1
        assert metrics.miss_count == 1
        assert metrics.total_requests == 2
        assert metrics.hit_ratio == 0.5
        assert metrics.avg_response_time == 0.0015  # (0.001 + 0.002) / 2
    
    @pytest.mark.asyncio
    async def test_check_alerts(self, cache_monitor):
        """Test performance alerts"""
        # Set up low hit ratio scenario
        cache_monitor.hit_count = 1
        cache_monitor.miss_count = 9  # 10% hit ratio
        
        alerts = await cache_monitor.check_alerts()
        
        # Should have low hit ratio alert
        assert len(alerts) > 0
        assert any(alert["type"] == "low_hit_ratio" for alert in alerts)
    
    @pytest.mark.asyncio
    async def test_reset_metrics(self, cache_monitor):
        """Test resetting metrics"""
        # Record some activity
        await cache_monitor.record_hit(0.001)
        await cache_monitor.record_miss(0.002)
        await cache_monitor.record_error()
        
        # Reset metrics
        await cache_monitor.reset_metrics()
        
        assert cache_monitor.hit_count == 0
        assert cache_monitor.miss_count == 0
        assert cache_monitor.error_count == 0
        assert cache_monitor.request_count == 0
        assert len(cache_monitor.response_times) == 0
        assert len(cache_monitor.metrics_history) == 0


class TestIntegration:
    """Integration tests for caching system"""
    
    @pytest.mark.asyncio
    async def test_translation_with_caching(self):
        """Test translation service with caching integration"""
        from app.services.translation import TranslationService
        from app.schemas.translation import SimplifyRequest
        
        # Mock cache manager
        mock_cache_manager = Mock()
        mock_cache_manager.generate_key.return_value = "test_key"
        mock_cache_manager.get.return_value = None
        mock_cache_manager.set.return_value = True
        
        # Create translation service with cache
        translation_service = TranslationService(cache_manager=mock_cache_manager)
        
        # Mock HTTP request
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{"generated_text": "Simplified text"}]
            mock_post.return_value = mock_response
            
            # Test translation request
            request = SimplifyRequest(
                input="Test German text",
                format="text",
                mode="easy"
            )
            
            result = await translation_service.simplify_text(request)
            
            # Verify result
            assert result.status == "done"
            assert result.output == "Simplified text"
            assert result.cache_hit is False
            
            # Verify cache was called
            mock_cache_manager.get.assert_called_once()
            mock_cache_manager.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_translation_with_cache_hit(self):
        """Test translation service with cache hit"""
        from app.services.translation import TranslationService
        from app.schemas.translation import SimplifyRequest
        
        # Mock cache manager with cached result
        mock_cache_manager = Mock()
        mock_cache_manager.generate_key.return_value = "test_key"
        mock_cache_manager.get.return_value = {
            "output": "Cached simplified text",
            "model_version": "mt5-v1.0",
            "processing_time_ms": 10
        }
        
        # Create translation service with cache
        translation_service = TranslationService(cache_manager=mock_cache_manager)
        
        # Test translation request
        request = SimplifyRequest(
            input="Test German text",
            format="text",
            mode="easy"
        )
        
        result = await translation_service.simplify_text(request)
        
        # Verify result
        assert result.status == "done"
        assert result.output == "Cached simplified text"
        assert result.cache_hit is True
        assert result.processing_time_ms < 50  # Should be very fast for cache hit
