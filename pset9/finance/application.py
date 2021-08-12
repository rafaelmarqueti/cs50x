import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    # get portfilo from database
    portfolio = db.execute("SELECT symbol AS Symbol, SUM(quantity) AS Shares FROM transactions \
                WHERE u_id = :u_id GROUP BY symbol", u_id=session['user_id'])
    shares = []
    value = 0
    # iterate through the portfolio and add price and total to the dictionarys
    for stock in portfolio:
        if stock.get("Shares") == 0:
            continue
        quote = lookup(stock.get("Symbol"))
        price = quote.get("price") 
        total = price * stock.get("Shares")
        stock["Price"] = usd(price)
        stock["Total"] = usd(total)
        shares.append(stock)
        value += round(total, 2)

    # get current cash amount
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
    balance = cash[0]["cash"]
    # calculate total aof cash and stock value
    grand_total = value + balance

    return render_template("index.html", shares=shares, balance=usd(balance), value=usd(value), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # send GET requests to the buy form
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        shares = request.form.get("shares")
        # check for missing symbol input
        if request.form.get("symbol"):
            # get stock quote from API
            quote = lookup(request.form.get("symbol"))
        else:
            return apology("Missing Stock Name!", 400)
        # check for invalid symbol
        if quote == None:
            return apology("Invalid Stock Name!", 400)
        # check for missing quantity input
        if not request.form.get("shares"):
            return apology("Missing Share Quantity!", 400)
        # check for invalid input
        if not shares.isdigit():
            return apology("Please provide a positive numeric number", 400)
        elif int(shares) < 1:
            return apology("Please provide a positive number", 400)
        # set variables
        symbol = request.form.get("symbol").upper()
        price = quote.get("price")
        qty = int(shares)
        # get current balance of the user
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
        balance = cash[0]["cash"]
        total = qty * price
        new_balance = balance - total
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # process order if there's enough balance in the account
        if balance >= total:
            # store transaction in the database
            db.execute("INSERT INTO transactions (symbol, quantity, quote, total, timestamp, u_id) VALUES(:symbol, :quantity, :quote, :total, :timestamp, :u_id)",
                       symbol=symbol, quantity=qty, quote=price, total=total, timestamp=timestamp, u_id=session["user_id"])
            # update balance in database
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=round(new_balance, 2), id=session["user_id"])
             # flash a success message
            flash("Successfully bought!")
            return redirect("/")
        else:
            return apology("Not enough cash. Buy less!")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get grouped portfolio
    rows = db.execute(
        "SELECT symbol AS Symbol, SUM(quantity) AS Shares FROM transactions WHERE u_id = :u_id GROUP BY symbol", u_id=session['user_id'])
    # Create stock dropdown list for buy form
    if request.method == "GET":
        symbols = []
        for stock in rows:
            symbols.append(stock.get("Symbol"))
        return render_template("sell.html", symbols=symbols)

    if request.method == "POST":
        shares = request.form.get("shares")
        symbol_sale = request.form.get("symbol")
        # get quantity of stock to sell
        share_stock = db.execute(
            "SELECT SUM(quantity) as quantity from transactions WHERE u_id = :u_id AND symbol = :symbol", u_id=session['user_id'], symbol=symbol_sale)
        share_stock = int(share_stock[0]["quantity"])
        # check quantity for valid number
        if not shares:
            return apology("Missing Share Quantity!", 400)
        elif not shares.isdigit():
            return apology("Please enter a positive numeric number", 400)
        elif int(shares) < 1:
            return apology("Please enter a positive number", 400)
        # check if user has enough shares to sell
        elif int(shares) > share_stock:
            return apology("Not enough shares in your portfolio", 400)
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
            balance = cash[0]["cash"]
            quote = lookup(symbol_sale)
            price = quote.get("price")
            shares_sale = int(shares)
            new_balance = balance + price * shares_sale
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # update cash in user account
            db.execute("UPDATE users SET cash = :cash WHERE id=:id", cash=round(new_balance, 2), id=session["user_id"])
            # store transaction data in the database
            db.execute("INSERT INTO transactions (symbol, quantity, quote, total, timestamp, u_id) \
            VALUES(:symbol, :quantity, :quote, :total, :timestamp, :u_id)", symbol=symbol_sale, quantity=-shares_sale,
                     quote=price, total=shares_sale * price, timestamp=timestamp,  u_id=session["user_id"])
         # flash a success message
        flash("Successfully sold!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol AS Symbol, quantity AS Shares, quote AS Price, timestamp AS Timestamp \
                                FROM transactions WHERE u_id = :u_id", u_id=session['user_id'])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Successfully logged out. Log in again?!")
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Please enter valid symbol", 400)
        else:
            symbol = quote.get("symbol")
            price = quote.get("price")
            return render_template("result.html", symbol=symbol, price=usd(price))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username!", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password!", 400)

        # Ensure password equals condirmation password submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!", 400)
        else:
            # Ensure username doesn't exist already in database
            if len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) == 0:
                # hash the password
                pwdhash = generate_password_hash(request.form.get("password"))
                # insert user to the database
                uid = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"), hash=pwdhash)
                session["user_id"] = uid
                # Redirect user to home page
                flash("Registered successfully!")
                return redirect("/")
            else:
                return apology("Please choose another username!", 400)

    return render_template("register.html")


@app.route("/change_pw", methods=["GET", "POST"])
@login_required
def change_pw():
    """Let user change the password"""
    if request.method == "GET":
        return render_template("change_pw.html")

    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Missing password!", 400)

        # Ensure password equals condirmation password submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!", 400)
        else:
            # hash the password
            pwdhash = generate_password_hash(request.form.get("password"))
            db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=pwdhash, id=session["user_id"])
            # Redirect user to home page
            flash("Password changed!")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
