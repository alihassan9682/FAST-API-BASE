# Database Migrations Guide

This project uses **Alembic** for database migrations with a **Django-like** interface for ease of use.

## Quick Start

### 1. Check Migration Status
```bash
# Check if there are pending migrations
python scripts/migrate.py check

# Show all migrations and their status
python scripts/migrate.py showmigrations
```

### 2. Create New Migrations
```bash
# Auto-detect model changes and create migration
python scripts/migrate.py makemigrations -m "add user profile fields"

# Or using Make
make makemigrations msg="add user profile fields"
```

### 3. Apply Migrations
```bash
# Apply all pending migrations
python scripts/migrate.py migrate

# Or using Make
make migrate
```

## Available Commands

### Django-like Commands

| Command | Description | Example |
|---------|-------------|---------|
| `makemigrations` | Create a new migration (auto-detects changes) | `python scripts/migrate.py makemigrations -m "add email field"` |
| `migrate` | Apply all pending migrations | `python scripts/migrate.py migrate` |
| `showmigrations` | Show all migrations and their status | `python scripts/migrate.py showmigrations` |
| `check` | Check for pending migrations | `python scripts/migrate.py check` |
| `rollback` | Rollback migrations | `python scripts/migrate.py rollback -s 2` |
| `history` | Show migration history | `python scripts/migrate.py history -l 20` |
| `current` | Show current migration revision | `python scripts/migrate.py current` |

### Using Make Commands

```bash
make makemigrations msg="your migration message"
make migrate
make migrate-check
make migrate-show
make migrate-rollback
make migrate-history
make migrate-current
```

## Workflow

### Adding a New Model

1. **Create/modify your model** in `apps/<service>/db/models/`

2. **Import the model** in `alembic/env.py`:
   ```python
   from apps.your_service.db.models.your_model import YourModel
   ```

3. **Create migration**:
   ```bash
   python scripts/migrate.py makemigrations -m "add your_model table"
   ```

4. **Review the migration** in `alembic/versions/`

5. **Apply migration**:
   ```bash
   python scripts/migrate.py migrate
   ```

### Modifying an Existing Model

1. **Update your model** in `apps/<service>/db/models/`

2. **Create migration**:
   ```bash
   python scripts/migrate.py makemigrations -m "add field to user"
   ```

3. **Review and apply**:
   ```bash
   python scripts/migrate.py showmigrations
   python scripts/migrate.py migrate
   ```

## Best Practices

### 1. Always Check Before Starting Development
```bash
# Check for pending migrations
python scripts/migrate.py check

# If there are pending migrations, apply them
python scripts/migrate.py migrate
```

### 2. Descriptive Migration Messages
```bash
# ✅ Good
python scripts/migrate.py makemigrations -m "add email_verified field to user"
python scripts/migrate.py makemigrations -m "create product_category table"

# ❌ Bad
python scripts/migrate.py makemigrations -m "update"
python scripts/migrate.py makemigrations -m "fix"
```

### 3. Review Migrations Before Applying
Always review the generated migration file in `alembic/versions/` before applying it to production.

### 4. Never Edit Applied Migrations
Once a migration has been applied (especially in production), never edit it. Create a new migration instead.

### 5. Keep Migrations Small
Create separate migrations for different changes rather than one large migration.

## Team Collaboration

### When Pulling Changes

1. **Pull the latest code**:
   ```bash
   git pull origin main
   ```

2. **Check for new migrations**:
   ```bash
   python scripts/migrate.py showmigrations
   ```

3. **Apply new migrations**:
   ```bash
   python scripts/migrate.py migrate
   ```

### When Creating Migrations

1. **Pull latest changes first**:
   ```bash
   git pull origin main
   python scripts/migrate.py migrate
   ```

2. **Create your migration**:
   ```bash
   python scripts/migrate.py makemigrations -m "your changes"
   ```

3. **Test the migration**:
   ```bash
   python scripts/migrate.py migrate
   # Test your application
   python scripts/migrate.py rollback  # If needed
   ```

4. **Commit and push**:
   ```bash
   git add alembic/versions/
   git commit -m "Add migration: your changes"
   git push
   ```

## Automatic Migration Checking

The application can automatically check for pending migrations on startup. See `scripts/check_migrations.py`.

### Enable Startup Check

Add this to your `apps/main.py`:

```python
from scripts.check_migrations import check_migrations_on_startup

@app.on_event("startup")
async def startup_event():
    logger.info("Unified application starting up...")
    check_migrations_on_startup()  # Add this line
```

## Troubleshooting

### "No module named 'alembic'"
```bash
pip install alembic
```

### "Target database is not up to date"
```bash
python scripts/migrate.py showmigrations
python scripts/migrate.py migrate
```

### "Multiple head revisions"
This happens when multiple developers create migrations simultaneously. You need to merge them:
```bash
alembic merge heads -m "merge migrations"
python scripts/migrate.py migrate
```

### "Can't locate revision"
```bash
# Reset to a specific revision
python scripts/migrate.py migrate <revision_id>

# Or start fresh (⚠️ DANGER: This will drop all tables!)
# Only do this in development
python scripts/migrate.py migrate base
python scripts/migrate.py migrate head
```

## Migration File Naming

Migration files are automatically named with timestamps:
```
20260113_1724-abc123def456_add_user_email_field.py
```

Format: `YYYYMMDD_HHMM-<revision>_<message>.py`

This makes it easy to:
- See when migrations were created
- Maintain chronological order
- Identify migrations quickly

## Advanced Usage

### Rollback Multiple Migrations
```bash
python scripts/migrate.py rollback -s 3  # Rollback 3 migrations
```

### Migrate to Specific Revision
```bash
python scripts/migrate.py migrate abc123def456
```

### Show More History
```bash
python scripts/migrate.py history -l 50  # Show last 50 migrations
```

## CI/CD Integration

### In Your CI Pipeline

```yaml
# .github/workflows/ci.yml
- name: Check for pending migrations
  run: |
    python scripts/migrate.py check
    if [ $? -eq 1 ]; then
      echo "⚠️ Pending migrations detected!"
      exit 1
    fi
```

### Pre-deployment

```bash
# Always run migrations before deploying
python scripts/migrate.py migrate
```

## Database Backup

Always backup your database before applying migrations in production:

```bash
# PostgreSQL example
pg_dump -U user -d database > backup_$(date +%Y%m%d_%H%M%S).sql

# Then apply migrations
python scripts/migrate.py migrate
```

## Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Django Migrations (for reference)](https://docs.djangoproject.com/en/stable/topics/migrations/)
