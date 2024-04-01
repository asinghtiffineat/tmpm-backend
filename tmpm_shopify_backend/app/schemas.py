from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Product Schemas

class ProductBase(BaseModel):
    title: str
    price: float
    inventory_count: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Order Schemas

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    status: str
    amount: float
    discount: float
    order_date: Optional[datetime] = None

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
