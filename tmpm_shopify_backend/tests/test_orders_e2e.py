from fastapi.testclient import TestClient
from tmpm_shopify_backend.app.main import app

client = TestClient(app)

# Test JWT token for an authenticated user
test_token = "your_test_jwt_token"

def test_create_order():
    response = client.post(
        "/orders/",
        json={"product_id": 1, "quantity": 2, "status": "pending", "amount": 20.0, "discount": 0.0},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 2

def test_read_order():
    # Assuming an order with id 1 exists
    response = client.get("/orders/1", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_read_orders():
    response = client.get("/orders/", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_order():
    # Assuming an order with id 1 exists
    response = client.put(
        "/orders/1",
        json={"product_id": 1, "quantity": 3, "status": "shipped", "amount": 30.0, "discount": 0.0},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 3

def test_delete_order():
    # Create a new order to delete
    create_response = client.post(
        "/orders/",
        json={"product_id": 1, "quantity": 2, "status": "pending", "amount": 20.0, "discount": 0.0},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    order_id = create_response.json()["id"]
    delete_response = client.delete(f"/orders/{order_id}", headers={"Authorization": f"Bearer {test_token}"})
    assert delete_response.status_code == 200
