from flask import Flask, redirect, url_for, render_template
from models import db, connect_db, default_img, User, Post, Tag, PostTag
from forms import UserForm, PostForm, TagForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly2'
app.config['SECRET_KEY'] = 'shhhh'

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
    users = User.query.all()
    tags = Tag.query.all()
    return render_template('home.html', users=users, tags=tags)

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
    '''Deletes a user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#       ROUTES FOR POST

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/users/<int:user_id>/post', methods=['GET', 'POST'])
def add_post(user_id):
    '''Handles form for user to create a post'''
    
    user = User.query.get_or_404(user_id)
    form = PostForm()
    
    tags = [(t.id, t.name) for t in Tag.query.all()]
    
    form.tags.choices = tags
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tag_ids = form.tags.data
        
        post = Post(
            title=title,
            content=content,
            user_id=user.id
        )
        
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('user_profile', user_id=user_id))
    
    return render_template('add_post.html', form=form, user=user)

# ////////////////////////////////////////////////////////////////////////

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Shows a specific post by ID'''
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)

# ////////////////////////////////////////////////////////////////////////

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    tags = [(t.id, t.name) for t in Tag.query.all()]
    
    form.tags.choices = tags
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        tag_ids = form.tags.data
        
        for tag in post.tags:
            if tag.id not in tag_ids:
                post.tags.remove(tag)
                
        for tag_id in tag_ids:
            if tag_id not in [tag.id for tag in post.tags]:
                tag = Tag.query.get(tag_id)
                if tag:
                    post.tags.append(tag)
        
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    
    return render_template('edit_post.html', post=post, form=form)

# ////////////////////////////////////////////////////////////////////////

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Deletes a post'''
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_profile', user_id=user_id))

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#       ROUTES FOR TAGS

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/tags')
def tags_list():
    '''Shows a list of all tags'''
    tags = Tag.query.all()
    return render_template('tags_list.html', tags=tags)

# ////////////////////////////////////////////////////////////////////////

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    '''Displays data for a single tag'''
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

# ////////////////////////////////////////////////////////////////////////

@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    '''Handles form to add new tag'''
    form = TagForm()
    
    if form.validate_on_submit():
        name = form.name.data
        
        tag = Tag(name=name)
        
        db.session.add(tag)
        db.session.commit()
        
        return redirect(url_for('tags_list'))
    
    return render_template('add_tag.html', form=form)

# ////////////////////////////////////////////////////////////////////////

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    '''Handles form to edit a tag'''
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm(obj=tag)
    
    if form.validate_on_submit():
        tag.name = form.name.data
        
        db.session.commit()
        return redirect(url_for('show_tag', tag_id=tag.id))
    
    return render_template('edit_tag.html', tag=tag, form=form)

# ////////////////////////////////////////////////////////////////////////

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''deletes a tag'''
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags_list'))

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#       ROUTES FOR POST_TAGS

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/posts/<int:post_id>/tag', methods=['GET', 'POST'])
def tag_posts(post_id):
    '''Handles form to add tags to a post'''