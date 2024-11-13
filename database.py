import sqlite3 as sq

class Database:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                              (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT DEFAULT 'user')''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                              (id INTEGER PRIMARY KEY, title TEXT, content TEXT, category TEXT, user_id INTEGER, media TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS comments
                              (id INTEGER PRIMARY KEY, post_id INTEGER, comment TEXT, user_id INTEGER)''')
        self.connection.commit()

    def add_user(self, username, password, role='user'):
        self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.connection.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def add_post(self, title, content, category, user_id, media):
        self.cursor.execute("INSERT INTO posts (title, content, category, user_id, media) VALUES (?, ?, ?, ?, ?)",
                            (title, content, category, user_id, media))
        self.connection.commit()

    def get_posts(self):
        self.cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        return self.cursor.fetchall()

    def get_post(self, post_id):
        self.cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        return self.cursor.fetchone()

    def add_comment(self, post_id, comment, user_id):
        self.cursor.execute("INSERT INTO comments (post_id, comment, user_id) VALUES (?, ?, ?)",
                            (post_id, comment, user_id))
        self.connection.commit()

    def get_comments(self, post_id):
        self.cursor.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,))
        return self.cursor.fetchall()

    def delete_post(self, post_id):
        self.cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        self.connection.commit()

    def update_post(self, post_id, title, content, category, media):
        self.cursor.execute("UPDATE posts SET title = ?, content = ?, category = ?, media = ? WHERE id = ?",
                            (title, content, category, media, post_id))
        self.connection.commit()

    def get_posts_by_category(self, category):
        self.cursor.execute("SELECT * FROM posts WHERE category = ? ORDER BY id DESC", (category,))
        return self.cursor.fetchall()



