import unittest
from models import Session, User, Post

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        Base.metadata.create_all(bind=self.session.bind)

    def tearDown(self):
        self.session.query(Post).delete()
        self.session.query(User).delete()
        self.session.commit()

    def test_user_creation(self):
        user = User(email='testuser@test.com', password='hashedpassword')
        self.session.add(user)
        self.session.commit()
        retrieved_user = self.session.query(User).filter_by(email='testuser@test.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'testuser@test.com')

    def test_post_creation(self):
        user = User(email='postuser@test.com', password='hashedpassword')
        self.session.add(user)
        self.session.commit()
        post = Post(user_id=user.id, content='This is a test post')
        self.session.add(post)
        self.session.commit()
        retrieved_post = self.session.query(Post).filter_by(content='This is a test post').first()
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post.content, 'This is a test post')
        self.assertEqual(retrieved_post.user_id, user.id)

    def test_query_posts_for_user(self):
        user = User(email='queryuser@test.com', password='hashedpassword')
        self.session.add(user)
        self.session.commit()
        post1 = Post(user_id=user.id, content='First post')
        post2 = Post(user_id=user.id, content='Second post')
        self.session.add(post1)
        self.session.add(post2)
        self.session.commit()
        posts = self.session.query(Post).filter_by(user_id=user.id).all()
        self.assertEqual(len(posts), 2)

if __name__ == '__main__':
    unittest.main()