import unittest
from models import session, User, Post

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

    def tearDown(self):
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

    def test_create_user(self):
        user = User(email='test@example.com', password='hashedpassword')
        session.add(user)
        session.commit()
        retrieved_user = session.query(User).filter_by(email='test@example.com').first()
        self.assertIsNotNone(retrieved_user)

    def test_create_post(self):
        user = User(email='test@example.com', password='hashedpassword')
        session.add(user)
        session.commit()
        post = Post(user_id=user.id, content='This is a test post')
        session.add(post)
        session.commit()
        retrieved_post = session.query(Post).filter_by(content='This is a test post').first()
        self.assertIsNotNone(retrieved_post)

if __name__ == '__main__':
    unittest.main()