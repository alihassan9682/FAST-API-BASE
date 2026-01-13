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

# Edit .env and set a strong SECRET_KEY
# You can generate one with: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Start Services

```bash
# Start all services with Docker Compose
make dev-up

# Or manually:
cd infrastructure/docker
docker-compose up -d
```

### 4. Verify Services

Check that services are running:

```bash
# Check service status
docker-compose -f infrastructure/docker/docker-compose.yml ps

# View logs
make logs
```

### 5. Access API Documentation

- **Auth Service**: http://localhost:8000/docs
- **Product Service**: http://localhost:8001/docs

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
# Use the access_token from login response
curl -X POST "http://localhost:8001/api/v1/products/" \
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
# Stop services
make dev-down

# View logs
make logs

# Restart services
make dev-down && make dev-up

# Clean everything
make clean
```

## Troubleshooting

### Port Already in Use

If ports 8000, 8001, or 5432 are already in use:

1. Stop conflicting services
2. Or change ports in `.env` and `docker-compose.yml`

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
- Explore the API documentation at http://localhost:8000/docs
- Check out the project structure to understand the architecture
- Add your own microservices following the existing pattern

Happy coding! 🚀
