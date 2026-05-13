from db.models.logger import Logger
from db.session import SessionLocal

def log(level, message):
    session = SessionLocal()
    try:
        new_log = Logger(
            level = level,
            message = message
        )
        session.add(new_log)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error while saving log: {e}")
    finally:
        session.close()