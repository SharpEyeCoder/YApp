import unittest
from flask import Flask
from views import yapp
from models import session, User, Post

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(yapp)
        self.client = self.app.test_client()

        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

        # Add a test user
        self.user = User(email='user@example.com', password='hashedpassword')
        session.add(self.user)
        session.commit()

    def tearDown(self):
        session.query(Post).delete()
        session.query(User).delete()
        session.commit()

    def test_create_post_success(self):
        response = self.client.post('/posts', json={'user_id': self.user.id, 'content': 'New Post Content'})
        self.assertEqual(response.status_code, 201)

    def test_create_post_user_not_found(self):
        response = self.client.post('/posts', json={'user_id': 999, 'content': 'New Post Content'})
        self.assertEqual(response.status_code, 404)

    def test_list_posts(self):
        post = Post(user_id=self.user.id, content='Another Post')
        session.add(post)
        session.commit()

        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)

    def test_delete_post_success(self):
        post = Post(user_id=self.user.id, content='Post to delete')
        session.add(post)
        session.commit()

        response = self.client.delete(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_post_not_found(self):
        response = self.client.delete('/posts/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()