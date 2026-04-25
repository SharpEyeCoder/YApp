# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=False)

    user = relationship('User', back_populates='posts')

User.posts = relationship('Post', order_by=Post.id, back_populates='user')

# Initialize the database
engine = create_engine('sqlite:///yapp.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()