"""
Core file navigates all path o site
"""


from app import app
from flask import request, render_template, flash, redirect, url_for
from flask_login import logout_user
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User


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
