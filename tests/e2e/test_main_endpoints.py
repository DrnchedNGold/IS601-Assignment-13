import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Home</title>" in response.text

def test_login_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_register_page():
    response = client.get("/register")
    assert response.status_code == 200
    assert "register" in response.text.lower()

def test_dashboard_page():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "dashboard" in response.text.lower()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_and_login_and_calculation_flow():
    # Register user
    reg_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    assert reg_resp.status_code == 201
    user_id = reg_resp.json()["id"]

    # Login user
    login_data = {
        "username": "testuser",
        "password": "TestPass123!"
    }
    login_resp = client.post("/auth/login", json=login_data)
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    access_token = tokens["access_token"]

    # Auth header
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create calculation
    calc_data = {
        "type": "addition",
        "inputs": [1, 2]
    }
    calc_resp = client.post("/calculations", json=calc_data, headers=headers)
    assert calc_resp.status_code == 201
    calc_id = calc_resp.json()["id"]

    # List calculations
    list_resp = client.get("/calculations", headers=headers)
    assert list_resp.status_code == 200
    assert any(c["id"] == calc_id for c in list_resp.json())

    # Get calculation
    get_resp = client.get(f"/calculations/{calc_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == calc_id

    # Update calculation
    update_data = {
        "inputs": [3, 4]
    }
    update_resp = client.put(f"/calculations/{calc_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["inputs"] == [3, 4]

    # Delete calculation
    del_resp = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert del_resp.status_code == 204

    # Confirm deletion
    get_resp2 = client.get(f"/calculations/{calc_id}", headers=headers)
    assert get_resp2.status_code == 404
