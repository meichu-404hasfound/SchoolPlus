from flask import current_app, Blueprint, render_template, redirect, url_for
from ..utils import get_current_user

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    user = get_current_user()

    announcements = [
        {"type": "success", "msg": "System maintenance completed successfully."},
        {"type": "info", "msg": "Midterm exam schedule released."},
        {"type": "danger", "msg": "Network outage expected this weekend."}
    ]

    upcoming = [
        {"course": "Math 101", "when": "Mon 10:00–11:30", "room": "Room A1", "status": "Confirmed"},
        {"course": "Physics 202", "when": "Tue 14:00–15:30", "room": "Lab 3", "status": "Confirmed"},
        {"course": "History 303", "when": "Wed 09:00–10:30", "room": "Room B2", "status": "Pending"}
    ]
    
    if not user:
        return redirect(url_for("auth.login_get"))

    return render_template(
        "index.html",
        user=user,
        announcements=announcements,
        upcoming=upcoming
    )
    
@index_bp.get("/profile")
def profile_get():
    user = get_current_user()
    if not user:
        return redirect(url_for("index.login"))
    
    return render_template(
        "profile.html",
        user=user
    )

@index_bp.route("/dashboard")
def dashboard():
    return render_template("index.html")

@index_bp.route("/courses")
def courses():
    return render_template("index.html")

@index_bp.route("/profile")
def profile():
    return render_template("index.html")