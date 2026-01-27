#!/usr/bin/env python
"""
Django-like migration management script for Alembic.
Provides commands similar to Django's migration system.
"""
import sys
import os
from pathlib import Path
import subprocess
import argparse
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from core.config import settings


class MigrationManager:
    """Manages database migrations with Django-like commands."""
    
    def __init__(self):
        self.alembic_cfg = Config("alembic.ini")
        self.alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        self.script = ScriptDirectory.from_config(self.alembic_cfg)
        
    def makemigrations(self, message: str = None):
        """
        Create a new migration file (like Django's makemigrations).
        Automatically detects model changes.
        """
        if not message:
            message = f"auto_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🔍 Detecting model changes...")
        print(f"📝 Creating migration: {message}")
        
        try:
            command.revision(
                self.alembic_cfg,
                autogenerate=True,
                message=message
            )
            print(f"✅ Migration created successfully!")
            print(f"\n💡 Next step: Run 'python scripts/migrate.py migrate' to apply migrations")
        except Exception as e:
            print(f"❌ Error creating migration: {e}")
            sys.exit(1)
    
    def migrate(self, revision: str = "head"):
        """
        Apply migrations to the database (like Django's migrate).
        """
        print(f"🚀 Applying migrations to database...")
        
        try:
            # Check for pending migrations first
            pending = self.check_pending()
            if not pending:
                print("✅ No pending migrations to apply.")
                return
            
            command.upgrade(self.alembic_cfg, revision)
            print(f"✅ Migrations applied successfully!")
        except Exception as e:
            print(f"❌ Error applying migrations: {e}")
            sys.exit(1)
    
    def rollback(self, steps: int = 1):
        """
        Rollback migrations (like Django's migrate app_name migration_name).
        """
        print(f"⏪ Rolling back {steps} migration(s)...")
        
        try:
            revision = f"-{steps}"
            command.downgrade(self.alembic_cfg, revision)
            print(f"✅ Rollback completed successfully!")
        except Exception as e:
            print(f"❌ Error rolling back: {e}")
            sys.exit(1)
    
    def showmigrations(self):
        """
        Show all migrations and their status (like Django's showmigrations).
        """
        print("📋 Migration Status:\n")
        print("=" * 80)
        
        try:
            # Get current revision from database
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                try:
                    result = conn.execute(text("SELECT version_num FROM alembic_version"))
                    current_rev = result.scalar()
                except Exception:
                    current_rev = None
            
            # Get all revisions
            revisions = list(self.script.walk_revisions())
            
            if not revisions:
                print("No migrations found.")
                return
            
            # Reverse to show oldest first
            revisions.reverse()
            
            applied_count = 0
            pending_count = 0
            found_current = current_rev is None
            
            for rev in revisions:
                is_applied = found_current
                
                if rev.revision == current_rev:
                    found_current = True
                    is_applied = True
                
                status = "✅ APPLIED" if is_applied else "⏳ PENDING"
                
                if is_applied:
                    applied_count += 1
                else:
                    pending_count += 1
                
                # Format the output
                print(f"{status:12} | {rev.revision[:12]} | {rev.doc or 'No description'}")
            
            print("=" * 80)
            print(f"\n📊 Summary:")
            print(f"   Applied: {applied_count}")
            print(f"   Pending: {pending_count}")
            print(f"   Total:   {len(revisions)}")
            
            if pending_count > 0:
                print(f"\n⚠️  You have {pending_count} pending migration(s)!")
                print(f"💡 Run 'python scripts/migrate.py migrate' to apply them.")
            else:
                print(f"\n✅ All migrations are up to date!")
                
        except Exception as e:
            print(f"❌ Error showing migrations: {e}")
            sys.exit(1)
    
    def check_pending(self) -> bool:
        """
        Check if there are pending migrations.
        Returns True if there are pending migrations, False otherwise.
        """
        try:
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                try:
                    result = conn.execute(text("SELECT version_num FROM alembic_version"))
                    current_rev = result.scalar()
                except Exception:
                    # Table doesn't exist, all migrations are pending
                    return True
            
            # Get head revision
            head_rev = self.script.get_current_head()
            
            return current_rev != head_rev
        except Exception as e:
            print(f"⚠️  Warning: Could not check pending migrations: {e}")
            return False
    
    def history(self, limit: int = 10):
        """
        Show migration history.
        """
        print(f"📜 Migration History (last {limit}):\n")
        print("=" * 80)
        
        try:
            revisions = list(self.script.walk_revisions())[:limit]
            
            if not revisions:
                print("No migrations found.")
                return
            
            for rev in revisions:
                print(f"Revision: {rev.revision}")
                print(f"Message:  {rev.doc or 'No description'}")
                print(f"Created:  {rev.revision[:8]}")
                print(f"Down:     {rev.down_revision or 'None'}")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ Error showing history: {e}")
            sys.exit(1)
    
    def current(self):
        """
        Show current migration revision.
        """
        print("🔍 Current Migration:\n")
        
        try:
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                try:
                    result = conn.execute(text("SELECT version_num FROM alembic_version"))
                    current_rev = result.scalar()
                    
                    if current_rev:
                        rev = self.script.get_revision(current_rev)
                        print(f"Revision: {rev.revision}")
                        print(f"Message:  {rev.doc or 'No description'}")
                        print(f"✅ Database is at this revision")
                    else:
                        print("⚠️  No migrations applied yet")
                        
                except Exception:
                    print("⚠️  Migration table doesn't exist. Run migrations first.")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the migration script."""
    parser = argparse.ArgumentParser(
        description="Django-like migration management for Alembic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/migrate.py makemigrations -m "add user table"
  python scripts/migrate.py migrate
  python scripts/migrate.py showmigrations
  python scripts/migrate.py rollback
  python scripts/migrate.py check
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # makemigrations command
    make_parser = subparsers.add_parser(
        "makemigrations",
        help="Create a new migration (auto-detects changes)"
    )
    make_parser.add_argument(
        "-m", "--message",
        help="Migration message/description",
        default=None
    )
    
    # migrate command
    migrate_parser = subparsers.add_parser(
        "migrate",
        help="Apply pending migrations"
    )
    migrate_parser.add_argument(
        "revision",
        nargs="?",
        default="head",
        help="Target revision (default: head)"
    )
    
    # rollback command
    rollback_parser = subparsers.add_parser(
        "rollback",
        help="Rollback migrations"
    )
    rollback_parser.add_argument(
        "-s", "--steps",
        type=int,
        default=1,
        help="Number of migrations to rollback (default: 1)"
    )
    
    # showmigrations command
    subparsers.add_parser(
        "showmigrations",
        help="Show all migrations and their status"
    )
    
    # check command
    subparsers.add_parser(
        "check",
        help="Check for pending migrations"
    )
    
    # history command
    history_parser = subparsers.add_parser(
        "history",
        help="Show migration history"
    )
    history_parser.add_argument(
        "-l", "--limit",
        type=int,
        default=10,
        help="Number of migrations to show (default: 10)"
    )
    
    # current command
    subparsers.add_parser(
        "current",
        help="Show current migration revision"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = MigrationManager()
    
    # Execute the appropriate command
    if args.command == "makemigrations":
        manager.makemigrations(args.message)
    elif args.command == "migrate":
        manager.migrate(args.revision)
    elif args.command == "rollback":
        manager.rollback(args.steps)
    elif args.command == "showmigrations":
        manager.showmigrations()
    elif args.command == "check":
        has_pending = manager.check_pending()
        if has_pending:
            print("⚠️  You have pending migrations!")
            print("💡 Run 'python scripts/migrate.py showmigrations' to see them.")
            sys.exit(1)
        else:
            print("✅ No pending migrations. Database is up to date!")
            sys.exit(0)
    elif args.command == "history":
        manager.history(args.limit)
    elif args.command == "current":
        manager.current()


if __name__ == "__main__":
    main()
