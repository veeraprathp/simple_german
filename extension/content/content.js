// Content script for German Text Simplifier extension

class GermanTextSimplifier {
  constructor() {
    this.originalTexts = new Map();
    this.isActive = false;
    this.apiUrl = 'http://localhost:8000';
    this.cache = new Map();
    this.stats = {
      textsSimplified: 0,
      cacheHits: 0,
      errors: 0
    };
    
    // Load settings and cache
    this.loadFromStorage();
  }

  async loadFromStorage() {
    try {
      const result = await chrome.storage.local.get(['settings', 'translationCache']);
      
      if (result.settings) {
        this.apiUrl = result.settings.apiUrl || 'http://localhost:8000';
      }
      
      if (result.translationCache) {
        this.cache = new Map(Object.entries(result.translationCache));
      }
    } catch (error) {
      console.error('Load from storage error:', error);
    }
  }

  async saveToStorage() {
    try {
      const cacheObj = Object.fromEntries(this.cache);
      await chrome.storage.local.set({ translationCache: cacheObj });
    } catch (error) {
      console.error('Save to storage error:', error);
    }
  }

  /**
   * Extract text nodes from the DOM
   */
  extractTextNodes() {
    const textNodes = [];
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          // Skip empty nodes
          if (!node.textContent.trim()) {
            return NodeFilter.FILTER_REJECT;
          }
          
          // Skip script, style, and other non-content elements
          const parentTag = node.parentElement?.tagName;
          if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'IFRAME', 'OBJECT', 'EMBED'].includes(parentTag)) {
            return NodeFilter.FILTER_REJECT;
          }
          
          // Skip very short text
          if (node.textContent.trim().length < 15) {
            return NodeFilter.FILTER_REJECT;
          }
          
          // Only German text (basic heuristic)
          if (!this.isLikelyGerman(node.textContent)) {
            return NodeFilter.FILTER_REJECT;
          }
          
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    let node;
    while (node = walker.nextNode()) {
      textNodes.push(node);
    }
    
    return textNodes;
  }

  /**
   * Simple heuristic to detect German text
   */
  isLikelyGerman(text) {
    // Look for common German characteristics
    const germanIndicators = /[äöüßÄÖÜ]|der|die|das|und|ist|nicht|werden|sein/i;
    return germanIndicators.test(text);
  }

  /**
   * Simplify all text on the page
   */
  async simplifyPage(mode = 'easy') {
    if (this.isActive) {
      console.log('Simplification already in progress');
      return { success: false, error: 'Already active' };
    }

    try {
      this.isActive = true;
      this.stats = { textsSimplified: 0, cacheHits: 0, errors: 0 };
      
      const textNodes = this.extractTextNodes();
      console.log(`Found ${textNodes.length} text nodes to simplify`);

      // Process nodes in batches
      const batchSize = 5;
      for (let i = 0; i < textNodes.length; i += batchSize) {
        const batch = textNodes.slice(i, i + batchSize);
        await this.processBatch(batch, mode);
      }

      // Save cache
      await this.saveToStorage();

      return { 
        success: true, 
        stats: this.stats 
      };

    } catch (error) {
      console.error('Simplify page error:', error);
      return { success: false, error: error.message };
    } finally {
      this.isActive = false;
    }
  }

  /**
   * Process a batch of text nodes
   */
  async processBatch(nodes, mode) {
    const promises = nodes.map(node => this.simplifyNode(node, mode));
    await Promise.all(promises);
  }

  /**
   * Simplify a single text node
   */
  async simplifyNode(node, mode) {
    const originalText = node.textContent.trim();
    
    try {
      // Store original text
      this.originalTexts.set(node, originalText);
      
      // Check cache first
      const cacheKey = `${mode}:${this.hashText(originalText)}`;
      if (this.cache.has(cacheKey)) {
        const cachedText = this.cache.get(cacheKey);
        node.textContent = cachedText;
        this.highlightNode(node, true);
        this.stats.cacheHits++;
        this.stats.textsSimplified++;
        return;
      }

      // Show loading indicator
      this.showLoadingIndicator(node);

      // Call API
      const simplifiedText = await this.callSimplifyAPI(originalText, mode);
      
      if (simplifiedText && simplifiedText !== originalText) {
        node.textContent = simplifiedText;
        this.highlightNode(node, false);
        
        // Cache the result
        this.cache.set(cacheKey, simplifiedText);
        this.stats.textsSimplified++;
      } else {
        // Restore original if simplification failed
        node.textContent = originalText;
      }

    } catch (error) {
      console.error('Simplify node error:', error);
      node.textContent = originalText; // Restore original on error
      this.stats.errors++;
    }
  }

  /**
   * Call the simplification API
   */
  async callSimplifyAPI(text, mode) {
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
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      return data.output || text;

    } catch (error) {
      console.error('API call error:', error);
      return text; // Return original text on error
    }
  }

  /**
   * Show loading indicator on node
   */
  showLoadingIndicator(node) {
    const parent = node.parentElement;
    if (parent) {
      parent.style.opacity = '0.6';
      parent.style.transition = 'opacity 0.3s';
    }
  }

  /**
   * Highlight simplified node
   */
  highlightNode(node, isCached) {
    const parent = node.parentElement;
    if (parent) {
      parent.style.opacity = '1';
      parent.style.backgroundColor = isCached ? '#f0fdf4' : '#fef3c7';
      parent.style.transition = 'all 0.3s';
      parent.setAttribute('data-simplified', 'true');
      
      // Remove highlight after a few seconds
      setTimeout(() => {
        if (parent.hasAttribute('data-simplified')) {
          parent.style.backgroundColor = '';
        }
      }, 3000);
    }
  }

  /**
   * Restore original text
   */
  restoreOriginal() {
    this.originalTexts.forEach((originalText, node) => {
      node.textContent = originalText;
      
      // Remove highlights
      const parent = node.parentElement;
      if (parent) {
        parent.style.backgroundColor = '';
        parent.style.opacity = '1';
        parent.removeAttribute('data-simplified');
      }
    });

    this.originalTexts.clear();
    this.isActive = false;

    return { success: true };
  }

  /**
   * Simple hash function for cache keys
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
}

// Initialize simplifier
const simplifier = new GermanTextSimplifier();

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'simplify') {
    simplifier.simplifyPage(message.mode || 'easy')
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Will respond asynchronously
    
  } else if (message.action === 'restore') {
    const result = simplifier.restoreOriginal();
    sendResponse(result);
    
  } else if (message.action === 'getStats') {
    sendResponse({ success: true, stats: simplifier.stats });
  }
  
  return true;
});

console.log('German Text Simplifier content script loaded');
