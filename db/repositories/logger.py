from db.models.logger import Logger, LogLevel
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


def get_logs(limit=100):
    session = SessionLocal()
    try:
        logs = session.query(Logger).limit(limit).all()
        return logs
    except Exception as e:
        log(LogLevel.ERROR, f"Error while getting logs: {e}")
    finally:
        session.close()


def get_log_by_id(id):
    session = SessionLocal()
    try:
        logs = session.query(Logger).filter_by(id=id).first()
        return logs
    except Exception as e:
        log(LogLevel.ERROR, f"Error while getting log: {e}")
    finally:
        session.close()


def get_log_by_level(level):
    session = SessionLocal()
    try:
        logs = session.query(Logger).filter_by(level=level).all()
        return logs
    except Exception as e:
        log(LogLevel.ERROR, f"Error while getting logs: {e}")
    finally:
        session.close()
