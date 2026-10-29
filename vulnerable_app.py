from flask import Flask, request
import sqlite3
import hashlib
import os

app = Flask(__name__)
SECRET_KEY = "admin123"


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
    hashed = hashlib.md5(password.encode()).hexdigest()
    db = get_db()
    db.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')")
    db.commit()
    return "Registered"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hashed = hashlib.md5(password.encode()).hexdigest()
    db = get_db()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed}'"
    user = db.execute(query).fetchone()
    if user:
        return f"Welcome {username}"
    return "Invalid login"


@app.route("/ping")
def ping():
    host = request.args.get("host")
    return os.popen("ping -n 1 " + host).read()


@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return f"<h1>Hello {name}</h1>"


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")