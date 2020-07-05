import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from login import login


def register(db):

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

        # Ensure -confirm was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 403)

        # Check if user already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("user with that name already exists", 403)

        hash = generate_password_hash(request.form.get(
            "password"), method='pbkdf2:sha256', salt_length=8)

        # Insert user into database for username
        rows = db.execute("INSERT INTO users (username, hash) VALUES  (:username, :hash)",
                          username=request.form.get("username"), hash=hash)

        # Automatic login of newly registered user
        flash('You were successfully registered!')
        return login(db)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
