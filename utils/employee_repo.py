from db.models.users import Employees
import uuid


def generate_employee_id(session):
    while True:
        employee_id = f"EMP-{uuid.uuid4().hex[:12].upper()}"
        exists = session.query(Employees).filter_by(
            employee_id=employee_id
        ).first()
        if not exists:
            return employee_id
