#!/usr/bin/env python3
"""
Django-like management script for ATB Backend.
Usage: python manage.py <command> [options]
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import argparse
from typing import List, Optional


def runserver(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Run the development server (like Django's runserver)."""
    import uvicorn
    from core.config import settings
    
    print(f"🚀 Starting development server at http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("\nPress CTRL+C to quit\n")
    
    uvicorn.run(
        "apps.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


def makemigrations(message: Optional[str] = None, empty: bool = False):
    """Create new migration files (like Django's makemigrations)."""
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    
    alembic_cfg = Config("alembic.ini")
    
    if empty:
        # Create empty migration
        if not message:
            message = "empty migration"
        command.revision(alembic_cfg, message=message, autogenerate=False)
    else:
        # Auto-generate migration from model changes
        if not message:
            message = "auto migration"
        command.revision(alembic_cfg, message=message, autogenerate=True)
    
    print("✅ Migration file created successfully!")
    print("💡 Run 'python manage.py migrate' to apply migrations")


def migrate(target: Optional[str] = None, downgrade: bool = False):
    """Apply database migrations (like Django's migrate)."""
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    
    alembic_cfg = Config("alembic.ini")
    
    if downgrade:
        # Rollback one migration
        command.downgrade(alembic_cfg, "-1")
        print("✅ Rolled back last migration")
    elif target:
        # Migrate to specific revision
        command.upgrade(alembic_cfg, target)
        print(f"✅ Migrated to revision: {target}")
    else:
        # Migrate to latest (head)
        command.upgrade(alembic_cfg, "head")
        print("✅ All migrations applied successfully!")


def showmigrations():
    """Show migration status (like Django's showmigrations)."""
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
    from core.config import settings
    
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    
    # Connect to database to check current revision
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
    
    print("\n📋 Migration Status:")
    print("=" * 80)
    
    # Get all migrations
    revisions = list(script.walk_revisions())
    revisions.reverse()  # Show oldest first
    
    for rev in revisions:
        status = "✅" if rev.revision == current_rev else ("⏳" if current_rev else "❌")
        if rev.revision == current_rev:
            print(f"{status} [{rev.revision[:8]}] {rev.doc} (current)")
        else:
            print(f"{status} [{rev.revision[:8]}] {rev.doc}")
    
    print("=" * 80)
    if current_rev:
        print(f"Current revision: {current_rev}")
    else:
        print("⚠️  No migrations applied yet. Run 'python manage.py migrate' to apply.")


def migrate_check():
    """Check for pending migrations (like Django's migrate --check)."""
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
    from core.config import settings
    
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
        head_rev = script.get_current_head()
    
    if current_rev != head_rev:
        print("⚠️  You have unapplied migrations!")
        print(f"   Current: {current_rev or 'None'}")
        print(f"   Head: {head_rev}")
        print("   Run 'python manage.py migrate' to apply them.")
        sys.exit(1)
    else:
        print("✅ All migrations are up to date!")


def migrate_history():
    """Show migration history."""
    from alembic.config import Config
    from alembic.script import ScriptDirectory
    
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    
    print("\n📜 Migration History:")
    print("=" * 80)
    
    revisions = list(script.walk_revisions())
    revisions.reverse()
    
    for rev in revisions:
        print(f"[{rev.revision[:8]}] {rev.doc}")
        if rev.down_revision:
            print(f"    ↓ from {rev.down_revision[:8]}")
    
    print("=" * 80)


def migrate_current():
    """Show current migration."""
    from alembic.config import Config
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
    from core.config import settings
    
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
    
    if current_rev:
        print(f"Current migration: {current_rev}")
    else:
        print("⚠️  No migrations applied yet.")


def shell():
    """Start Python shell with database session (like Django's shell)."""
    from core.database import SessionLocal
    from core.config import settings
    
    db = SessionLocal()
    print("🐍 Starting Python shell with database session...")
    print("💡 Use 'db' variable to access database session")
    print("💡 Example: from apps.auth_service.db.models.user import User; db.query(User).all()")
    print("💡 Type 'exit' to quit\n")
    
    try:
        from IPython import embed
        embed()
    except ImportError:
        print("⚠️  IPython not installed. Using standard Python shell.")
        print("💡 Install IPython for better experience: pip install ipython\n")
        import code
        code.interact(local={"db": db, "settings": settings})


def collectstatic():
    """Collect static files (placeholder for future use)."""
    print("📦 Static files collection (not implemented yet)")


def test():
    """Run tests."""
    import subprocess
    result = subprocess.run(["pytest", "tests/", "-v"])
    sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="Django-like management script for ATB Backend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py runserver              # Start development server
  python manage.py runserver --port 8080  # Start on port 8080
  python manage.py makemigrations         # Create migration
  python manage.py makemigrations -m "add field"  # Create with message
  python manage.py migrate                 # Apply migrations
  python manage.py migrate --downgrade     # Rollback last migration
  python manage.py showmigrations          # Show migration status
  python manage.py migrate-check          # Check for pending migrations
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # runserver command
    runserver_parser = subparsers.add_parser("runserver", help="Start development server")
    runserver_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    runserver_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    runserver_parser.add_argument("--noreload", action="store_true", help="Disable auto-reload")
    
    # makemigrations command
    makemigrations_parser = subparsers.add_parser("makemigrations", help="Create new migration")
    makemigrations_parser.add_argument("-m", "--message", help="Migration message")
    makemigrations_parser.add_argument("--empty", action="store_true", help="Create empty migration")
    
    # migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Apply migrations")
    migrate_parser.add_argument("target", nargs="?", help="Target revision (default: head)")
    migrate_parser.add_argument("--downgrade", action="store_true", help="Rollback last migration")
    
    # showmigrations command
    subparsers.add_parser("showmigrations", help="Show migration status")
    
    # migrate-check command
    subparsers.add_parser("migrate-check", help="Check for pending migrations")
    
    # migrate-history command
    subparsers.add_parser("migrate-history", help="Show migration history")
    
    # migrate-current command
    subparsers.add_parser("migrate-current", help="Show current migration")
    
    # shell command
    subparsers.add_parser("shell", help="Start Python shell with database")
    
    # collectstatic command
    subparsers.add_parser("collectstatic", help="Collect static files")
    
    # test command
    subparsers.add_parser("test", help="Run tests")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "runserver":
            runserver(host=args.host, port=args.port, reload=not args.noreload)
        elif args.command == "makemigrations":
            makemigrations(message=args.message, empty=args.empty)
        elif args.command == "migrate":
            if args.downgrade:
                migrate(downgrade=True)
            else:
                migrate(target=args.target)
        elif args.command == "showmigrations":
            showmigrations()
        elif args.command == "migrate-check":
            migrate_check()
        elif args.command == "migrate-history":
            migrate_history()
        elif args.command == "migrate-current":
            migrate_current()
        elif args.command == "shell":
            shell()
        elif args.command == "collectstatic":
            collectstatic()
        elif args.command == "test":
            test()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
