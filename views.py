# views.py

from flask import Blueprint, request, jsonify
from models import session, User, Post

yapp = Blueprint('yapp', __name__)

@yapp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        post = Post(user_id=user_id, content=content)
        session.add(post)
        session.commit()
        return jsonify({'message': 'Post created'}), 201
    return jsonify({'message': 'User not found'}), 404

@yapp.route('/posts', methods=['GET'])
def list_posts():
    posts = session.query(Post).all()
    return jsonify([{'id': post.id, 'content': post.content, 'user_id': post.user_id} for post in posts]), 200

@yapp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        return jsonify({'message': 'Post deleted'}), 200
    return jsonify({'message': 'Post not found'}), 404