import pytest
from flask import json
from models import session, User
from views import yapp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(yapp)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    session.rollback()

@pytest.fixture(autouse=True)
def setup_db():
    # Ensure a clean start
    User.__table__.drop(session.bind, checkfirst=True)
    User.__table__.create(session.bind)

# Test creating a post
def test_create_post(client):
    # Setup user
    user = User(email='post@example.com', password='hashedpassword')
    session.add(user)
    session.commit()

    # Test creating a post
    response = client.post('/posts', json={'user_id': user.id, 'content': 'This is a new post'})
    assert response.status_code == 201
    assert response.json['message'] == 'Post created'

    # Test creating a post for non-existent user
    response = client.post('/posts', json={'user_id': 9999, 'content': 'Invalid user post'})
    assert response.status_code == 404
    assert response.json['message'] == 'User not found'

# Test listing posts
def test_list_posts(client):
    user = User(email='poster@example.com', password='hashedpassword')
    session.add(user)
    session.commit()

    client.post('/posts', json={'user_id': user.id, 'content': 'Post for listing'})

    response = client.get('/posts')
    assert response.status_code == 200
    assert len(response.json) == 1

# Test deleting a post
def test_delete_post(client):
    user = User(email='delete@example.com', password='hashedpassword')
    session.add(user)
    session.commit()

    post_response = client.post('/posts', json={'user_id': user.id, 'content': 'Post to delete'})
    post_id = post_response.json['id']

    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Post deleted'

    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == 404
    assert response.json['message'] == 'Post not found'