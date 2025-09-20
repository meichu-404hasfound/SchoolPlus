from flask import current_app, Blueprint, render_template

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    user = {
        "name": "Alice Johnson",
        "courses": ["Math 101", "Physics 202", "History 303"],
        "avatar_url": "https://static.vecteezy.com/system/resources/previews/002/002/403/non_2x/man-with-beard-avatar-character-isolated-icon-free-vector.jpg"
    }

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

    return render_template(
        "index.html",
        user=user,
        announcements=announcements,
        upcoming=upcoming
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