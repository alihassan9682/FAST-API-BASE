# Django-like Commands Guide

This project provides Django-like management commands through `manage.py`. All apps run on a single port, just like Django.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your configuration

# 3. Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Start development server
python manage.py runserver
```

## 📋 Available Commands

### Development Server

```bash
# Start server on default port (8000)
python manage.py runserver

# Start on custom port
python manage.py runserver --port 8080

# Start without auto-reload
python manage.py runserver --noreload

# Start on custom host and port
python manage.py runserver --host 0.0.0.0 --port 8000
```

**Equivalent to Django's:** `python manage.py runserver`

### Migrations

#### Create Migrations

```bash
# Auto-detect model changes (recommended)
python manage.py makemigrations

# With custom message
python manage.py makemigrations -m "Add email field to user"

# Create empty migration
python manage.py makemigrations --empty -m "Custom data migration"
```

**Equivalent to Django's:** `python manage.py makemigrations`

#### Apply Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Apply to specific revision
python manage.py migrate <revision_id>
```

**Equivalent to Django's:** `python manage.py migrate`

#### Check Migrations

```bash
# Show migration status
python manage.py showmigrations

# Check for pending migrations (exits with error if pending)
python manage.py migrate-check

# Show migration history
python manage.py migrate-history

# Show current migration
python manage.py migrate-current
```

**Equivalent to Django's:** `python manage.py showmigrations`

#### Rollback Migrations

```bash
# Rollback last migration
python manage.py migrate --downgrade
```

**Equivalent to Django's:** `python manage.py migrate <previous_revision>`

### Shell

```bash
# Start Python shell with database session
python manage.py shell
```

**Equivalent to Django's:** `python manage.py shell`

In the shell, you have access to:
- `db` - Database session
- `settings` - Application settings
- All your models (User, Product, etc.)

Example:
```python
>>> from apps.auth_service.db.models.user import User
>>> users = db.query(User).all()
>>> print(users)
```

### Testing

```bash
# Run tests
python manage.py test
```

**Equivalent to Django's:** `python manage.py test`

## 🏗️ Project Structure (Django-like)

```
ATB-BE/
├── apps/                    # Like Django's apps directory
│   ├── auth_service/        # App 1: Authentication
│   │   ├── api/            # API endpoints (like views)
│   │   ├── db/models/      # Database models
│   │   ├── schemas/        # Pydantic schemas (like serializers)
│   │   └── services/       # Business logic
│   ├── product_service/    # App 2: Products
│   └── main.py            # Unified FastAPI app (like Django's wsgi.py)
├── core/                   # Shared core (like Django's settings)
├── manage.py              # Management script (like Django's manage.py)
└── alembic/               # Migrations (like Django's migrations/)
```

## 🔄 Migration Workflow

### 1. Make Model Changes

Edit your model in `apps/<app_name>/db/models/<model>.py`:

```python
class User(Base):
    # ... existing fields ...
    new_field = Column(String, nullable=True)  # Add new field
```

### 2. Create Migration

```bash
python manage.py makemigrations
```

This will:
- Auto-detect changes in all models
- Create a new migration file in `alembic/versions/`
- Show you what changes were detected

### 3. Review Migration

Check the generated migration file in `alembic/versions/` to ensure it's correct.

### 4. Apply Migration

```bash
python manage.py migrate
```

This will:
- Apply all pending migrations
- Update your database schema
- Show which migrations were applied

### 5. Verify

```bash
python manage.py showmigrations
```

## 🆚 Differences from Django

While the commands are similar, there are some differences:

1. **Models**: Uses SQLAlchemy instead of Django ORM
2. **Migrations**: Uses Alembic instead of Django migrations
3. **API**: Uses FastAPI instead of Django REST Framework
4. **Schemas**: Uses Pydantic instead of Django serializers

## 💡 Tips

1. **Always create migrations after model changes**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Check migration status before deploying**
   ```bash
   python manage.py migrate-check
   ```

3. **Use descriptive migration messages**
   ```bash
   python manage.py makemigrations -m "Add email verification field"
   ```

4. **Review migrations before applying**
   - Always check generated migration files
   - Test migrations on development database first

5. **Single Port Architecture**
   - All apps run on one port (default: 8000)
   - Access all endpoints at `http://localhost:8000/api/v1/`
   - API docs at `http://localhost:8000/docs`

## 🐛 Troubleshooting

### Migration Issues

**Problem:** Migration not detecting changes
```bash
# Make sure models are imported in alembic/env.py
# Then try:
python manage.py makemigrations -m "Force migration"
```

**Problem:** Migration conflicts
```bash
# Check current state
python manage.py showmigrations

# Rollback if needed
python manage.py migrate --downgrade
```

### Server Issues

**Problem:** Port already in use
```bash
# Use different port
python manage.py runserver --port 8080
```

**Problem:** Import errors
```bash
# Make sure you're in project root
# Install dependencies
pip install -r requirements.txt
```

## 📚 More Information

- See `README.md` for full project documentation
- See `QUICKSTART.md` for quick setup guide
- API documentation at `http://localhost:8000/docs` when server is running
