// Popup script for German Text Simplifier extension

class PopupController {
  constructor() {
    this.statusIndicator = document.getElementById('status-indicator');
    this.statusText = document.getElementById('status-text');
    this.simplifyBtn = document.getElementById('simplify-btn');
    this.restoreBtn = document.getElementById('restore-btn');
    this.settingsBtn = document.getElementById('settings-btn');
    this.clearCacheBtn = document.getElementById('clear-cache-btn');
    this.textsCount = document.getElementById('texts-count');
    this.cacheHits = document.getElementById('cache-hits');
    this.processingTime = document.getElementById('processing-time');
    
    this.init();
  }

  init() {
    // Set up event listeners
    this.simplifyBtn.addEventListener('click', () => this.handleSimplify());
    this.restoreBtn.addEventListener('click', () => this.handleRestore());
    this.settingsBtn.addEventListener('click', () => this.handleSettings());
    this.clearCacheBtn.addEventListener('click', () => this.handleClearCache());
    
    // Load saved settings
    this.loadSettings();
    
    // Update stats
    this.updateStats();
    
    // Set initial status
    this.setStatus('ready', 'Ready to simplify');
  }

  async handleSimplify() {
    try {
      this.setStatus('processing', 'Simplifying page...');
      this.simplifyBtn.disabled = true;
      
      // Get selected mode
      const mode = document.querySelector('input[name="mode"]:checked').value;
      
      // Get active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send message to content script
      const startTime = Date.now();
      chrome.tabs.sendMessage(tab.id, { 
        action: 'simplify',
        mode: mode
      }, (response) => {
        const processingTime = Date.now() - startTime;
        
        if (chrome.runtime.lastError) {
          this.setStatus('error', 'Failed to simplify page');
          console.error(chrome.runtime.lastError);
        } else if (response && response.success) {
          this.setStatus('active', 'Page simplified!');
          this.updateStats(response.stats);
          this.textsCount.textContent = response.stats.textsSimplified || 0;
          this.processingTime.textContent = `${processingTime}ms`;
        } else {
          this.setStatus('error', response?.error || 'Simplification failed');
        }
        
        this.simplifyBtn.disabled = false;
      });
      
    } catch (error) {
      console.error('Simplification error:', error);
      this.setStatus('error', 'An error occurred');
      this.simplifyBtn.disabled = false;
    }
  }

  async handleRestore() {
    try {
      this.setStatus('processing', 'Restoring original text...');
      this.restoreBtn.disabled = true;
      
      // Get active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send message to content script
      chrome.tabs.sendMessage(tab.id, { 
        action: 'restore' 
      }, (response) => {
        if (chrome.runtime.lastError) {
          this.setStatus('error', 'Failed to restore');
          console.error(chrome.runtime.lastError);
        } else {
          this.setStatus('ready', 'Original text restored');
          this.textsCount.textContent = '0';
        }
        
        this.restoreBtn.disabled = false;
      });
      
    } catch (error) {
      console.error('Restore error:', error);
      this.setStatus('error', 'An error occurred');
      this.restoreBtn.disabled = false;
    }
  }

  handleSettings() {
    // Open settings page (could be a new tab or modal)
    chrome.runtime.openOptionsPage();
  }

  async handleClearCache() {
    if (confirm('Are you sure you want to clear the cache?')) {
      try {
        await chrome.storage.local.remove('translationCache');
        this.cacheHits.textContent = '0';
        this.setStatus('ready', 'Cache cleared');
      } catch (error) {
        console.error('Clear cache error:', error);
        this.setStatus('error', 'Failed to clear cache');
      }
    }
  }

  setStatus(type, message) {
    this.statusIndicator.className = `status-indicator ${type}`;
    this.statusText.textContent = message;
  }

  async loadSettings() {
    try {
      const result = await chrome.storage.local.get('settings');
      const settings = result.settings || {
        mode: 'easy',
        apiUrl: 'http://localhost:8000',
        apiKey: ''
      };
      
      // Set selected mode
      const modeRadio = document.querySelector(`input[name="mode"][value="${settings.mode}"]`);
      if (modeRadio) {
        modeRadio.checked = true;
      }
      
      // Save mode changes
      document.querySelectorAll('input[name="mode"]').forEach(radio => {
        radio.addEventListener('change', async (e) => {
          settings.mode = e.target.value;
          await chrome.storage.local.set({ settings });
        });
      });
      
    } catch (error) {
      console.error('Load settings error:', error);
    }
  }

  async updateStats(newStats = null) {
    try {
      if (newStats) {
        // Update with new stats
        this.textsCount.textContent = newStats.textsSimplified || 0;
        this.cacheHits.textContent = newStats.cacheHits || 0;
      } else {
        // Load stats from storage
        const result = await chrome.storage.local.get('stats');
        const stats = result.stats || {
          totalTextsSimplified: 0,
          totalCacheHits: 0,
          totalProcessingTime: 0
        };
        
        this.cacheHits.textContent = stats.totalCacheHits || 0;
      }
    } catch (error) {
      console.error('Update stats error:', error);
    }
  }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PopupController();
});
