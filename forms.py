from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, URL

class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    img_url = StringField('Profile Picture', validators=[Optional(), URL()])
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
    
class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])