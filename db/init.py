import os
from sqlalchemy import text
from db.session import engine
from db.repositories.logger import log
from db.models.logger import LogLevel


def run_migrations(dir_path):
    if not os.path.exists(dir_path):
        log(LogLevel.ERROR, "Migrations folder doesn't exist.")
        return 
    migrations = sorted([
        f for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f))
        and f.endswith(".sql")
    ])
    for i in migrations:
        try:
            with engine.begin() as connection:
                with open(os.path.join(dir_path, i), 'r', encoding="utf-8") as f:
                    migration_sql = f.read()
                    connection.execute(text(migration_sql))
                    log(LogLevel.INFO, f"Migration {i} applied successfully.")
        except Exception as e:
            log(LogLevel.ERROR, f"Error applying migration {i}: {e}")


def init_db():
    try:
        run_migrations("db/migrations")
    except Exception as e:
        log(LogLevel.ERROR, f"Error initializing the database: {e}")