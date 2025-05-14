import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'api')))

import pytest
from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient
from jose import jwt

from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_admin,
    SECRET_KEY,
    ALGORITHM
)


def test_verify_password_and_hash():
    pwd = "admin123"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_access_token_and_decode():
    data = {"sub": "admin"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "admin"

@pytest.fixture
def temp_app():
    app = FastAPI()

    @app.get("/me")
    def read_current_user(username: str = Depends(get_current_admin)):
        return {"username": username}

    return TestClient(app)

def test_get_current_admin_success(temp_app):
    token = create_access_token({"sub": "admin"})
    response = temp_app.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "admin"

def test_get_current_admin_missing_sub(temp_app):
    token = create_access_token({})
    response = temp_app.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_get_current_admin_invalid_token(temp_app):
    response = temp_app.get("/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert response.status_code == 401
