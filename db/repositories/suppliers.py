from db.models.inventory import Suppliers
from db.session import SessionLocal
from utils.exception_repo import repo_exception

# Create
def create_supplier(data):
    session = SessionLocal()
    try:
        new_supplier = Suppliers(
            name=data["name"],
            contact_info=data.get("contact_info")
        )
        session.add(new_supplier)
        session.commit()
        session.refresh(new_supplier)
        return {
            "id": new_supplier.id,
            "name": new_supplier.name
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while creating supplier",
            e,
            500
        )
    finally:
        session.close()

# Read
def get_suppliers(limit=100):
    session = SessionLocal()
    try:
        suppliers = session.query(Suppliers).limit(limit).all()
        return [
            {
                "id": i.id,
                "name": i.name,
                "contact_info": i.contact_info
            }
            for i in suppliers
        ]
    except Exception as e:
        repo_exception(
            "Error while getting suppliers",
            e,
            500
        )
    finally:
        session.close()


def get_supplier_by_id(supplier_id):
    session = SessionLocal()
    try:
        supplier = session.query(Suppliers).filter_by(
            id=supplier_id
        ).first()
        if not supplier:
            return None
        return {
            "id": supplier.id,
            "name": supplier.name,
            "contact_info": supplier.contact_info
        }
    except Exception as e:
        repo_exception(
            "Error while getting supplier",
            e,
            500
        )
    finally:
        session.close()

# Update
def update_supplier(supplier_id, data):
    session = SessionLocal()
    try:
        supplier = session.query(Suppliers).filter_by(
            id=supplier_id
        ).first()
        if not supplier:
            return None
        allowed_fields = {
            "name",
            "contact_info"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(supplier, key, value)
        session.commit()
        session.refresh(supplier)
        return {
            "id": supplier.id,
            "name": supplier.name
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while updating supplier",
            e,
            500
        )
    finally:
        session.close()

# Delete
def delete_supplier(supplier_id):
    session = SessionLocal()
    try:
        supplier = session.query(Suppliers).filter_by(
            id=supplier_id
        ).first()
        if not supplier:
            return None
        session.delete(supplier)
        session.commit()
        return {
            "message": "Supplier deleted successfully"
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while deleting supplier",
            e,
            500
        )
    finally:
        session.close()
