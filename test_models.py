import pytest
from sqlalchemy.exc import IntegrityError
from models import User, Post, session

@pytest.fixture(autouse=True)
def setup_db():
    # Ensure a clean start
    User.__table__.drop(session.bind, checkfirst=True)
    Post.__table__.drop(session.bind, checkfirst=True)
    User.__table__.create(session.bind)
    Post.__table__.create(session.bind)
    yield
    session.rollback()

# Test creating a User
def test_create_user():
    user = User(email='test@example.com', password='hashedpassword')
    session.add(user)
    session.commit()

    fetched_user = session.query(User).filter_by(email='test@example.com').first()
    assert fetched_user is not None
    assert fetched_user.email == 'test@example.com'

# Test creating a User with duplicate email
def test_create_user_duplicate_email():
    user1 = User(email='duplicate@example.com', password='hashedpassword')
    user2 = User(email='duplicate@example.com', password='hashedpassword')
    session.add(user1)
    session.commit()
    
    with pytest.raises(IntegrityError):
        session.add(user2)
        session.commit()

# Test creating a Post
def test_create_post():
    user = User(email='postuser@example.com', password='hashedpassword')
    session.add(user)
    session.commit()

    post = Post(user_id=user.id, content='This is a test post')
    session.add(post)
    session.commit()

    fetched_post = session.query(Post).filter_by(user_id=user.id).first()
    assert fetched_post is not None
    assert fetched_post.content == 'This is a test post'
    assert fetched_post.user.email == 'postuser@example.com'