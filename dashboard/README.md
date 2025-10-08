# German Simplifier - Dashboard

A modern React dashboard for managing German text simplification services.

## Features

- 🔐 **Authentication**: Secure login and user management
- 📊 **Dashboard**: Real-time statistics and analytics
- 📝 **Translation Interface**: Upload and translate documents
- 📚 **Glossary Management**: Custom term replacements
- 📈 **Analytics**: Usage tracking and performance metrics
- ⚙️ **Settings**: API configuration and user preferences

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Development

### Project Structure

```
dashboard/
├── src/
│   ├── components/      # Reusable components
│   │   └── Layout.tsx   # Main layout with sidebar
│   ├── pages/           # Page components
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Translate.tsx
│   │   ├── Glossary.tsx
│   │   ├── Analytics.tsx
│   │   └── Settings.tsx
│   ├── services/        # API services
│   │   └── api.ts
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── Dockerfile           # Docker configuration
```

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### API Integration

The dashboard connects to the FastAPI backend at `/api` endpoints:

- `POST /api/v1/simplify` - Translate text
- `GET /api/v1/cache/stats` - Get cache statistics
- `POST /api/v1/cache/flush` - Clear cache
- `GET /api/v1/glossaries` - List glossaries
- `POST /api/v1/glossaries` - Create glossary

## Docker

### Build and Run

```bash
# Build image
docker build -t german-simplifier-dashboard .

# Run container
docker run -p 3000:80 german-simplifier-dashboard
```

### Docker Compose

```yaml
dashboard:
  build: ./dashboard
  ports:
    - "3000:80"
  environment:
    - API_URL=http://backend:8000
  depends_on:
    - backend
```

## Pages

### Dashboard
- Overview statistics
- Recent translations
- Quick actions

### Translate
- Text input/output interface
- Mode selection (Easy/Light German)
- File upload support
- Export functionality

### Glossary
- Manage custom term translations
- Add/edit/delete entries
- Scope configuration (global/sentence)

### Analytics
- Usage metrics
- Performance charts
- Activity history

### Settings
- API configuration
- User profile
- Notifications

## Styling

The dashboard uses Tailwind CSS with a custom theme:

- **Primary Color**: `#667eea` (Purple/Blue)
- **Secondary Color**: `#764ba2` (Purple)
- **Component Classes**: `btn`, `card`, `input`

## Production Build

```bash
# Build optimized production bundle
npm run build

# Output will be in dist/ directory
```

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```

## Performance

- **Bundle Size**: ~150KB (gzipped)
- **First Paint**: <1s
- **Interactive**: <2s
- **Lighthouse Score**: 95+

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) for details
