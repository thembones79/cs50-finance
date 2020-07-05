import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from quote import quote
from index import index
from buy import buy
from history import history
from login import login
from register import register
from sell import sell
from add_cash import add_cash


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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index_route():
    return index(db)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote_route():
    return quote()


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy_route():
    return buy(db)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell_route():
    return sell(db)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash_route():
    return add_cash(db)


@app.route("/history")
@login_required
def history_route():
    return history(db)


@app.route("/register", methods=["GET", "POST"])
def register_route():
    return register(db)


@app.route("/login", methods=["GET", "POST"])
def login_route():
    return login(db)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
