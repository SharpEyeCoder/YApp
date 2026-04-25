import unittest
from flask import Flask
from views import yapp
from models import session, User, Post

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Flask(__name__).test_client()
        self.client.application.register_blueprint(yapp)

    def test_create_post_with_valid_user(self):
        user = User(email='viewuser@test.com', password='hashed')
        session.add(user)
        session.commit()
        response = self.client.post('/posts', json={'user_id': user.id, 'content': 'A new post'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Post created', response.get_data(as_text=True))

    def test_create_post_with_non_existing_user(self):
        response = self.client.post('/posts', json={'user_id': 9999, 'content': 'Should not work'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_data(as_text=True))

    def test_list_posts(self):
        user = User(email='listuser@test.com', password='hashed')
        session.add(user)
        session.commit()
        post = Post(user_id=user.id, content='List this post')
        session.add(post)
        session.commit()
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn('List this post', response.get_data(as_text=True))

    def test_delete_existing_post(self):
        user = User(email='deleteuser@test.com', password='hashed')
        session.add(user)
        session.commit()
        post = Post(user_id=user.id, content='Delete this post')
        session.add(post)
        session.commit()
        response = self.client.delete(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post deleted', response.get_data(as_text=True))

    def test_delete_non_existing_post(self):
        response = self.client.delete('/posts/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Post not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()