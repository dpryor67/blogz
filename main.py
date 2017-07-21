from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bloggerz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


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
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.userame = username
        self.password = password



@app.route('/')
def index():
    return redirect('/blog')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
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
