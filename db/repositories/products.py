from db.models.inventory import Products
from db.models.inventory import Suppliers
from db.session import SessionLocal
from utils.exception_repo import repo_exception

# Create
def create_product(data):
    session = SessionLocal()
    try:
        supplier_id = data.get("supplier_id")
        if supplier_id:
            supplier = session.query(Suppliers).filter_by(
                id=supplier_id
            ).first()
            if not supplier:
                return None
        new_product = Products(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            supplier_id=supplier_id
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while creating product",
            e,
            500
        )
    finally:
        session.close()

# Read
def get_products(limit=100):
    session = SessionLocal()
    try:
        products = session.query(Products).limit(limit).all()
        return [
            {
                "id": i.id,
                "name": i.name,
                "description": i.description,
                "price": i.price,
                "supplier_id": i.supplier_id
            }
            for i in products
        ]
    except Exception as e:
        repo_exception(
            "Error while getting products",
            e,
            500
        )
    finally:
        session.close()


def get_product_by_id(product_id):
    session = SessionLocal()
    try:
        product = session.query(Products).filter_by(
            id=product_id
        ).first()
        if not product:
            return None
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "supplier_id": product.supplier_id
        }
    except Exception as e:
        repo_exception(
            "Error while getting product",
            e,
            500
        )
    finally:
        session.close()

# Update
def update_product(product_id, data):
    session = SessionLocal()
    try:
        product = session.query(Products).filter_by(
            id=product_id
        ).first()
        if not product:
            return None
        if "supplier_id" in data:
            supplier = session.query(Suppliers).filter_by(
                id=data["supplier_id"]
            ).first()
            if not supplier:
                return None
        allowed_fields = {
            "name",
            "description",
            "price",
            "supplier_id"
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(product, key, value)
        session.commit()
        session.refresh(product)
        return {
            "id": product.id,
            "name": product.name
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while updating product",
            e,
            500
        )
    finally:
        session.close()

# Delete
def delete_product(product_id):
    session = SessionLocal()
    try:
        product = session.query(Products).filter_by(
            id=product_id
        ).first()
        if not product:
            return None
        session.delete(product)
        session.commit()
        return {
            "message": "Product deleted successfully"
        }
    except Exception as e:
        session.rollback()
        repo_exception(
            "Error while deleting product",
            e,
            500
        )
    finally:
        session.close()
