# Migration Quick Reference

## Common Commands

```bash
# Check status
python scripts/migrate.py check
python scripts/migrate.py showmigrations

# Create migration
python scripts/migrate.py makemigrations -m "description"
make makemigrations msg="description"

# Apply migrations
python scripts/migrate.py migrate
make migrate

# Rollback
python scripts/migrate.py rollback
make migrate-rollback

# View current
python scripts/migrate.py current
```

## Daily Workflow

### Starting Work
```bash
git pull
python scripts/migrate.py check
python scripts/migrate.py migrate  # if needed
```

### After Model Changes
```bash
python scripts/migrate.py makemigrations -m "what you changed"
python scripts/migrate.py migrate
git add alembic/versions/
git commit -m "Add migration: what you changed"
```

### Before Pushing
```bash
python scripts/migrate.py showmigrations  # verify
git push
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make makemigrations msg="..."` | Create new migration |
| `make migrate` | Apply migrations |
| `make migrate-check` | Check for pending |
| `make migrate-show` | Show all migrations |
| `make migrate-rollback` | Rollback last |
| `make migrate-history` | Show history |
| `make migrate-current` | Show current |

## Troubleshooting

### Pending migrations warning on startup?
```bash
python scripts/migrate.py showmigrations
python scripts/migrate.py migrate
```

### Need to rollback?
```bash
python scripts/migrate.py rollback
# Or rollback multiple
python scripts/migrate.py rollback -s 3
```

### Merge conflicts in migrations?
```bash
alembic merge heads -m "merge migrations"
python scripts/migrate.py migrate
```
