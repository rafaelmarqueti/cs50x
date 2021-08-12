import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, hash TEXT);")

# Render the homepage
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Go to Register page 
    if request.method == "GET":
        return render_template("register.html")
    # Register user
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Ensure user registered correctly
        if not username:
            return redirect("/")
        elif not password:
            return redirect("/")
        elif not confirmation:
            return redirect("/")
        elif password != confirmation:
            return redirect("/")

        # Enter user's details into the database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username,
                    password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        
        # Go back to homepage
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return redirect("/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect("/")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout user
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Create new note
@app.route("/new_note", methods=["GET", "POST"])
def new_note():
    if request.method == "GET":
        return render_template("new_note.html")
    else: 
        title = request.form.get("title")
        note = request.form.get("note")

        if not title: 
            return redirect("/new_note")
        elif not note: 
            return redirect("/new_note")
        
        db.execute("CREATE TABLE IF NOT EXISTS notes (note_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, note TEXT, FOREIGN KEY(user_id) REFERENCES users(id));")
        db.execute("INSERT INTO notes (user_id, title, note) VALUES (:user_id, :title, :note)",
                    user_id=session["user_id"], title=title, note=note)
        
        return redirect("/my_notes")

# View 'my' notes
@app.route("/my_notes", methods=["GET", "POST"])
def my_notes():
    rows = db.execute("SELECT title FROM notes WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("my_notes.html", rows=rows)
    
# Review seleted note
@app.route("/review", methods=["GET", "POST"]) 
def review(): 
    if request.method == "POST":
        title = request.form.get("title")
        note = db.execute("SELECT note FROM notes WHERE title = :title AND user_id = :user_id", title=title, user_id=session["user_id"])
    
        return render_template("review.html", title=title, note=note)

# Edit selected note
@app.route("/edit/<title>", methods=["GET", "POST"])
def edit(title):
    if request.method == "GET":
        note = db.execute("SELECT note FROM notes WHERE title = :title AND user_id = :user_id", title=title, user_id=session["user_id"])
        return render_template("edit.html", note=note)
    else: 
        new_note = request.form.get("note")
        db.execute("UPDATE notes SET note = :note WHERE user_id = :user_id AND title = :title", note=new_note, user_id=session["user_id"], title=title) 
        return redirect("/my_notes")
