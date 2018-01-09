from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
import pymongo
from pymongo import MongoClient
__author__ = "Neha"
from src.models.user import User
from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # this just gives a name to the app
app.secret_key = "abcde"  # Secret key is for the cookies sent over the server to get encrypted

@app.before_first_request   # It is run before first request only
def initialize_db():
    Database.initialize()


@app.route('/')
def home_template():
    return render_template("home.html")

@app.route('/view_blogs')
def view_all_blogs_template():
    blogs = Blog.get_all_blogs()
    return render_template("view_blogs.html", blogs=blogs)

@app.route('/login')  # 127.0.0.1:4995/login the end point of our api
def login_template():
    return render_template('login.html')

@app.route('/register')   # 127.0.0.1:4995/register
def register_template():
    return render_template('register.html')

# only post method is allowed, it provides security to data sent over the server
@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password) == True:
        User.login(email)
        email_id = session['email']
        return render_template("profile.html", email=email_id)  # we can pass any data to template, like email
    else:
        session['email'] = None
        return render_template("login_retry.html")


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    if User.register(email, password) == False:
        return render_template("user_exists_register.html")
    else:
        return render_template("profile.html", email=session['email'])



@app.route('/logout')
def logout():
    session['email'] = None
    return render_template("home.html")

@app.route('/profile')
def view_profile():
    return render_template("profile.html", email=session['email'])

@app.route('/blogs')
@app.route('/blogs/<string:user_id>')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template("new_blog.html")
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))  # make response gets the argument value from user_blogs method

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts.html", posts=posts, blog_title=blog.title, blog_id=blog._id)

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template("new_post.html", blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

@app.route('/readposts/<string:blog_id>')
def readblog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts-readonly.html", posts=posts, blog_title=blog.title, blog_id=blog._id)

#@app.route('/search', methods=['POST'])
#def search():
    #query = request.form['query']
    #results = Database.search_blogs(query)
    #return render_template("search.html", results=results)


if __name__ == "__main__":
    app.run(port=4995)  # if we specify the port then process runs on that port only
