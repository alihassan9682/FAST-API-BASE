# Quick Start Guide

Get up and running with ATB Backend in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Git installed

## Steps

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd ATB-backend
```

### 2. Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env and set your SECRET_KEY (required - project will not run without it)
# SECRET_KEY must be at least 32 characters long
```

### 3. Create and Apply Migrations

```bash
# Create initial migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Start Development Server

```bash
# Start server (Django-like!)
python manage.py runserver

# Or using Make
make runserver

# Or with Docker Compose
make dev-up
```

### 5. Access API Documentation

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 6. Test Authentication

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 7. Create a Product

```bash
# All endpoints are on port 8000 now
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 99.99,
    "stock_quantity": 100,
    "category": "Electronics"
  }'
```

## Common Commands

```bash
# Development server (Django-like)
python manage.py runserver

# Migrations (Django-like)
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Docker commands
make dev-up          # Start with Docker
make dev-down        # Stop Docker
make logs            # View logs
make clean           # Clean everything
```

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 are already in use:

1. Stop conflicting services
2. Or use a different port: `python manage.py runserver --port 8080`

### Database Connection Error

1. Ensure PostgreSQL container is running: `docker ps`
2. Check database credentials in `.env`
3. Wait a few seconds for database to initialize

### Import Errors

If you see import errors when running locally:

1. Ensure you're in the project root
2. Install dependencies: `pip install -r requirements.txt`
3. Check Python path includes project root

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DJANGO_LIKE_GUIDE.md](DJANGO_LIKE_GUIDE.md) for Django-like commands
- Explore the API documentation at http://localhost:8000/docs
- Check out the project structure to understand the architecture
- Add your own apps following the existing pattern

Happy coding! 🚀
