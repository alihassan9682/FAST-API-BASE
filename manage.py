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


def makemigrations(message: Optional[str] = None, empty: bool = False, dry_run: bool = False):
    """
    Create new migration files (like Django's makemigrations).
    
    Only creates migrations if there are actual model changes.
    Shows output similar to Django's makemigrations command.
    """
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    from alembic.autogenerate import compare_metadata
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
    from core.config import settings
    from core.database import TimestampBase
    from datetime import datetime
    import os
    
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    script = ScriptDirectory.from_config(alembic_cfg)
    
    # Check if database is up to date first (Django-like)
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_rev = context.get_current_revision()
            head_rev = script.get_current_head()
            
            if current_rev != head_rev:
                print("\n❌ Error: Target database is not up to date.")
                print(f"   Current: {current_rev or 'None'}")
                print(f"   Head: {head_rev}")
                print("   Run 'python manage.py migrate' first to apply pending migrations.")
                sys.exit(1)
    except Exception:
        # If database doesn't exist or connection fails, continue
        # (first migration scenario)
        pass
    
    # Django-like output
    print("Migrations for '':")
    
    if empty:
        # Create empty migration
        if not message:
            message = "empty migration"
        
        if dry_run:
            print(f"  Would create empty migration: {message}")
            return
        
        print(f"  Creating {message}...")
        try:
            rev = command.revision(alembic_cfg, message=message, autogenerate=False)
            if rev:
                rev_str = rev if isinstance(rev, str) else rev.revision
                # Get the created migration file
                try:
                    migration = script.get_revision(rev_str)
                    if migration:
                        rel_path = os.path.relpath(migration.path, os.getcwd())
                        print(f"    - Create migration {rev_str[:8]}")
                        print(f"\n✅ Created migration file: {rel_path}")
                except:
                    print(f"    - Create migration {rev_str[:8]}")
                    print(f"\n✅ Created migration: {rev_str[:8]}")
        except Exception as e:
            if "Target database is not up to date" in str(e):
                print("\n❌ Error: Target database is not up to date.")
                print("   Run 'python manage.py migrate' first to apply pending migrations.")
                sys.exit(1)
            else:
                raise
    else:
        # Auto-generate migration from model changes
        # First, check if there are actual changes
        try:
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                
                # Compare current database state with models
                diffs = compare_metadata(context, TimestampBase.metadata)
                
                # Filter out false positives (like sequence detections)
                # Only consider real changes: tables, columns, indexes, constraints
                real_changes = []
                for diff in diffs:
                    # Check if it's a meaningful change
                    if hasattr(diff, 'add_table') or hasattr(diff, 'remove_table'):
                        real_changes.append(diff)
                    elif hasattr(diff, 'add_column') or hasattr(diff, 'remove_column'):
                        real_changes.append(diff)
                    elif hasattr(diff, 'modify_column'):
                        # Check if it's a real modification, not just a comment/sequence detection
                        real_changes.append(diff)
                    elif hasattr(diff, 'add_index') or hasattr(diff, 'remove_index'):
                        real_changes.append(diff)
                    elif hasattr(diff, 'add_constraint') or hasattr(diff, 'remove_constraint'):
                        real_changes.append(diff)
                
                if not real_changes:
                    print("No changes detected")
                    return
        except Exception:
            # If we can't compare (e.g., database doesn't exist), continue to create migration
            pass
        
        if not message:
            # Use timestamp for default message (Django-like)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message = f"auto_migration_{timestamp}"
        
        if dry_run:
            print(f"  Would detect changes and create migration: {message}")
            return
        
        print(f"  Detecting changes...")
        try:
            # Temporarily capture stdout to check if migration has actual changes
            import io
            import contextlib
            
            # Create migration
            rev = command.revision(alembic_cfg, message=message, autogenerate=True)
            
            if rev:
                rev_str = rev if isinstance(rev, str) else rev.revision
                # Check if the migration file has actual changes (not just pass)
                try:
                    migration = script.get_revision(rev_str)
                    if migration:
                        # Read the migration file to check if it's empty
                        with open(migration.path, 'r') as f:
                            content = f.read()
                        
                        # Check if upgrade() function has actual operations (not just pass)
                        if 'def upgrade() -> None:' in content:
                            # Extract upgrade function content
                            upgrade_start = content.find('def upgrade() -> None:')
                            upgrade_end = content.find('def downgrade() -> None:', upgrade_start)
                            if upgrade_end == -1:
                                upgrade_end = len(content)
                            
                            upgrade_content = content[upgrade_start:upgrade_end]
                            
                            # Check if it's just "pass" or has actual operations
                            if 'pass' in upgrade_content and upgrade_content.strip().count('\n') <= 2:
                                # Migration is empty, delete it
                                os.remove(migration.path)
                                print("No changes detected")
                                return
                        
                        rel_path = os.path.relpath(migration.path, os.getcwd())
                        print(f"    - Create migration {rev_str[:8]}: {message}")
                        print(f"\n✅ Created migration file: {rel_path}")
                    else:
                        print(f"    - Create migration {rev_str[:8]}: {message}")
                        print(f"\n✅ Created migration: {rev_str[:8]}")
                except Exception as e:
                    # If we can't read the file, assume it's valid
                    print(f"    - Create migration {rev_str[:8]}: {message}")
                    print(f"\n✅ Created migration: {rev_str[:8]}")
            else:
                print("No changes detected")
                return
        except Exception as e:
            error_msg = str(e)
            if "Target database is not up to date" in error_msg:
                print("\n❌ Error: Target database is not up to date.")
                print("   Run 'python manage.py migrate' first to apply pending migrations.")
                sys.exit(1)
            elif "No changes detected" in error_msg or "No changes" in error_msg:
                print("No changes detected")
                return
            else:
                raise
    
    print("💡 Run 'python manage.py migrate' to apply migrations")


def migrate(target: Optional[str] = None, downgrade: bool = False, plan: bool = False):
    """
    Apply database migrations (like Django's migrate).
    
    Shows operations to perform and applies migrations step by step.
    """
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
    from core.config import settings
    
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    script = ScriptDirectory.from_config(alembic_cfg)
    
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
        head_rev = script.get_current_head()
    
    if downgrade:
        # Rollback one migration (Django-like)
        if not current_rev:
            print("No migrations to rollback.")
            return
        
        current = script.get_revision(current_rev)
        if current and current.down_revision:
            prev_rev = current.down_revision
            prev = script.get_revision(prev_rev)
            print("Operations to perform:")
            print(f"  Rollback {current_rev[:8]}: {current.doc}")
            if prev:
                print(f"  Target: {prev_rev[:8]}: {prev.doc}")
            print("\nRunning migrations:")
            print(f"  Rolling back {current_rev[:8]}: {current.doc}... ", end="", flush=True)
            command.downgrade(alembic_cfg, "-1")
            print("OK")
            print("\n✅ Rolled back last migration")
        else:
            print("No previous migration to rollback to.")
        return
    
    if plan:
        # Show migration plan without applying (Django-like)
        if current_rev == head_rev:
            print("No migrations to apply.")
            return
        
        print("Planned migrations:")
        # Get list of migrations to apply
        rev = script.get_revision(head_rev)
        migrations_to_apply = []
        while rev and rev.revision != current_rev:
            migrations_to_apply.append(rev)
            if rev.down_revision:
                rev = script.get_revision(rev.down_revision)
            else:
                break
        
        migrations_to_apply.reverse()
        
        for rev in migrations_to_apply:
            print(f"  [{rev.revision[:8]}] {rev.doc}")
        
        return
    
    # Normal migrate - apply all pending migrations (Django-like)
    if current_rev == head_rev:
        print("No migrations to apply.")
        return
    
    # Get list of migrations to apply
    rev = script.get_revision(head_rev)
    migrations_to_apply = []
    while rev and rev.revision != current_rev:
        migrations_to_apply.append(rev)
        if rev.down_revision:
            rev = script.get_revision(rev.down_revision)
        else:
            break
    
    migrations_to_apply.reverse()
    
    print("Operations to perform:")
    print(f"  Apply all migrations: '{current_rev[:8] if current_rev else 'None'}' -> '{head_rev[:8]}'")
    print(f"\nRunning migrations:")
    
    # Apply migrations one by one (Django-like)
    for rev in migrations_to_apply:
        print(f"  Applying {rev.revision[:8]}: {rev.doc}... ", end="", flush=True)
        try:
            if target:
                command.upgrade(alembic_cfg, target)
                break
            else:
                command.upgrade(alembic_cfg, rev.revision)
            print("OK")
        except Exception as e:
            print("FAILED")
            raise
    
    if not target:
        print("\n✅ All migrations applied successfully!")
    else:
        print(f"\n✅ Migrated to revision: {target}")


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
    
    # makemigrations command (Django-like)
    makemigrations_parser = subparsers.add_parser("makemigrations", help="Create new migration files")
    makemigrations_parser.add_argument("-m", "--message", help="Migration message/description")
    makemigrations_parser.add_argument("--empty", action="store_true", help="Create empty migration")
    makemigrations_parser.add_argument("--dry-run", action="store_true", help="Show what would be created without creating")
    
    # migrate command (Django-like)
    migrate_parser = subparsers.add_parser("migrate", help="Apply database migrations")
    migrate_parser.add_argument("target", nargs="?", help="Target revision (default: head)")
    migrate_parser.add_argument("--downgrade", action="store_true", help="Rollback last migration")
    migrate_parser.add_argument("--plan", action="store_true", help="Show migration plan without applying")
    
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
            makemigrations(message=args.message, empty=args.empty, dry_run=args.dry_run)
        elif args.command == "migrate":
            if args.plan:
                migrate(plan=True)
            elif args.downgrade:
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
