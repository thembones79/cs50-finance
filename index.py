import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def index(db):
    """Show portfolio of stocks"""
    # Query database for user's transaction summary
    rows = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = :id GROUP BY symbol",
                      id=session["user_id"])
    # Add relevant data
    total = 0.0
    for row in rows:
        company = lookup(row["symbol"])
        row["price"] = usd(company["price"])
        row["name"] = company["name"]
        row["total"] = usd(row["shares"]*company["price"])
        total = total+(row["shares"]*company["price"])
        # remove empty stocks from the list
        if row["shares"] == 0:
            rows.remove(row)

    # Query database for cash
    money = db.execute("SELECT cash FROM users WHERE id = :id",
                       id=session["user_id"])

    cash = money[0]["cash"]
    sum = usd(cash + total)
    cash = usd(cash)
    total = usd(total)

    return render_template("index.html", rows=rows, cash=cash, sum=sum)
