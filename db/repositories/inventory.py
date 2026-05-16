from db.models.inventory import Inventory
from db.models.inventory import Products
from db.session import SessionLocal
from utils.exception_repo import repo_exception

# Create
def create_inventory(data):
    session = SessionLocal()
    try:
        product = session.query(Products).filter_by(
            id=data["product_id"]
        ).first()
        if not product:
            return None
        new_inventory = Inventory(
            product_id=data["product_id"],
            quantity=data["quantity"]
        )
        session.add(new_inventory)
        session.commit()
        session.refresh(new_inventory)
        return {
            "id": new_inventory.id,
            "product_id": new_inventory.product_id,
            "quantity": new_inventory.quantity
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while creating inventory",
            e,
            500
        )
    finally:
        session.close()

# Read
def get_inventory(limit=100):
    session = SessionLocal()
    try:
        inventory = session.query(Inventory).limit(limit).all()
        return [
            {
                "id": i.id,
                "product_id": i.product_id,
                "quantity": i.quantity
            }
            for i in inventory
        ]
    except Exception as e:
        repo_exception(
            "Error while getting inventory",
            e,
            500
        )
    finally:
        session.close()


def get_inventory_by_id(inventory_id):
    session = SessionLocal()
    try:
        inventory = session.query(Inventory).filter_by(
            id=inventory_id
        ).first()
        if not inventory:
            return None
        return {
            "id": inventory.id,
            "product_id": inventory.product_id,
            "quantity": inventory.quantity
        }
    except Exception as e:
        repo_exception(
            "Error while getting inventory item",
            e,
            500
        )
    finally:
        session.close()

# Update
def update_inventory(inventory_id, data):
    session = SessionLocal()
    try:
        inventory = session.query(Inventory).filter_by(
            id=inventory_id
        ).first()
        if not inventory:
            return None
        if "product_id" in data:
            product = session.query(Products).filter_by(
                id=data["product_id"]
            ).first()
            if not product:
                return None
        allowed_fields = {
            "product_id",
            "quantity"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(inventory, key, value)
        session.commit()
        session.refresh(inventory)
        return {
            "id": inventory.id,
            "product_id": inventory.product_id,
            "quantity": inventory.quantity
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while updating inventory",
            e,
            500
        )
    finally:
        session.close()

# Delete
def delete_inventory(inventory_id):
    session = SessionLocal()
    try:
        inventory = session.query(Inventory).filter_by(
            id=inventory_id
        ).first()
        if not inventory:
            return None
        session.delete(inventory)
        session.commit()
        return {
            "message": "Inventory item deleted successfully"
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while deleting inventory",
            e,
            500
        )
    finally:
        session.close()
