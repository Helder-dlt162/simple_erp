from utils.employee_repo import generate_employee_id
from utils.exception_repo import repo_exception
from db.models.users import Employees
from db.session import SessionLocal

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
        repo_exception("Error while creating employee", e, 500)
    finally:
        session.close()
