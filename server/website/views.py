from functools import wraps
from flask import Blueprint, render_template, request, redirect, session
from .utilities.database import database_request
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.route('/')
def landing_page():
    return "landing_page"

@views_blueprint.route('/database_test')
#@login_required
def database_test():
    return database_request()


@views_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username or not password or password != confirm_password:
            return render_template("register.html")

        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user:
            return render_template("register.html")
        
        insert_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
        return redirect('/login')
    else:
        return render_template("register.html")

@views_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("login.html")
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if not user or password != user['password']:
            return render_template("login.html")
        session['user_id'] = user['id']
        return redirect('/')
    else:
        return render_template("login.html")


@views_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect('/')



"""
for user in query_db('SELECT * FROM users'):
            print(user['username'] + ' has password ' + user['password'])
            """