# German Simplification SaaS Platform

A production-ready SaaS platform for simplifying German text using AI, with browser extension, dashboard, and API capabilities.

## Project Overview

This platform provides real-time German text simplification for accessibility compliance, targeting government agencies, healthcare organizations, legal firms, and educational institutions.

### Key Features

- **Real-time Translation**: AI-powered German text simplification
- **Browser Extension**: Chrome/Firefox extension for on-page translation
- **Web Dashboard**: React-based management interface
- **REST API**: Enterprise-grade translation API
- **Custom Glossaries**: Organization-specific terminology management

### Technology Stack

- **Backend**: Python 3.11, FastAPI, PostgreSQL, Redis
- **Frontend**: React, TypeScript, Tailwind CSS
- **ML Model**: DEplain/mt5-simple-german-corpus (mT5-base)
- **Infrastructure**: AWS/GCP, Docker, Kubernetes, Terraform
- **CI/CD**: GitHub Actions, ArgoCD

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+
- Terraform
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:veeraprathp/simple_german.git
   cd simple_german
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development environment**
   ```bash
   docker-compose up -d
   ```

4. **Install dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd ../dashboard
   npm install
   ```

5. **Run the application**
   ```bash
   # Backend API
   cd backend
   uvicorn app.main:app --reload

   # Frontend Dashboard
   cd dashboard
   npm run dev

   # Browser Extension
   cd extension
   npm run build
   # Load unpacked extension in Chrome
   ```

## Project Structure

```
simple_german/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── tests/               # Backend tests
│   ├── requirements.txt
│   └── Dockerfile
├── model-serving/           # Model inference service
│   ├── app/
│   ├── models/
│   └── Dockerfile
├── extension/               # Browser extension
│   ├── manifest.json
│   ├── content/             # Content scripts
│   ├── popup/               # Extension popup
│   └── background/          # Background scripts
├── dashboard/               # React dashboard
│   ├── src/
│   ├── public/
│   └── package.json
├── infrastructure/          # Terraform configs
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── docs/                   # Documentation
├── scripts/                 # Utility scripts
├── docker-compose.yml       # Local development
└── .github/                 # GitHub Actions
    └── workflows/
```

## Development Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature development
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes

### Commit Convention

```
type(scope): description

feat(api): add translation endpoint
fix(extension): resolve content script injection
docs(readme): update setup instructions
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd dashboard
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Infrastructure

### Local Development

- **Database**: PostgreSQL 14+ (Docker)
- **Cache**: Redis 7+ (Docker)
- **Storage**: Local S3-compatible (MinIO)
- **Monitoring**: Prometheus + Grafana (Docker)

### Production

- **Cloud**: AWS/GCP
- **Compute**: GPU instances (T4/A10)
- **Database**: RDS PostgreSQL Multi-AZ
- **Cache**: ElastiCache Redis
- **Storage**: S3/Cloud Storage
- **CDN**: CloudFront/CloudFlare

## API Documentation

### Core Endpoints

- `POST /v1/simplify` - Synchronous text simplification
- `POST /v1/simplify/page` - Asynchronous page translation
- `GET /v1/jobs/{job_id}` - Job status and results
- `POST /v1/glossaries` - Glossary management

### Authentication

- JWT-based authentication
- API key management
- Organization-based access control
- Rate limiting per key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/veeraprathp/simple_german/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veeraprathp/simple_german/discussions)

## Roadmap

- [ ] Phase A: MVP Foundation (Weeks 1-4)
- [ ] Phase B: Browser Extension (Weeks 5-8)
- [ ] Phase C: Dashboard & Management (Weeks 9-12)
- [ ] Phase D: Production Hardening (Weeks 13-16)

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap.

