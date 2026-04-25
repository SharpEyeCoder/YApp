import pytest
from auth import app
from flask import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test signup functionality
def test_signup(client):
    # Test a successful signup
    response = client.post('/signup', json={'email': 'test@example.com', 'password': 'testpassword'})
    assert response.status_code == 201
    assert response.json['message'] == 'User created'

    # Test signing up an existing user
    response = client.post('/signup', json={'email': 'test@example.com', 'password': 'testpassword'})
    assert response.status_code == 400
    assert response.json['message'] == 'User already exists'

# Test login functionality
def test_login(client):
    # Sign up a user first
    client.post('/signup', json={'email': 'test2@example.com', 'password': 'testpassword'})
    
    # Test successful login
    response = client.post('/login', json={'email': 'test2@example.com', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'token' in response.json

    # Test login failure
    response = client.post('/login', json={'email': 'test2@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid credentials'

# Test logout functionality
def test_logout(client):
    # Test a successful logout
    response = client.post('/logout')
    assert response.status_code == 200
    assert response.json['message'] == 'Logged out'
