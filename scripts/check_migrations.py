"""
Automatic migration checker for application startup.
Warns developers if there are pending migrations.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from core.config import settings
from core.logger import logger


def check_migrations_on_startup(strict: bool = False):
    """
    Check for pending migrations on application startup.
    
    Args:
        strict: If True, raise an exception if pending migrations are found.
                If False, just log a warning.
    """
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        script = ScriptDirectory.from_config(alembic_cfg)
        
        # Get current revision from database
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                current_rev = result.scalar()
            except Exception:
                current_rev = None
        
        # Get head revision
        head_rev = script.get_current_head()
        
        if current_rev != head_rev:
            message = (
                "\n" + "=" * 80 + "\n"
                "⚠️  WARNING: PENDING MIGRATIONS DETECTED!\n"
                "=" * 80 + "\n"
                f"Current database revision: {current_rev or 'None (empty database)'}\n"
                f"Latest migration revision:  {head_rev}\n"
                "\n"
                "Your database is not up to date with the latest migrations.\n"
                "This may cause errors or unexpected behavior.\n"
                "\n"
                "To fix this, run:\n"
                "  python scripts/migrate.py showmigrations  # See pending migrations\n"
                "  python scripts/migrate.py migrate         # Apply migrations\n"
                "\n"
                "Or using Make:\n"
                "  make migrate-show\n"
                "  make migrate\n"
                "=" * 80 + "\n"
            )
            
            if strict:
                logger.error(message)
                raise RuntimeError(
                    "Pending migrations detected. "
                    "Please apply migrations before starting the application."
                )
            else:
                logger.warning(message)
        else:
            logger.info("✅ Database migrations are up to date")
            
    except Exception as e:
        if strict:
            raise
        else:
            logger.warning(f"Could not check migration status: {e}")


def check_migrations_cli():
    """
    CLI version of migration checker.
    Returns exit code 1 if pending migrations exist, 0 otherwise.
    """
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        script = ScriptDirectory.from_config(alembic_cfg)
        
        # Get current revision from database
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                current_rev = result.scalar()
            except Exception:
                current_rev = None
        
        # Get head revision
        head_rev = script.get_current_head()
        
        if current_rev != head_rev:
            print("⚠️  Pending migrations detected!")
            print(f"Current: {current_rev or 'None'}")
            print(f"Latest:  {head_rev}")
            return 1
        else:
            print("✅ No pending migrations")
            return 0
            
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(check_migrations_cli())
