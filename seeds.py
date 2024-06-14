from models import db, User, Post, Tag
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    
    User.query.delete()
    
    users = [
        User(first_name='John', last_name='Doe'),
        User(first_name='Mark', last_name='Johns', img_url='https://scontent-mia3-2.xx.fbcdn.net/v/t39.30808-6/370283022_10218118569474535_3499045784827855420_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=5f2048&_nc_ohc=1wJ2Ajh8A3UQ7kNvgFcDs_D&_nc_ht=scontent-mia3-2.xx&oh=00_AYBOvOpWhBvCXYIyucOZEd-LlA3e1WevWteQxQNBNz241w&oe=667185E3')
    ]
    
    db.session.add_all(users)
    
    db.session.commit()
    
    tags = [
        Tag(name='test'),
        Tag(name='example')
    ]
    
    db.session.add_all(tags)
    
    db.session.commit()