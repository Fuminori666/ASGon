"""
Core file navigates all path o site
"""


from app import app
from flask import request, render_template, flash, redirect, url_for
from app.forms import LoginForm


"""
Index page of site
"""


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

"""
Login page
"""


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/login', methods=['POST'])
def login_post():
    print(request.form['username'])


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
