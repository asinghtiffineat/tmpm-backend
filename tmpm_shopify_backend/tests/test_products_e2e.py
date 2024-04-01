from fastapi.testclient import TestClient
from tmpm_shopify_backend.app.main import app

client = TestClient(app)

# Test JWT token for an authenticated user
test_token = "your_test_jwt_token"

def test_create_product():
    response = client.post(
        "/products/",
        json={"title": "Test Product", "price": 10.0, "inventory_count": 100},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Product"

def test_read_product():
    # Assuming a product with id 1 exists
    response = client.get("/products/1", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_read_products():
    response = client.get("/products/", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product():
    # Assuming a product with id 1 exists
    response = client.put(
        "/products/1",
        json={"title": "Updated Product", "price": 12.0, "inventory_count": 150},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Product"

def test_delete_product():
    # Create a new product to delete
    create_response = client.post(
        "/products/",
        json={"title": "Product to Delete", "price": 10.0, "inventory_count": 100},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    product_id = create_response.json()["id"]
    delete_response = client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {test_token}"})
    assert delete_response.status_code == 200
