# auth.py

from flask import Flask, request, jsonify
import bcrypt
from jose import JWTError, jwt

app = Flask(__name__)

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'

# Mock database
users_db = {}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email in users_db:
        return jsonify({'message': 'User already exists'}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_db[email] = hashed_password
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = users_db.get(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user):
        token = jwt.encode({'email': email}, SECRET_KEY, algorithm=ALGORITHM)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    # Handle logout logic here (e.g., token blacklisting)
    return jsonify({'message': 'Logged out'}), 200

if __name__ == '__main__':
    app.run(debug=True)