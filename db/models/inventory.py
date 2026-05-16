from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float
)
from sqlalchemy.sql import func
from db.base import base


class Suppliers(base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    contact_info = Column(String)
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name})>"
    

class Products(base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Product(id={self.id}, (name={self.name}), price={self.price})>"
    

class Inventory(base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    modified_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Inventory(product_id={self.product_id}, quantity={self.quantity})>"
