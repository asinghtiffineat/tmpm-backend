from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(DECIMAL(10, 2))
    inventory_count = Column(Integer)

    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    status = Column(String)  # e.g., "pending", "completed", "shipped"
    order_date = Column(DateTime)
    amount = Column(DECIMAL(10, 2))  # Total amount of the order
    discount = Column(DECIMAL(10, 2))  # Discount amount, if any

    product = relationship("Product", back_populates="orders")
