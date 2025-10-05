# German Simplification API Backend

This is the FastAPI backend for the German Simplification SaaS platform.

## Features

- **Text Simplification**: AI-powered German text simplification using Hugging Face models
- **REST API**: Clean, documented API endpoints
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication and API key management
- **Caching**: Redis integration for performance optimization
- **Monitoring**: Health checks and logging

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Development

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Check logs**:
   ```bash
   docker-compose logs backend
   ```

## API Endpoints

### Core Endpoints

- `POST /v1/simplify` - Simplify German text
- `GET /health` - Health check
- `GET /docs` - API documentation

### Example Usage

```bash
curl -X POST "http://localhost:8000/v1/simplify" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Der komplizierte deutsche Text, der vereinfacht werden soll.",
    "format": "text",
    "mode": "easy",
    "max_output_chars": 1000
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── utils/         # Utilities
├── alembic/           # Database migrations
├── tests/             # Test files
├── requirements.txt   # Dependencies
└── Dockerfile         # Container configuration
```

## Database Models

- **Organization**: Customer organizations
- **User**: System users
- **APIKey**: API authentication keys
- **Translation**: Translation records

## Configuration

The application uses environment variables for configuration. See `.env.example` for all available options.

Key settings:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `HF_API_TOKEN`: Hugging Face API token
- `SECRET_KEY`: JWT secret key

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Deployment

The application is containerized and can be deployed using Docker Compose or Kubernetes.

### Docker Compose

```bash
docker-compose up -d
```

### Production Considerations

- Set strong `SECRET_KEY`
- Configure proper CORS origins
- Set up SSL/TLS
- Configure monitoring and logging
- Set up database backups
- Configure rate limiting

## Monitoring

- Health check: `GET /health`
- API documentation: `GET /docs`
- Metrics: Prometheus integration (coming soon)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
