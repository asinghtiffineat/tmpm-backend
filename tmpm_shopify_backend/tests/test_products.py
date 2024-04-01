from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tmpm_shopify_backend.app.models import Base, Product
from tmpm_shopify_backend.app.crud import create_product, get_product, get_products, update_product, delete_product
import pytest

# Setup for the tests - create an in-memory SQLite database for testing
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

# Product Tests

def test_create_product(db_session):
    product_data = {"title": "Test Product", "price": 10.0, "inventory_count": 100}
    product = create_product(db_session, product_data)
    assert product.title == "Test Product"

def test_get_product(db_session):
    product = create_product(db_session, {"title": "Test Product", "price": 20.0, "inventory_count": 50})
    retrieved_product = get_product(db_session, product.id)
    assert retrieved_product.id == product.id

def test_get_products(db_session):
    create_product(db_session, {"title": "Product 1", "price": 10.0, "inventory_count": 100})
    create_product(db_session, {"title": "Product 2", "price": 20.0, "inventory_count": 50})
    products = get_products(db_session)
    assert len(products) == 2

def test_update_product(db_session):
    product = create_product(db_session, {"title": "Old Title", "price": 15.0, "inventory_count": 70})
    update_product(db_session, product.id, {"title": "New Title"})
    updated_product = get_product(db_session, product.id)
    assert updated_product.title == "New Title"

def test_delete_product(db_session):
    product = create_product(db_session, {"title": "Delete Me", "price": 15.0, "inventory_count": 10})
    delete_product(db_session, product.id)
    assert get_product(db_session, product.id) is None
