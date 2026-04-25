import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post

# Set up a test database
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

class TestModels:
    def setup_method(self):
        # Clear the database before each test
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def test_create_user(self):
        user = User(email='test@example.com', password='hashed_pw')
        session.add(user)
        session.commit()
        assert user.id is not None

    def test_create_post(self):
        user = User(email='test@example.com', password='hashed_pw')
        session.add(user)
        session.commit()
        post = Post(user_id=user.id, content='Example content')
        session.add(post)
        session.commit()
        assert post.id is not None
        assert post.user == user