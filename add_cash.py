import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def add_cash(db):
    if request.method == "POST":
        # Ensure cash was submitted
        if not request.form.get("cash"):
            return apology("must provide amount of cash", 403)

        added_cash = int(float(request.form.get("cash")))

        if (added_cash < 1):
            return apology("you have to add 1 or more dollars", 403)

        # Query database for cash
        rows = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])

        current_cash = rows[0]["cash"]

        cash = current_cash + added_cash

        # Update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                   cash=cash, id=session["user_id"])
        flash('Cash added!')
        return redirect("/")
    else:
        return render_template("add_cash.html")
