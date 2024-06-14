from flask_sqlalchemy import SQLAlchemy

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
    
