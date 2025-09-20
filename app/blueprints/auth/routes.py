from flask import current_app, Blueprint, render_template
from ...extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/register")
def register():
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    return ""
