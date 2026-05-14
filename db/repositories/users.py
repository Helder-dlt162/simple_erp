from db.repositories.logger import log
from db.models.logger import LogLevel
from db.models.users import Users
from db.session import SessionLocal
from werkzeug.security import generate_password_hash


# Create
def add_user(data):
    session = SessionLocal()
    try:
        new_user = Users(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            user_type=data.get('user_type', '0001'),
        )
        session.add(new_user)
        session.commit()
        return {
            "id": new_user.id,
            "username": new_user.username
        }
    except Exception as e:
        session.rollback()
        er = f"Error while adding user: {e}"
        log(LogLevel.ERROR, er)
        return er
    finally:
        session.close()
        

# Read
def get_users(limit=100):
    session = SessionLocal()
    try:
        users = session.query(Users).limit(limit).all()
        return users
    except Exception as e:
        er = f"Error while getting users: {e}"
        log(LogLevel.ERROR, er)
        return er
    finally:
        session.close()


def get_user_by_id(id):
    session = SessionLocal()
    try:
        user = session.query(Users).filter_by(id=id).first()
        return user
    except Exception as e:
        er = f"Error while getting user: {e}"
        log(LogLevel.ERROR, er)
        return er
    finally:
        session.close()

# Update
# Delete
