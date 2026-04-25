import unittest
from auth import app, users_db
import bcrypt
from jose import jwt

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users_db.clear()  # Clear user database before each test

    def test_signup_success(self):
        response = self.app.post('/signup', json={'email': 'test@example.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)

    def test_signup_existing_user(self):
        users_db['test@example.com'] = bcrypt.hashpw(b'testpass', bcrypt.gensalt())
        response = self.app.post('/signup', json={'email': 'test@example.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        password = 'testpass'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_db['test@example.com'] = hashed_password
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': password})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()