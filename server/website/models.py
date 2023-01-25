from flask_login import UserMixin
import sqlite3

def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    cur.close()
    return


class User(UserMixin):
    """ User class that is initialised when a user is loaded i.e. logs in
        Attributes can be accessed via current_user.attribute when a user is logged in
	"""
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)