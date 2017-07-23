from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bloggerz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'aqQX4ZGSUzf0'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/')
def index():
    return redirect('/blog')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in as " + username)
            return redirect('/newpost')
        else:
            if not user:
                flash('User does not exist', 'error')
            elif user.password != password:
                flash('User password is incorrect', 'error')
            # return redirect('/login')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ''
        password_error = ''
        verify_error = ''

        if not username:
            username_error = 'Please enter a username'
        elif len(username) < 3:
            username_error = 'Username must be longer than 3 characters'
            username = ''
        elif ' ' in username:
            username_error = 'Username cannot contain spaces'
            username = ''

        if not password:
            password_error = 'Please enter a password'
        elif len(password) < 3:
            password_error = 'Password must be longer than 3 characters'
            password = ''
        elif ' ' in password:
            password_error = 'Password cannot contain spaces'
            password = ''

        if password != verify:
            verify_error = 'The passwords do not match'
            verify = ''

        if not username_error and not password_error and not verify_error:

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash('Logged in as ' + username)
                return redirect('/blog')
            else:
                flash('This username is already in the database', 'error')
        else:
            return render_template('signup.html', username_error=username_error,
            password_error=password_error, verify_error=verify_error,
            username=username)

    return render_template('signup.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_post_title = request.form['blog_post_title']
        blog_post_body = request.form['blog_post_body']

        title_error = ''
        body_error = ''

        if not blog_post_title:
            title_error = "Please enter a title for your blog post."

        if not blog_post_body:
            body_error = "Please enter some content for your blog post."

        if not title_error and not body_error:
            new_blog_post = Blog(blog_post_title, blog_post_body, owner)
            db.session.add(new_blog_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_blog_post.id))
        else:
            return render_template('new_posts.html', title_error=title_error, body_error=body_error, blog_post_title=blog_post_title, blog_post_body=blog_post_body)

    return render_template('new_posts.html')


@app.route('/blog', methods=['GET'])
def blog_list():

    blog_post_id = request.args.get('id')

    if blog_post_id:
        blog_posts = Blog.query.filter_by(id=blog_post_id).all()
        individual_blog_post = Blog.query.filter_by(id=blog_post_id).first()
        return render_template('individual_blog_post.html', title=individual_blog_post.title, blog_posts=blog_posts)

    blog_posts = Blog.query.order_by(Blog.id.desc()).all()

    return render_template('main_blog_page.html', blog_posts=blog_posts)


if __name__ == '__main__':
    app.run()
