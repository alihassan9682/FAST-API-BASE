# ATB Backend - FastAPI Microservices Architecture

A scalable, production-ready FastAPI microservices backend with best practices, Docker support, and PostgreSQL database.

## 🏗️ Architecture

This project follows a microservices architecture with the following structure:

```
ATB-BE/
├── apps/                    # Microservices
│   ├── auth_service/        # Authentication & User Management
│   └── product_service/     # Product Management (Example)
├── core/                    # Shared core modules
├── shared/                  # Shared utilities and schemas
├── infrastructure/          # Docker, K8s, Terraform configs
├── tests/                   # Test suites
└── alembic/                 # Database migrations
```

## 🚀 Features

- **Microservices Architecture**: Independent, scalable services
- **FastAPI**: Modern, fast web framework
- **PostgreSQL**: Robust relational database
- **Docker & Docker Compose**: Containerized development and deployment
- **Alembic**: Database migrations
- **JWT Authentication**: Secure token-based auth
- **Environment Variables**: Configuration management
- **Health Checks**: Service monitoring endpoints
- **CORS Support**: Cross-origin resource sharing
- **Structured Logging**: Comprehensive logging system

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (if running locally without Docker)
- Git

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ATB-backend
```

### 2. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and update the following critical values:

```env
# Database
DATABASE_URL=postgresql://atb_user:atb_password@localhost:5432/atb_db
POSTGRES_USER=atb_user
POSTGRES_PASSWORD=atb_password
POSTGRES_DB=atb_db

# Security - IMPORTANT: Change in production!
SECRET_KEY=your-secret-key-here-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Install Dependencies

#### Option A: Using pip

```bash
pip install -r requirements.txt
```

#### Option B: Using Poetry (Recommended)

```bash
poetry install
```

### 4. Run with Docker Compose (Recommended)

This is the easiest way to get started:

```bash
# Start all services
make dev-up

# Or manually:
cd infrastructure/docker
docker-compose up -d
```

This will start:
- PostgreSQL database
- Auth Service (port 8000)
- Product Service (port 8001)
- Nginx reverse proxy (port 80)

### 5. Run Locally (Without Docker)

#### Start PostgreSQL

Make sure PostgreSQL is running locally or use Docker:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=atb_user \
  -e POSTGRES_PASSWORD=atb_password \
  -e POSTGRES_DB=atb_db \
  -p 5432:5432 \
  postgres:15-alpine
```

#### Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

#### Start Services

**Auth Service:**
```bash
make run-auth
# Or manually:
cd apps/auth_service
uvicorn main:app --reload --port 8000
```

**Product Service:**
```bash
make run-product
# Or manually:
cd apps/product_service
uvicorn main:app --reload --port 8001
```

## 📚 API Documentation

Once services are running, access the interactive API documentation:

- **Auth Service**: http://localhost:8000/docs
- **Product Service**: http://localhost:8001/docs
- **Nginx (All Services)**: http://localhost/docs

## 🔐 Authentication

### Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword123",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Use Access Token

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Testing

Run tests:

```bash
make test
# Or manually:
pytest tests/ -v
```

## 📦 Available Make Commands

```bash
make help              # Show all available commands
make install           # Install dependencies
make dev-up           # Start development environment
make dev-down         # Stop development environment
make build            # Build Docker images
make up               # Start all services
make down             # Stop all services
make logs             # View service logs
make clean            # Clean up Docker volumes
make test             # Run tests
make migrate          # Create new migration (use: make migrate msg="description")
make migrate-upgrade  # Apply migrations
make migrate-downgrade # Rollback last migration
make format           # Format code with black
make lint             # Lint code with flake8
make run-auth         # Run auth service locally
make run-product      # Run product service locally
```

## 🏗️ Project Structure

### Core Modules (`core/`)

- `config.py`: Shared configuration settings
- `database.py`: Database connection and session management
- `security.py`: Authentication and password hashing utilities
- `logger.py`: Logging configuration
- `exceptions.py`: Custom exception classes

### Microservices (`apps/`)

Each microservice follows this structure:

```
service_name/
├── api/
│   ├── v1/
│   │   ├── endpoints/    # API endpoints
│   │   └── api.py        # Router aggregation
│   └── dependencies.py   # API dependencies
├── core/                 # Service-specific config
├── db/
│   ├── models/          # SQLAlchemy models
│   ├── base.py          # Database base
│   └── session.py       # Session management
├── schemas/             # Pydantic schemas
├── services/            # Business logic
├── tasks/               # Background tasks (Celery)
└── main.py             # FastAPI application
```

### Adding a New Microservice

1. Create a new directory under `apps/`.
2. Use the existing `apps/product_service` folder as a **reference/example** for how to structure a service (API, db, schemas, services, tasks, etc.).
3. Copy that structure for your new service (e.g. `apps/order_service`) and rename modules/classes to fit your domain.
4. Update `apps/main.py` (or `docker-compose.yml` if you later split services again) to include your new service’s routes.
5. Update any related configuration (e.g. service URLs in `core/config.py`) if you introduce separate deployable services.

## 🔄 Database Migrations

### Create a Migration

```bash
make migrate msg="Add new table"
# Or manually:
alembic revision --autogenerate -m "Add new table"
```

### Apply Migrations

```bash
make migrate-upgrade
# Or manually:
alembic upgrade head
```

### Rollback Migration

```bash
make migrate-downgrade
# Or manually:
alembic downgrade -1
```

## 🐳 Docker

### Build Images

```bash
make build
```

### View Logs

```bash
make logs
# Or for specific service:
docker-compose -f infrastructure/docker/docker-compose.yml logs -f auth_service
```

### Clean Up

```bash
make clean
```

## 🔒 Security Best Practices

1. **Change SECRET_KEY**: Always use a strong, random secret key in production
2. **Use HTTPS**: Enable SSL/TLS in production
3. **Environment Variables**: Never commit `.env` files
4. **Database Credentials**: Use strong passwords
5. **CORS**: Configure allowed origins properly
6. **Token Expiration**: Adjust token expiration times as needed

## 📝 Environment Variables

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | 7 |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `LOG_LEVEL` | Logging level | `INFO` |

See `.env.example` for all available variables.

## 🚢 Deployment

### Production Considerations

1. Use environment-specific `.env` files
2. Set up proper database backups
3. Configure reverse proxy (Nginx/Traefik)
4. Enable HTTPS with SSL certificates
5. Set up monitoring and logging
6. Use container orchestration (Kubernetes) for production
7. Implement rate limiting
8. Set up CI/CD pipeline

### Docker Production Build

```bash
docker build -f infrastructure/docker/Dockerfile -t atb-backend:latest .
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Ensure code passes linting: `make lint`
5. Format code: `make format`
6. Submit a pull request

## 📄 License

[Your License Here]

## 🆘 Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database credentials are correct

### Port Already in Use

- Change port in `.env` or `docker-compose.yml`
- Stop conflicting services

### Import Errors

- Ensure you're in the project root
- Verify Python path includes project root
- Check that all dependencies are installed

### Migration Issues

- Ensure database is accessible
- Check Alembic configuration
- Verify models are imported in `alembic/env.py`

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Happy Coding! 🚀**
