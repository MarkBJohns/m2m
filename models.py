from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
default_img = 'https://imgs.search.brave.com/xRLAOStYtw4m5_8Pov_PBYMh7lmcrkLzavkwcT3lVHU/rs:fit:860:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzAwLzY0LzY3LzUy/LzM2MF9GXzY0Njc1/MjA5Xzd2ZTJYUUFO/dXp1SGpNWlhQM2FJ/WUlwc0RLRWJGNWRE/LmpwZw'

class User(db.Model):
    '''table for users'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    img_url = db.Column(db.String, default=default_img)
    
class Post(db.Model):
    '''table for posts'''
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', backref='posts')
    tags = relationship('Tag', secondary='post_tags', backref='posts')
    
class Tag(db.Model):
    '''table for tags'''
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    
class PostTag(db.Model):
    '''table for post/tag relationships'''
    
    __tablename__ = 'post_tags'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True,)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True,)