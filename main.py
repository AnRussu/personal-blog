from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
database = Database("blog.db")
database.create_tables()

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def home_page():
    posts = database.get_posts()
    return render_template('home_page.html', posts=posts)

def search():
    query = request.args.get('category') 
    posts = database.get_posts_by_category(query) 
    return render_template('search_result.html', posts=posts, query=query)


def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        database.add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        user = database.get_user(username)
        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('home_page'))
    return render_template('login.html')

def logout():
    session.clear()
    return redirect(url_for('home_page'))

def new_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        
        media = None
        if 'media' in request.files:
            media_file = request.files['media']
            if media_file.filename != '':
                media_filename = media_file.filename
                media_file.save(os.path.join(app.config['UPLOAD_FOLDER'], media_filename))
                media = media_filename

        database.add_post(title, content, category, session['user_id'], media)
        return redirect(url_for('home_page'))

    return render_template('new_post.html')

def post_page(post_id):
    post = database.get_post(post_id)
    comments = database.get_comments(post_id)

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('register'))
        comment = request.form['comment']
        database.add_comment(post_id, comment, session['user_id'])
        return redirect(url_for('post_page', post_id=post_id))

    return render_template('post_page.html', post=post, comments=comments)

def edit_post(post_id):
    post = database.get_post(post_id)

    if session.get('user_id') != post[4]:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']

        media = post[5]
        if 'media' in request.files:
            media_file = request.files['media']
            if media_file.filename != '':
                media_filename = media_file.filename
                media_file.save(os.path.join(app.config['UPLOAD_FOLDER'], media_filename))
                media = media_filename

        database.update_post(post_id, title, content, category, media)
        return redirect(url_for('post_page', post_id=post_id))

    return render_template('edit_post.html', post=post)

def delete_post(post_id):
    post = database.get_post(post_id)

    if session.get('user_id') != post[4] and session.get('role') != 'admin':
        return redirect(url_for('home_page'))

    database.delete_post(post_id)
    return redirect(url_for('home_page'))

app.add_url_rule('/', 'home_page', home_page)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/new_post', 'new_post', new_post, methods=['GET', 'POST'])
app.add_url_rule('/post/<int:post_id>', 'post_page', post_page, methods=['GET', 'POST'])
app.add_url_rule('/edit_post/<int:post_id>', 'edit_post', edit_post, methods=['GET', 'POST'])
app.add_url_rule('/delete_post/<int:post_id>', 'delete_post', delete_post, methods=['POST'])
app.add_url_rule('/search', 'search', search, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)




