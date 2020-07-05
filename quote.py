import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensure company symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide Company Symbol", 403)
        company = lookup(request.form.get("symbol"))

        # Ensure company exists
        if not company:
            return apology("company not found", 404)
        return render_template("quoted.html", name=company["name"], price=usd(company["price"]), symbol=company["symbol"])
    else:
        return render_template("quote.html")
