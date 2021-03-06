from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:stg!@#$%@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(360))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()

    return render_template('newpost.html', title='Build a Blog', blogs=blogs, completed_blogs=completed_blogs)

@app.route('/blog', methods=['POST', 'GET'])
def blog_listings():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newblog = Blog(title, body)
        db.session.add(newblog)
        db.session.commit()
    
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_error_message = "Please fill in the title"
    body_error_message = "Please fill in the body"
        
    if request.method == 'POST':
        newBlog_title = request.form['title']
        body = request.form['body']
        newblog = Blog(newBlog_title, body)
        db.session.add(newblog)
        db.session.commit()

        # Stores the id of the post
        new_postId = str(newblog.id)
        
        blogs = Blog.query.all()
        blogs.append(newblog)

        if newBlog_title == "" or body == "":

             return render_template('newpost.html', newBlog_title=newBlog_title, body=body, title_error=title_error_message,
             body_error=body_error_message)

        #return redirect('/blog')

        #redirects to single-entry.html to show the post
        return redirect('/single_post/' + new_postId)

    return render_template('newpost.html')

@app.route('/single_post/<int:id>', methods=['POST', 'GET'])
def single_post(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single-entry.html', blog=blog)



if __name__ == '__main__':
    app.run()