from utils.exception_repo import repo_exception
from db.repositories.logger import log
from db.models.logger import LogLevel
from db.models.users import UserTypes
from db.session import SessionLocal

# Create
def add_user_type(data):
    session = SessionLocal()
    try:
        new_type = UserTypes(
            name=data["name"]
        )
        session.add(new_type)
        session.commit()
        session.refresh(new_type)
        return {
            "type_id": new_type.type_id,
            "name": new_type.name,
        }
    except Exception as e:
        session.rollback()
        repo_exception("Error while adding user type", e, 500)
    finally:
        session.close()

# Read
def get_user_types(limit=100):
    session = SessionLocal()
    try:
        user_types = session.query(UserTypes).limit(limit).all()
        return [
            {
                "type_id": i.type_id,
                "name": i.name
            }
            for i in user_types
        ]
    except Exception as e:
        repo_exception("Error while getting user types", e, 500)
    finally:
        session.close()


def get_user_type_by_id(id):
    session = SessionLocal()
    try:
        user_type = session.query(UserTypes).filter_by(type_id=id).first()
        if not user_type:
            return "User type not found"
        return {
            "type_id": user_type.type_id,
            "name": user_type.name
        }
    except Exception as e:
        repo_exception("Error while getting user type", e, 500)
    finally:
        session.close()

# Update
def update_user_type(id, data):
    session = SessionLocal()
    try:
        user_type = session.query(UserTypes).filter_by(type_id=id).first()
        if not user_type:
            return "User type not found"
        allowed_fields = {
            "type_id",
            "name"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(user_type, key, value)
        session.commit()
        session.refresh(user_type)
        return {
            "type_id": user_type.type_id,
            "name": user_type.name
        }
    except Exception as e:
        session.rollback()
        er = f"Error while updating user type: {e}"
        log(LogLevel.ERROR, er)
        return er
    finally:
        session.close()

# Delete
def delete_user_type(id):
    session = SessionLocal()
    try:
        user_type = session.query(UserTypes).filter_by(type_id=id).first()
        if not user_type:
            return "User type not found"
        session.delete(user_type)
        session.commit()
        return "User type deleted successfully"
    except Exception as e:
        session.rollback()
        er = f"Error while deleting user type: {e}"
        log(LogLevel.ERROR, er)
        return er
    finally:
        session.close()
