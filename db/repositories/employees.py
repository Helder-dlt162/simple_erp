from db.repositories.logger import log
from db.models.logger import LogLevel
from db.models.users import Employees
from db.session import SessionLocal
import uuid


# Create
def create_employee(first_name, cpf):
    session = SessionLocal()
    employee_id = generate_employee_id(session)
    try:
        new_employee = Employees(
            employee_id=employee_id,
            first_name=first_name,
            cpf=cpf,
        )
        session.add(new_employee)
        session.commit()
        return employee_id
    except Exception as e:
        session.rollback()
        log(LogLevel.ERROR, f"Error while creating employee: {e}")
    finally:
        session.close()


def generate_employee_id(session):
    while True:
        employee_id = f"EMP-{uuid.uuid4().hex[:12].upper()}"
        exists = session.query(Employees).filter_by(
            employee_id=employee_id
        ).first()
        if not exists:
            return employee_id
