from utils.employee_repo import generate_employee_id
from utils.exception_repo import repo_exception
from db.models.users import Employees
from db.session import SessionLocal

# Create
def create_employee(data):
    session = SessionLocal()
    employee_id = generate_employee_id(session)
    try:
        new_employee = Employees(
            employee_id=employee_id,
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            cpf=data.get("cpf"),
            birth_date=data.get("birth_date"),
            department=data.get("department")
        )
        session.add(new_employee)
        session.commit()
        session.refresh(new_employee)
        return {
            "id": new_employee.id,
            "employee_id": new_employee.employee_id
        }
    except Exception as e:
        session.rollback()
        repo_exception("Error while creating employee", e, 500)
    finally:
        session.close()

# Read
def get_employees(limit=100):
    session = SessionLocal()
    try:
        employees = session.query(Employees).limit(limit).all()
        return [
            {
                "id": i.id,
                "employee_id": i.employee_id,
                "first_name": i.first_name,
                "last_name": i.last_name,
                "cpf": i.cpf,
                "department": i.department
            }
            for i in employees
        ]
    except Exception as e:
        repo_exception("Error while getting employees", e, 500)
    finally:
        session.close()


def get_employee_by_id(employee_id):
    session = SessionLocal()
    try:
        employee = session.query(Employees).filter_by(
            employee_id=employee_id
        ).first()
        if not employee:
            return None
        return {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "cpf": employee.cpf,
            "birth_date": employee.birth_date,
            "department": employee.department
        }
    except Exception as e:
        repo_exception("Error while getting employee", e, 500)
    finally:
        session.close()

# Update
def update_employee(employee_id, data):
    session = SessionLocal()
    try:
        employee = session.query(Employees).filter_by(
            employee_id=employee_id
        ).first()
        if not employee:
            return None
        allowed_fields = {
            "first_name",
            "last_name",
            "cpf",
            "birth_date",
            "department"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(employee, key, value)
        session.commit()
        session.refresh(employee)
        return {
            "id": employee.id,
            "employee_id": employee.employee_id
        }
    except Exception as e:
        session.rollback()
        repo_exception("Error while updating employee", e, 500)
    finally:
        session.close()

# Delete
def delete_employee(employee_id):
    session = SessionLocal()
    try:
        employee = session.query(Employees).filter_by(
            employee_id=employee_id
        ).first()
        if not employee:
            return None
        session.delete(employee)
        session.commit()
        return {
            "message": "Employee deleted successfully"
        }
    except Exception as e:
        session.rollback()
        repo_exception("Error while deleting employee", e, 500)
    finally:
        session.close()
