#!/usr/bin/env python3
"""
Migration runner script.
Run this from the backend root directory: python run_migrations.py
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path so 'src' imports work
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def run_migration(migration_name: str, conn_string: str):
    """Run a specific migration by name."""
    try:
        # Import the migration client dynamically
        from src.db.migrations.migration_client import client

        # Import the migration module dynamically
        migration_module = __import__(
            f"src.db.migrations.{migration_name}", fromlist=[migration_name]
        )

        # Get database client
        db_client = client("verbs", conn_string)  # Replace with your actual database name

        # Run the migration
        if hasattr(migration_module, "main"):
            print(f"Running migration: {migration_name}")
            if asyncio.iscoroutinefunction(migration_module.main):
                asyncio.run(migration_module.main(db_client))
            else:
                migration_module.main(db_client)
            print(f"Migration {migration_name} completed successfully")
        else:
            print(f"Migration {migration_name} does not have a main function")

    except Exception as e:
        print(f"Error running migration {migration_name}: {e}")


def main():
    """Run all available migrations or a specific one."""
    import argparse

    parser = argparse.ArgumentParser(description="Run database migrations")
    parser.add_argument(
        "migration",
        nargs="?",
        help="Specific migration to run (e.g., 0001_fix_accents)",
    )
    
    parser.add_argument(
        "--connstr",
        default="mongodb://localhost:27017/",
        help="MongoDB connection string"
    )

    args = parser.parse_args()

    if args.migration:
        run_migration(args.migration, args.connstr)
    else:
        # Run all migrations
        migrations = ["0001_fix_accents", "0002_apply_translations"]

        for migration in migrations:
            run_migration(migration)


if __name__ == "__main__":
    main()
