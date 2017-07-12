from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

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
            new_blog_post = Blog(blog_post_title, blog_post_body)
            db.session.add(new_blog_post)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('new_posts.html', title_error=title_error, body_error=body_error, blog_post_title=blog_post_title, blog_post_body=blog_post_body)

    return render_template('new_posts.html')


@app.route('/blog', methods=['GET'])
def blog_list():

    blog_posts = Blog.query.all()

    return render_template('main_blog_page.html', blog_posts=blog_posts)


if __name__ == '__main__':
    app.run()
