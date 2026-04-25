import unittest
from auth import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_signup_new_user(self):
        response = self.client.post('/signup', json={'email': 'newuser@test.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created', response.get_data(as_text=True))

    def test_signup_existing_user(self):
        self.client.post('/signup', json={'email': 'existinguser@test.com', 'password': 'password123'})
        response = self.client.post('/signup', json={'email': 'existinguser@test.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists', response.get_data(as_text=True))

    def test_login_valid_credentials(self):
        self.client.post('/signup', json={'email': 'user@test.com', 'password': 'password123'})
        response = self.client.post('/login', json={'email': 'user@test.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_login_invalid_credentials(self):
        response = self.client.post('/login', json={'email': 'user@test.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.get_data(as_text=True))

    def test_logout(self):
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged out', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()