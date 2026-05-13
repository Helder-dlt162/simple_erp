import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL
from db.models import Base

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migrations():
    migration_file = "migration.sql"
    if os.path.exists(migration_file):
        try:
            with engine.connect() as connection:
                with open(migration_file, 'r') as f:
                    migration_sql = f.read()
                    connection.execute(migration_sql)
                    print("Migrations applied successfully.")
        except Exception as e:
            print(f"Error applying migrations: {e}")


def init_db():
    try:
        run_migrations()
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing the database: {e}")