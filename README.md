# ATB Backend - FastAPI Django-like Architecture

A scalable, production-ready FastAPI backend with Django-like management commands, unified application structure, and PostgreSQL database.

## 🏗️ Architecture

This project follows a Django-like monolithic architecture with multiple apps, all running on a single port:

```
ATB-BE/
├── apps/                    # Application modules (like Django apps)
│   ├── auth_service/        # Authentication & User Management
│   ├── product_service/     # Product Management (Example)
│   └── main.py              # Unified FastAPI application
├── core/                    # Shared core modules
├── shared/                  # Shared utilities and schemas
├── infrastructure/          # Docker, K8s, Terraform configs
├── tests/                   # Test suites
├── alembic/                 # Database migrations
└── manage.py                # Django-like management script
```

## 🚀 Features

- **Django-like Management**: `manage.py` with `runserver`, `migrate`, `makemigrations` commands
- **Unified Application**: All apps run on a single port (like Django)
- **FastAPI**: Modern, fast web framework
- **PostgreSQL**: Robust relational database
- **Docker & Docker Compose**: Containerized development and deployment
- **Alembic Migrations**: Django-like migration system
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

# Security - REQUIRED: Must be set (project will not run without it)
SECRET_KEY=your-unique-secret-key-must-be-at-least-32-characters-long

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

### 4. Run Database Migrations (Django-like)

```bash
# Create initial migration (auto-detect model changes)
python manage.py makemigrations

# Or with a custom message
python manage.py makemigrations -m "Initial migration"

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### 5. Start Development Server (Django-like)

#### Option A: Using manage.py (Recommended)

```bash
# Start server on default port 8000
python manage.py runserver

# Or with custom port
python manage.py runserver --port 8080

# Or using Make
make runserver
```

#### Option B: Using Docker Compose

```bash
# Start all services (PostgreSQL + App)
make dev-up

# Or manually:
cd infrastructure/docker
docker-compose up -d
```

This will start:
- PostgreSQL database
- Unified FastAPI application (all apps on port 8000)

#### Option C: Run Locally (Without Docker)

Make sure PostgreSQL is running locally or use Docker:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=atb_user \
  -e POSTGRES_PASSWORD=atb_password \
  -e POSTGRES_DB=atb_db \
  -p 5432:5432 \
  postgres:15-alpine

# Then start the server
python manage.py runserver
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Auth Endpoints**: http://localhost:8000/api/v1/auth/
- **Product Endpoints**: http://localhost:8000/api/v1/products/

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

## 📦 Available Commands

### Django-like Management Commands

```bash
# Development Server
python manage.py runserver              # Start server on port 8000
python manage.py runserver --port 8080 # Start on custom port
python manage.py runserver --noreload  # Disable auto-reload

# Migrations (Django-like)
python manage.py makemigrations                    # Auto-detect changes
python manage.py makemigrations -m "description"   # With message
python manage.py makemigrations --empty            # Create empty migration
python manage.py migrate                            # Apply all migrations
python manage.py migrate --downgrade               # Rollback last migration
python manage.py showmigrations                    # Show migration status
python manage.py migrate-check                     # Check for pending migrations
python manage.py migrate-history                    # Show migration history
python manage.py migrate-current                    # Show current migration

# Other Commands
python manage.py shell        # Start Python shell with database
python manage.py test         # Run tests
```

### Make Commands (Shortcuts)

```bash
make help                      # Show all available commands
make install                   # Install dependencies
make runserver                 # Start development server (Django-like)
make runserver-port PORT=8080  # Start on custom port
make dev-up                    # Start with Docker Compose
make dev-down                  # Stop Docker Compose
make build                     # Build Docker images
make logs                      # View service logs
make clean                     # Clean up Docker volumes
make test                      # Run tests

# Migration shortcuts (Django-like)
make makemigrations msg="description"  # Create new migration
make migrate                           # Apply all pending migrations
make migrate-check                     # Check for pending migrations
make migrate-show                      # Show all migrations and status
make migrate-rollback                  # Rollback last migration
make migrate-history                   # Show migration history
make migrate-current                   # Show current migration

# Code quality
make format                   # Format code with black
make lint                     # Lint code with flake8
make shell                    # Start Python shell with database
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

This project uses **Alembic** with a **Django-like** interface for easy migration management.

### Quick Start

```bash
# Check for pending migrations
python manage.py migrate-check

# Show all migrations and their status
python manage.py showmigrations

# Create a new migration (auto-detects model changes)
python manage.py makemigrations -m "add user profile"

# Apply migrations
python manage.py migrate
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `makemigrations` | Create new migration (auto-detect changes) | `python manage.py makemigrations -m "add email field"` |
| `migrate` | Apply all pending migrations | `python manage.py migrate` |
| `showmigrations` | Show all migrations and their status | `python manage.py showmigrations` |
| `migrate-check` | Check for pending migrations | `python manage.py migrate-check` |
| `migrate --downgrade` | Rollback last migration | `python manage.py migrate --downgrade` |
| `migrate-history` | Show migration history | `python manage.py migrate-history` |
| `migrate-current` | Show current migration | `python manage.py migrate-current` |

### Using Make Commands

```bash
make makemigrations msg="add user profile"
make migrate
make migrate-check
make migrate-show
make migrate-rollback
make migrate-history
make migrate-current
```

### Daily Workflow

**Starting work:**
```bash
git pull
python manage.py migrate-check
python manage.py migrate  # if needed
```

**After model changes:**
```bash
python manage.py makemigrations -m "what you changed"
python manage.py migrate
git add alembic/versions/
git commit -m "Add migration: what you changed"
```

### Automatic Migration Checking

The application automatically checks for pending migrations on startup and warns you if any are found. This ensures all developers are working with the same database schema.

### Migration Files

Migration files are automatically named with timestamps for easy tracking:
```
20260113_1724-abc123def456_add_user_email_field.py
```

### Documentation

For comprehensive migration documentation, see:
- **Full Guide**: [docs/MIGRATIONS.md](docs/MIGRATIONS.md)
- **Quick Reference**: [docs/MIGRATIONS_QUICK_REF.md](docs/MIGRATIONS_QUICK_REF.md)

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

1. **SECRET_KEY is Required**: The project will not run without a valid SECRET_KEY (minimum 32 characters)
2. **Use HTTPS**: Enable SSL/TLS in production
3. **Environment Variables**: Never commit `.env` files
4. **Database Credentials**: Use strong passwords
5. **CORS**: Configure allowed origins properly
6. **Token Expiration**: Adjust token expiration times as needed
7. **Keep SECRET_KEY Secret**: Never share or commit your SECRET_KEY

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
