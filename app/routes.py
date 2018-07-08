from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Anton'}
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

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')


@app.route('/post')
def post():
    posts = [
        {
            'author': {'username': 'Autor1'},
            'PostBody': 'Post Post Post',
        },
    ]
    return render_template('post.html', title='Post', posts=posts)
