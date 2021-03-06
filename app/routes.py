"""
Core file navigates all path o site
"""


from app import app
from flask import request, render_template, flash, redirect, url_for
from flask_login import logout_user, login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import User
from app import db
from app.forms import RegistrationForm, EditProfileForm


"""
Index page of site
"""


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'Admin'},
            'body': 'New weapons has arrived'
        },
        {
            'author': {'username': 'Admin'},
            'body': 'So cool!'
        },
        {
            'author': {'username': 'Admin'},
            'body': 'Post2'
        },
        {
            'author': {'username': 'Admin'},
            'body': 'Post2'
        },
        {
            'author': {'username': 'Admin'},
            'body': 'Post2'
        },
    ]

    return render_template("index.html", title='Home Page', posts=posts)

"""
Login page
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

"""
Not found page
"""


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')


"""
Post page
"""


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = [
        {
            'author': {'username': 'Autor1'},
            'PostBody': 'Post Post Post',
        },
    ]
    return render_template('post.html', title='Post', posts=posts)


"""
Register page function
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, surname=form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        password = request.form.get('password', None)
        if password is None:
            db.session.commit()
        else:
            current_user.set_password(form.password.data)
            db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)
