import pytest
from flask import Flask
from views import yapp
from models import session, User, Post

# Create a test client
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(yapp)
    with app.test_client() as client:
        yield client

class TestViews:
    def setup_method(self):
        # Clear the database before each test
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

    def test_create_post(self, client):
        user = User(email='test@example.com', password='hashed_pw')
        session.add(user)
        session.commit()
        response = client.post('/posts', json={'user_id': user.id, 'content': 'Hello World'})
        assert response.status_code == 201
        assert response.get_json() == {'message': 'Post created'}

    def test_list_posts(self, client):
        user = User(email='test@example.com', password='hashed_pw')
        session.add(user)
        post = Post(user_id=user.id, content='Hello World')
        session.add(post)
        session.commit()
        response = client.get('/posts')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['content'] == 'Hello World'

    def test_delete_post(self, client):
        user = User(email='test@example.com', password='hashed_pw')
        session.add(user)
        post = Post(user_id=user.id, content='Hello World')
        session.add(post)
        session.commit()
        response = client.delete(f'/posts/{post.id}')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Post deleted'}