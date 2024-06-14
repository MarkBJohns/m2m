from flask import Flask, redirect, url_for, render_template
from models import db, connect_db, default_img, User
from forms import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly2'
app.config['SECRET_KEY'] = 'shhhh'
app.config['DEBUG'] = True

connect_db(app)

with app.app_context():
    db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#       ROUTES FOR USERS

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/')
def home_page():
    '''Home page for the app'''
    return redirect(url_for('users_list'))

# ////////////////////////////////////////////////////////////////////////

@app.route('/users')
def users_list():
    '''Show a list of all of the users'''
    users = User.query.all()
    return render_template('users_list.html', users=users)

# ////////////////////////////////////////////////////////////////////////

@app.route('/users/new', methods=['GET', 'POST'])
def add_users():
    '''Handles form submission for a new user'''
    form = UserForm()
    
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        img_url = form.img_url.data or default_img
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            img_url=img_url
        )
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('users_list'))
    
    return render_template('add_users.html', form=form)

# ////////////////////////////////////////////////////////////////////////

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    '''Shows a specific user's profile'''
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

# ////////////////////////////////////////////////////////////////////////

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.img_url = form.img_url.data
        
        db.session.commit()
        return redirect(url_for('users_list'))
    
    return render_template('edit_user.html', form=form, user=user)

# ////////////////////////////////////////////////////////////////////////

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')





if __name__ == '__main__':
    app.run(debug=True)