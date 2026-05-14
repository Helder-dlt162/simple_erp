from db.models.users import Users
from db.session import SessionLocal
from werkzeug.security import generate_password_hash
from utils.exception_repo import repo_exception

# Create
def add_user(data):
    session = SessionLocal()
    try:
        new_user = Users(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            user_type=data.get('user_type', '1'),
        )
        session.add(new_user)
        session.commit()
        return {
            "id": new_user.id,
            "username": new_user.username
        }
    except Exception as e:
        session.rollback()
        repo_exception("Error while adding user", e, 500)
    finally:
        session.close()
        
# Read
def get_users(limit=100):
    session = SessionLocal()
    try:
        users = session.query(Users).limit(limit).all()
        if users:
            return users
        else:
            return "No users found"
    except Exception as e:
        session.rollback()
        repo_exception("Error while getting users", e, 500)
    finally:
        session.close()


def get_user_by_id(id):
    session = SessionLocal()
    try:
        user = session.query(Users).filter_by(id=id).first()
        if user:
            return user
        else:
            return "No users found with provided ID"
    except Exception as e:
        session.rollback()
        repo_exception("Error while getting user", e, 500)
    finally:
        session.close()

# Update
def update_user(id, data):
    session = SessionLocal()
    try:
        user = session.query(Users).filter_by(id=id).first()
        if not user:
            return "User not found"
        allowed_fields = {
            "username",
            "email",
            "user_type"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(user, key, value)
        if "password" in data:
            user.password_hash = generate_password_hash(
                data["password"]
            )
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        repo_exception("Error while updating user", e, 500)
    finally:
        session.close()

# Delete
def delete_user(id):
    session = SessionLocal()
    try:
        user = session.query(Users).filter_by(id=id).first()
        if not user:
            return "User not found"
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
        repo_exception("Error while deleting user", e, 500)
    finally:
        session.close()
