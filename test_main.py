from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_and_get_user():
    response = client.post("/token", data={"username": "john", "password": "secret"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "john"


def test_register():
    respone = client.post("/auth/register",
                          json={"username": "testuser", "email": "testuser@example.com", "password": "testpass"})
    assert respone.status_code == 200
    assert respone.json() == {"message": "user created successfuly"}


def test_login_and_protected_route():
    response = client.post("/auth/token", data={"username": "john", "password": "secret"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert isinstance(token, str)
    assert len(token) > 0  # Check if token has some length

    # Step 3: Access protected route with token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/me",headers = headers)
    assert response.status_code == 200
    assert response.json()=={"username":"john"}

    # Step 4: Change password
    new_password = "newtestpass"
    response = client.post("/auth/user/change_password", json={"new_password": new_password}, headers=headers)
    assert response.status_code == 200
    assert response.json()=={"message":"password updated succesfuly"}

    # Step 5: Log in with new password
    response = client.post("/auth/token",data={"username":"john","password":new_password})
    assert response.status_code == 200
    assert "access_token" in response.json()



