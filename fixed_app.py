from flask import Flask, request
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import subprocess
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


def get_db():
    return sqlite3.connect("users.db")


def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.commit()


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hashed = generate_password_hash(password)
    db = get_db()
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    db.commit()
    return "Registered"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    user = db.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    if user and check_password_hash(user[0], password):
        return f"Welcome {escape(username)}"
    return "Invalid login"


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    if not re.fullmatch(r"[A-Za-z0-9.\-]+", host):
        return "Invalid host", 400
    result = subprocess.run(["ping", "-n", "1", host], capture_output=True, text=True, timeout=10)
    return f"<pre>{escape(result.stdout)}</pre>"


@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return f"<h1>Hello {escape(name)}</h1>"


if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="127.0.0.1")