import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def buy(db):
    if request.method == "POST":
        # Ensure company symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Company Symbol", 403)

        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        company = lookup(request.form.get("symbol"))

        # Ensure company exists
        if not company:
            return apology("company not found", 404)

        price = float(company["price"])
        shares = int(float(request.form.get("shares")))

        if (shares < 1):
            return apology("you have to buy 1 or more shares", 403)

        value = price * shares

        # Query database for cash
        rows = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])

        cash = rows[0]["cash"]

        if (value > cash):
            return apology("not enough money", 403)

        balance = cash - value

        # Insert transaction into database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares, balance) VALUES  (:user_id, :symbol, :price, :shares, :balance)",
                   user_id=session["user_id"], symbol=company["symbol"], price=price, shares=shares, balance=balance)

        # Update user's cash
        db.execute("UPDATE users SET cash = :balance WHERE id = :id",
                   balance=balance, id=session["user_id"])
        flash('Purchase successfull!')
        return redirect("/")
    else:
        return render_template("buy.html")
