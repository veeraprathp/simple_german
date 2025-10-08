// Background service worker for German Text Simplifier extension

class BackgroundService {
  constructor() {
    this.cache = new Map();
    this.stats = {
      totalRequests: 0,
      totalCacheHits: 0,
      totalErrors: 0,
      totalProcessingTime: 0
    };
    
    this.apiUrl = 'http://localhost:8000';
    this.init();
  }

  async init() {
    // Load cache and settings from storage
    await this.loadFromStorage();
    
    // Set up alarm for periodic cache cleanup
    chrome.alarms.create('cleanupCache', { periodInMinutes: 60 });
  }

  async loadFromStorage() {
    try {
      const result = await chrome.storage.local.get(['translationCache', 'settings', 'stats']);
      
      if (result.translationCache) {
        this.cache = new Map(Object.entries(result.translationCache));
      }
      
      if (result.settings) {
        this.apiUrl = result.settings.apiUrl || 'http://localhost:8000';
      }
      
      if (result.stats) {
        this.stats = result.stats;
      }
    } catch (error) {
      console.error('Load from storage error:', error);
    }
  }

  async saveToStorage() {
    try {
      const cacheObj = Object.fromEntries(this.cache);
      await chrome.storage.local.set({ 
        translationCache: cacheObj,
        stats: this.stats
      });
    } catch (error) {
      console.error('Save to storage error:', error);
    }
  }

  /**
   * Handle simplification request
   */
  async handleSimplifyRequest(text, mode) {
    const startTime = Date.now();
    this.stats.totalRequests++;
    
    try {
      // Generate cache key
      const cacheKey = `${mode}:${this.hashText(text)}`;
      
      // Check cache first
      if (this.cache.has(cacheKey)) {
        this.stats.totalCacheHits++;
        const processingTime = Date.now() - startTime;
        this.stats.totalProcessingTime += processingTime;
        await this.saveToStorage();
        
        return {
          success: true,
          output: this.cache.get(cacheKey),
          cacheHit: true,
          processingTime
        };
      }

      // Call API
      const result = await this.callAPI(text, mode);
      
      if (result.success) {
        // Cache the result
        this.cache.set(cacheKey, result.output);
        
        // Limit cache size
        if (this.cache.size > 1000) {
          const firstKey = this.cache.keys().next().value;
          this.cache.delete(firstKey);
        }
        
        await this.saveToStorage();
      }
      
      const processingTime = Date.now() - startTime;
      this.stats.totalProcessingTime += processingTime;
      
      return {
        ...result,
        cacheHit: false,
        processingTime
      };

    } catch (error) {
      this.stats.totalErrors++;
      await this.saveToStorage();
      
      return {
        success: false,
        error: error.message,
        cacheHit: false,
        processingTime: Date.now() - startTime
      };
    }
  }

  /**
   * Call simplification API
   */
  async callAPI(text, mode) {
    try {
      const response = await fetch(`${this.apiUrl}/v1/simplify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          input: text,
          format: 'text',
          mode: mode,
          max_output_chars: 2000
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      return {
        success: true,
        output: data.output || text,
        modelVersion: data.model_version,
        processingTimeMs: data.processing_time_ms
      };

    } catch (error) {
      console.error('API call error:', error);
      return {
        success: false,
        error: error.message,
        output: text
      };
    }
  }

  /**
   * Simple hash function
   */
  hashText(text) {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }

  /**
   * Clean up old cache entries
   */
  async cleanupCache() {
    const maxCacheSize = 500;
    
    if (this.cache.size > maxCacheSize) {
      const entriesToRemove = this.cache.size - maxCacheSize;
      const keys = Array.from(this.cache.keys());
      
      for (let i = 0; i < entriesToRemove; i++) {
        this.cache.delete(keys[i]);
      }
      
      await this.saveToStorage();
      console.log(`Cleaned up ${entriesToRemove} cache entries`);
    }
  }

  /**
   * Get statistics
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: this.cache.size,
      avgProcessingTime: this.stats.totalRequests > 0 
        ? Math.round(this.stats.totalProcessingTime / this.stats.totalRequests)
        : 0,
      cacheHitRate: this.stats.totalRequests > 0
        ? (this.stats.totalCacheHits / this.stats.totalRequests * 100).toFixed(1)
        : 0
    };
  }

  /**
   * Clear all cache
   */
  async clearCache() {
    this.cache.clear();
    await this.saveToStorage();
    return { success: true, message: 'Cache cleared' };
  }
}

// Initialize background service
const backgroundService = new BackgroundService();

// Listen for messages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'simplify') {
    backgroundService.handleSimplifyRequest(message.text, message.mode)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Will respond asynchronously
    
  } else if (message.type === 'getStats') {
    const stats = backgroundService.getStats();
    sendResponse({ success: true, stats });
    
  } else if (message.type === 'clearCache') {
    backgroundService.clearCache()
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  return true;
});

// Listen for alarms
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'cleanupCache') {
    backgroundService.cleanupCache();
  }
});

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('German Text Simplifier installed');
    // Set default settings
    chrome.storage.local.set({
      settings: {
        apiUrl: 'http://localhost:8000',
        apiKey: '',
        mode: 'easy',
        autoSimplify: false
      }
    });
  } else if (details.reason === 'update') {
    console.log('German Text Simplifier updated');
  }
});

console.log('German Text Simplifier background service worker loaded');
