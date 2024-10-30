from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_and_get_user():
    response = client.post("/token",data={"username" : "john","password":"secret"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization":f"Bearer {token}"}
    response = client.get("/user/me",headers=headers)
    assert response.status_code == 200
    assert response.json()["username"]=="john"

def test_register():
    respone = client.post("/auth/register",json={"username":"testuser", "email": "testuser@example.com", "password": "testpass"})
    assert respone.status_code == 200
    assert respone.json() == {"message":"user created successfuly"}

