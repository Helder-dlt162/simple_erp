from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from db.base import base


class Users(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_type = Column(Integer, ForeignKey("user_types.type_id"), nullable=False)
    employee_id = Column(String, ForeignKey("employees.employee_id"), unique=True)
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, user_type={self.user_type}, employee_id={self.employee_id})>"
    

class Employees(base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    cpf = Column(String, unique=True)
    birth_date = Column(DateTime)
    department = Column(String)
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Employee(employee_id={self.employee_id})>"
    

class UserTypes(base):
    __tablename__ = 'user_types'

    type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<UserTypes(type_id={self.type_id})>"
