from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tmpm_shopify_backend.app.models import Base, Product, Order
from tmpm_shopify_backend.app.crud import create_product, create_order, get_order, get_orders, update_order, delete_order
import pytest

# Setup for the tests
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Order Tests

def test_create_order(db_session):
    product = create_product(db_session, {"title": "Order Product", "price": 10.0, "inventory_count": 100})
    order_data = {"product_id": product.id, "quantity": 1, "status": "pending", "amount": 10.0, "discount": 0.0}
    order = create_order(db_session, order_data)
    assert order.product_id == product.id

def test_get_order(db_session):
    product = create_product(db_session, {"title": "Order Product", "price": 10.0, "inventory_count": 100})
    order = create_order(db_session, {"product_id": product.id, "quantity": 2, "status": "completed", "amount": 20.0, "discount": 0.0})
    retrieved_order = get_order(db_session, order.id)
    assert retrieved_order.id == order.id

def test_get_orders(db_session):
    product = create_product(db_session, {"title": "Order Product", "price": 10.0, "inventory_count": 100})
    create_order(db_session, {"product_id": product.id, "quantity": 1, "status": "pending", "amount": 10.0, "discount": 0.0})
    create_order(db_session, {"product_id": product.id, "quantity": 2, "status": "completed", "amount": 20.0, "discount": 0.0})
    orders = get_orders(db_session)
    assert len(orders) == 2

def test_update_order(db_session):
    product = create_product(db_session, {"title": "Order Product", "price": 10.0, "inventory_count": 100})
    order = create_order(db_session, {"product_id": product.id, "quantity": 1, "status": "pending", "amount": 10.0, "discount": 0.0})
    update_order(db_session, order.id, {"status": "shipped"})
    updated_order = get_order(db_session, order.id)
    assert updated_order.status == "shipped"

def test_delete_order(db_session):
    product = create_product(db_session, {"title": "Order Product", "price": 10.0, "inventory_count": 100})
    order = create_order(db_session, {"product_id": product.id, "quantity": 1, "status": "pending", "amount": 10.0, "discount": 0.0})
    delete_order(db_session, order.id)
    assert get_order(db_session, order.id) is None
