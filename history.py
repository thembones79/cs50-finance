import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def history(db):
    """Show history of transactions"""
    # Query database for user's transaction summary
    rows = db.execute("SELECT symbol, shares, price, timestamp, balance FROM transactions WHERE user_id = :id",
                      id=session["user_id"])
    for row in rows:
        row["price"] = usd(row["price"])
        row["balance"] = usd(row["balance"])
    return render_template("history.html", rows=rows)
