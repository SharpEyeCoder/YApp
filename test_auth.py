import pytest
from flask import Flask
from auth import app, users_db
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Utility function for clearing the database state
def clear_users_db():
    users_db.clear()

class TestAuth:
    def setup_method(self):
        clear_users_db()

    def test_signup(self, client):
        response = client.post('/signup', data=json.dumps({'email': 'test@example.com', 'password': 'password'}), content_type='application/json')
        assert response.status_code == 201
        assert response.get_json() == {'message': 'User created'}

    def test_signup_existing_user(self, client):
        users_db['test@example.com'] = 'hashed_pw'
        response = client.post('/signup', data=json.dumps({'email': 'test@example.com', 'password': 'password'}), content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == {'message': 'User already exists'}

    def test_login_success(self, client):
        password = 'password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_db['test@example.com'] = hashed_password
        response = client.post('/login', data=json.dumps({'email': 'test@example.com', 'password': password}), content_type='application/json')
        assert response.status_code == 200
        assert 'token' in response.get_json()

    def test_login_failure(self, client):
        response = client.post('/login', data=json.dumps({'email': 'test@example.com', 'password': 'wrong_password'}), content_type='application/json')
        assert response.status_code == 401
        assert response.get_json() == {'message': 'Invalid credentials'}