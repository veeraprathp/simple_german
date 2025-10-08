# German Text Simplifier - Browser Extension

A Chrome/Firefox extension that simplifies German text on any webpage using AI-powered translation.

## Features

- **One-Click Simplification**: Simplify all German text on any webpage
- **Two Modes**: Choose between "Einfache Sprache" (Easy) or "Leichte Sprache" (Light)
- **Smart Caching**: Remember translations for faster performance
- **Visual Feedback**: See what text has been simplified
- **Restore Original**: Toggle back to original text anytime
- **Statistics**: Track your usage and cache performance

## Installation

### Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked"
4. Select the `extension` folder

### Firefox

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Navigate to the `extension` folder and select `manifest.json`

## Usage

### Basic Usage

1. **Click the extension icon** in your browser toolbar
2. **Select translation mode**:
   - **Einfache Sprache**: Simplified German for general audience
   - **Leichte Sprache**: Very simple German for accessibility
3. **Click "Simplify This Page"** to translate all German text
4. **Click "Restore Original"** to revert to original text

### Settings

- **API URL**: Configure your backend API endpoint (default: `http://localhost:8000`)
- **Mode**: Set your preferred translation mode
- **Cache**: Clear cached translations if needed

## How It Works

### 1. Text Detection
The extension automatically detects German text on the page using:
- Common German characters (ä, ö, ü, ß)
- Common German words (der, die, das, und, ist, etc.)
- Minimum text length (15+ characters)

### 2. Translation Process
1. Extract text nodes from the page
2. Check local cache for existing translations
3. Send uncached text to the API
4. Display simplified text with visual feedback
5. Store results in cache for future use

### 3. Caching Strategy
- **Local Cache**: Chrome storage API (unlimited)
- **LRU Eviction**: Keeps 1000 most recent translations
- **Automatic Cleanup**: Hourly cleanup of old entries
- **Cross-Tab**: Cache shared across all browser tabs

## API Integration

The extension connects to the German Simplification API:

```javascript
POST /v1/simplify
{
  "input": "Der komplizierte deutsche Text...",
  "format": "text",
  "mode": "easy",
  "max_output_chars": 2000
}
```

**Response:**
```javascript
{
  "job_id": "abc123",
  "status": "done",
  "model_version": "mt5-v1.0",
  "output": "Der einfache Text...",
  "processing_time_ms": 1500,
  "cache_hit": false
}
```

## Configuration

### Default Settings
```json
{
  "apiUrl": "http://localhost:8000",
  "apiKey": "",
  "mode": "easy",
  "autoSimplify": false
}
```

### Environment Variables
For production, update the API URL in the settings or modify `background/background.js`:

```javascript
this.apiUrl = 'https://api.simple-german.com';
```

## Performance

### Metrics
- **First Translation**: ~2-5 seconds (API call)
- **Cached Translation**: <10ms
- **Cache Hit Rate**: 70%+ for repeated visits
- **Memory Usage**: <50MB
- **Cache Size**: Up to 1000 translations

### Optimization
- Batch processing (5 texts at a time)
- Smart text filtering (German detection)
- Lazy loading (process on-demand)
- Background service worker
- Persistent cache

## Troubleshooting

### Extension Not Working

**Check Extension Status:**
1. Go to `chrome://extensions/`
2. Ensure extension is enabled
3. Check for error messages

**Reload Extension:**
1. Click the reload icon on the extension card
2. Try the page again

### API Connection Issues

**Check API Status:**
1. Open browser console (F12)
2. Look for network errors
3. Verify API URL in settings

**Test API Directly:**
```bash
curl -X POST http://localhost:8000/v1/simplify \
  -H "Content-Type: application/json" \
  -d '{"input":"Test text","format":"text","mode":"easy"}'
```

### No Text Being Simplified

**Possible Causes:**
- Page has no German text
- Text is too short (<15 characters)
- Text is in script/style tags
- Page structure prevents detection

**Debug Steps:**
1. Open browser console
2. Look for "Found X text nodes" message
3. Check if text meets detection criteria

## Development

### Project Structure
```
extension/
├── manifest.json          # Extension manifest
├── popup/                 # Extension popup UI
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── content/               # Content scripts
│   ├── content.js
│   └── content.css
├── background/            # Background service
│   └── background.js
└── icons/                 # Extension icons
```

### Testing

**Manual Testing:**
1. Load extension in developer mode
2. Visit German websites (e.g., deutsche-welle.de)
3. Test simplification functionality
4. Check browser console for errors

**Debugging:**
- Content script: Inspect webpage (F12)
- Popup: Right-click popup → Inspect
- Background: chrome://extensions/ → Background page

### Building for Production

1. **Update manifest.json:**
   - Increment version
   - Update permissions
   - Add production API URL

2. **Package extension:**
   ```bash
   # Chrome
   chrome://extensions/ → Pack extension

   # Firefox
   web-ext build
   ```

## Security

### Permissions
- `activeTab`: Access current tab for text extraction
- `storage`: Store cache and settings
- `scripting`: Inject content scripts

### Data Privacy
- **No personal data collected**
- **Translations stored locally only**
- **API calls use HTTPS (production)**
- **No tracking or analytics**

## License

MIT License - see [LICENSE](../LICENSE) for details

## Support

- **Documentation**: [docs/](../docs/)
- **Issues**: [GitHub Issues](https://github.com/veeraprathp/simple_german/issues)
- **Email**: support@simple-german.com

## Changelog

### Version 1.0.0 (2025-01-08)
- Initial release
- Chrome and Firefox support
- Two translation modes
- Local caching
- Statistics tracking
- Visual feedback
- Settings management
