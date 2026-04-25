import pytest
from flask import Flask
from auth import app as auth_app, users_db
from views import yapp as views_app
from models import session, User, Post
from sqlalchemy import text
import json
import bcrypt

@pytest.fixture
def auth_client():
    with auth_app.test_client() as client:
        yield client

@pytest.fixture
def views_client():
    app = Flask(__name__)
    app.register_blueprint(views_app)
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def setup_module():
    # Ensure tables are cleared before testing
    session.execute(text('DELETE FROM posts'))
    session.execute(text('DELETE FROM users'))
    session.commit()

class TestAdditionalAuth:
    def setup_method(self):
        users_db.clear()

    def test_invalid_signup_data(self, auth_client):
        response = auth_client.post('/signup', data=json.dumps({'email': '', 'password': ''}), content_type='application/json')
        assert response.status_code == 400

    def test_blank_password_login(self, auth_client):
        users_db['test@example.com'] = bcrypt.hashpw('12345'.encode('utf-8'), bcrypt.gensalt())
        response = auth_client.post('/login', data=json.dumps({'email': 'test@example.com', 'password': ''}), content_type='application/json')
        assert response.status_code == 401

class TestAdditionalViews:
    def setup_method(self, setup_module):
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

    def test_create_post_with_invalid_user(self, views_client):
        response = views_client.post('/posts', json={'user_id': 999, 'content': 'Hello World'})
        assert response.status_code == 404
        assert response.get_json() == {'message': 'User not found'}

    def test_delete_nonexistent_post(self, views_client):
        response = views_client.delete('/posts/500')
        assert response.status_code == 404
        assert response.get_json() == {'message': 'Post not found'}

    def test_get_posts_empty(self, views_client):
        response = views_client.get('/posts')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 0