import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def sell(db):
    # Query database for user's transaction summary
    rows = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = :id GROUP BY symbol",
                      id=session["user_id"])
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

        # Ensure that user ownes any shares of submitted company
        count = 0
        for row in rows:
            if (request.form.get("symbol") == row["symbol"]):
                count = count + 1
        if (count == 0):
            return apology("you don't have any shares of " + request.form.get("symbol"), 404)

        # Ensure that submitted shres number is integer and within range between 1 and possesed number of shares
        submitted_shares = int(float(request.form.get("shares")))

        if (submitted_shares < 1):
            return apology("number of shares has to be 1 or more", 403)

        for row in rows:
            if (request.form.get("symbol") == row["symbol"]):
                if (row["shares"] < submitted_shares):
                    return apology("you can't sell more shares than you have", 403)

        price = float(company["price"])
        value = price * submitted_shares

        # Query database for cash
        money = db.execute("SELECT cash FROM users WHERE id = :id",
                           id=session["user_id"])

        cash = money[0]["cash"]
        balance = cash + value

        # Insert transaction into database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares, balance) VALUES  (:user_id, :symbol, :price, :shares, :balance)",
                   user_id=session["user_id"], symbol=company["symbol"], price=price, shares=(-1*submitted_shares), balance=balance)

        # Update user's cash
        db.execute("UPDATE users SET cash = :balance WHERE id = :id",
                   balance=balance, id=session["user_id"])
        flash('Sold!')
        return redirect("/")
    else:
        for row in rows:
            # remove empty stocks from the list
            if row["shares"] == 0:
                rows.remove(row)

        return render_template("sell.html", rows=rows)
