# Extension Icons

## Required Icons

The extension requires icons in three sizes:
- `icon16.png` - 16x16 pixels (browser toolbar)
- `icon48.png` - 48x48 pixels (extension management page)
- `icon128.png` - 128x128 pixels (Chrome Web Store)

## Creating Icons

### Design Guidelines
- **Style**: Modern, minimal, flat design
- **Colors**: Use brand colors (#667eea, #764ba2)
- **Symbol**: Use "🇩🇪" flag or "Aa" text symbol
- **Background**: Transparent or solid color
- **Format**: PNG with transparency

### Tools
- Figma: https://figma.com
- Canva: https://canva.com
- GIMP: https://gimp.org
- Photoshop: https://adobe.com/photoshop

### Quick Creation with ImageMagick

```bash
# Install ImageMagick
sudo apt install imagemagick

# Create simple colored icons
convert -size 128x128 xc:'#667eea' -pointsize 80 -fill white \
  -gravity center -annotate +0+0 'DE' icon128.png

convert icon128.png -resize 48x48 icon48.png
convert icon128.png -resize 16x16 icon16.png
```

## Placeholder Icons

For development, you can use placeholder icons:
- Just create simple colored squares with text
- Use online tools like favicon.io
- Or use the ImageMagick commands above

## Production Icons

For production release:
1. Hire a designer or use design tools
2. Create professional-looking icons
3. Test on different backgrounds
4. Ensure clarity at all sizes
5. Follow platform guidelines
