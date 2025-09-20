from flask import current_app, Blueprint, render_template, redirect, url_for, request, flash
from ..utils import get_current_user, is_valid_avatar_url

from ...extensions import db
from ...models.user import User
from ...models.issue import Issue

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    user = get_current_user()

    announcements = [
        {"type": "success", "msg": "系統維​​護成功完成"},
        {"type": "info", "msg": "期中考時間表發布"},
        {"type": "danger", "msg": "預計本週末將出現網路中斷"}
    ]

    upcoming = [
        {"course": "數學 101", "when": "禮拜一 10:00–11:30", "room": "教室 A1", "status": "已確定"},
        {"course": "物理 202", "when": "禮拜二 14:00–15:30", "room": "試驗室 3", "status": "已確定"},
        {"course": "歷史 303", "when": "禮拜三 09:00–10:30", "room": "教室 B2", "status": "代辦中"}
    ]
    
    if not user:
        flash("請先登入。", "error")
        return redirect(url_for("auth.login_get"))
    
    issue = Issue.query.order_by(Issue.upvote).first()
    
    return render_template(
        "index.html",
        user=user,
        issue=issue,
        announcements=announcements,
        upcoming=upcoming
    )
    
@index_bp.get("/profile")
def profile_get():
    user = get_current_user()
    if not user:
        flash("請先登入。", "error")
        return redirect(url_for("index.login"))
    
    return render_template(
        "profile.html",
        user=user
    )
    
@index_bp.post("/profile/update_information")
def profile_post():
    user = get_current_user()
    
    if not user:
        flash("請先登入。", "error")
        return redirect(url_for("index.login"))
      
    display_name = request.form.get("display_name", "").strip()
    avatar_url = request.form.get("avatar_url", "").strip()
    
    user.display_name = display_name
    
    if avatar_url and not is_valid_avatar_url(avatar_url):
        flash("無效的頭像網址。", "error")
        return redirect(url_for("index.profile_get"))
    
    user.avatar_url = avatar_url
    db.session.commit()
    
    flash("個人資料已更新。", "success")
    return redirect(url_for("index.profile_get"))

@index_bp.post("/profile/update_password")
def profile_update_password():
    user = get_current_user()
    if not user:
        flash("請先登入。", "error")
        redirect(url_for("index.login"))
        
    current_password = request.form.get("current_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
        
    if not user.check_password(current_password):
        flash("帳號或密碼錯誤。", "error")
        return redirect(url_for("index.profile_get"))
    
    if current_password != new_password:
        flash("新密碼不一致。", "error")
        return redirect(url_for("index.profile_get"))

    if len(new_password) < 4 or len(new_password) > 20:
        flash("密碼需為 4 到 20 碼。", "error")
        return redirect(url_for("index.profile_get"))

    user.set_password(new_password)
    db.session.commit()
    
    flash("密碼已更新。", "success")
    return redirect(url_for("index.profile_get"))


@index_bp.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))
    
    stats = {"courses": 3, "assignments": 2, "messages": 5}
    announcements = [
        {"type": "info", "msg": "期中考時間表發布"},
        {"type": "success", "msg": "系統維​​護成功完成"},
    ]
    upcoming = [
        {"course": "數學 101", "when": "禮拜一 10:00–11:30", "room": "教室 A1", "status": "已確定"},
        {"course": "物理 202", "when": "禮拜二 14:00–15:30", "room": "試驗室 3", "status": "已確定"},
    ]
    return render_template("dashboard.html",
                           user=user,
                           stats=stats,
                           announcements=announcements,
                           upcoming=upcoming)


@index_bp.route("/courses")
def courses():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    # Weekly schedule with multiple courses
    schedule = {
        "禮拜一": {
            9: {"course": "數學 101", "room": "A1", "status": "已確定"},
            14: {"course": "English Literature 205", "room": "C2", "status": "已確定"}
        },
        "禮拜二": {
            10: {"course": "物理 202", "room": "試驗室 3", "status": "已確定"},
            15: {"course": "哲學 110", "room": "B3", "status": "代辦中"}
        },
        "禮拜三": {
            9: {"course": "歷史 303", "room": "B2", "status": "已確定"},
            13: {"course": "Economics 201", "room": "C1", "status": "已確定"}
        },
        "禮拜四": {
            11: {"course": "Computer Science 404", "room": "C4", "status": "已確定"},
            16: {"course": "Chemistry 220", "room": "試驗室 2", "status": "已確定"}
        },
        "禮拜五": {
            10: {"course": "Biology 150", "room": "B1", "status": "已確定"},
            14: {"course": "Data Science 310", "room": "CompSci 試驗室", "status": "已確定"}
        }
    }

    courses = [
        {"name": "數學 101", "code": "MATH101"},
        {"name": "物理 202", "code": "PHYS202"},
        {"name": "歷史 303", "code": "HIST303"},
        {"name": "電腦課 404", "code": "CS404"},
        {"name": "生物 150", "code": "BIO150"},
        {"name": "化學 220", "code": "CHEM220"},
        {"name": "哲學 110", "code": "PHIL110"},
        {"name": "英文 205", "code": "ENG205"},
        {"name": "經濟學 201", "code": "ECON201"},
        {"name": "資料科學 310", "code": "DS310"},
    ]

    upcoming = {
        "course": "數學 101",
        "when": "禮拜一 09:00–10:30",
        "room": "A1 教室",
        "status": "已確認"
    }

    return render_template(
        "courses.html",
        user=user,
        schedule=schedule,
        courses=courses,
        upcoming=upcoming
    )

@index_bp.route("/messages", defaults={"chat_id": None}, methods=["GET", "POST"])
@index_bp.route("/messages/<int:chat_id>", methods=["GET", "POST"])
def messages(chat_id):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))
    
    conversations = [
        {"id": 1, "name": "Smith 教授", "last_message": "See you in class!", "unread": 2},
        {"id": 2, "name": "Alice Johnson", "last_message": "Got it!", "unread": 0},
    ]
    active_chat = next((c for c in conversations if c["id"] == (chat_id or 1)), conversations[0])
    messages = [
        {"sender": "me", "text": "Hello!", "time": "10:01"},
        {"sender": "them", "text": "Hi! How are you?", "time": "10:02"},
        {"sender": "me", "text": "All good, working on homework.", "time": "10:05"},
    ]
    
    if request.method == "POST":
        text = request.form.get("message")
        if text:
            flash(f"Message sent: {text}", "success")
        return redirect(url_for("index.messages", chat_id=active_chat["id"]))
    return render_template("messages.html",
                           user=user,
                           conversations=conversations,
                           active_chat=active_chat,
                           messages=messages)

@index_bp.route("/notifications")
def notifications():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))
    
    notifications = [
        {"id": 1, "title": "新作業：數學作業", "content": "明天截止", "type": "assignment", "time": "今天 10:00", "read": False, "important": True},
        {"id": 2, "title": "系統更新", "content": "已安排維護", "type": "system", "time": "昨天 16:30", "read": True, "important": False},
        {"id": 3, "title": "來自李教授的新消息", "content": "下午 2 點見", "type": "message", "time": "2 天前", "read": False, "important": True},
    ]
    return render_template("notifications.html", notifications=notifications, user=user)

@index_bp.route("/settings")
def settings():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))
    
    return render_template("settings.html", user=user)


@index_bp.route("/grades")
def grades():
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))
    
    semesters = ["2024 Spring", "2024 Fall", "2025 Spring"]
    current_semester = request.args.get("semester", semesters[-1])

    # Example semester data
    semester_scores = {
        "2024 Spring": [
            {"name": "數學 101", "credits": 3, "grade": "A", "score": 95, "passed": True},
            {"name": "歷史 201", "credits": 2, "grade": "B", "score": 85, "passed": True},
        ],
        "2024 Fall": [
            {"name": "物理 202", "credits": 4, "grade": "B+", "score": 88, "passed": True},
            {"name": "Chemistry 210", "credits": 3, "grade": "C", "score": 72, "passed": True},
            {"name": "哲學 101", "credits": 2, "grade": "F", "score": 45, "passed": False},
        ],
        "2025 Spring": [
            {"name": "Biology 150", "credits": 3, "grade": "A-", "score": 91, "passed": True},
            {"name": "CompSci 101", "credits": 4, "grade": "B", "score": 83, "passed": True},
        ],
    }

    scores = semester_scores.get(current_semester, [])

    summary = {
        "gpa": 3.3,
        "credits": sum(c["credits"] for c in scores),
        "passed": sum(1 for c in scores if c["passed"]),
        "failed": sum(1 for c in scores if not c["passed"]),
        "achievements": ["Top 10% in class", "Completed all assignments on time"]
    }

    # Multi-semester stats
    stats = {
        "gpas": [3.5, 2.9, 3.3],
        "averages": [90, 78, 87],
        "highest": [98, 92, 95],
        "lowest": [82, 45, 72]
    }
    
    progress = {
        "completed": 92,
        "required": 128,
        "core": 60, "core_required": 80,
        "electives": 28, "electives_required": 40,
        "honors": 4, "honors_required": 8
    }
    
    insights = {
        "best_course": "Linear Algebra",
        "best_score": 96,
        "worst_course": "Microeconomics",
        "worst_score": 72,
        "average": 84,
        "trending": "Data Structures",
        "median": 85,                      # middle score for this semester
        "score_distribution": [72, 78, 80, 85, 88, 90, 96],  # can be plotted
        "attendance_rate": "92%",          # overall attendance for semester
        "improvement_since_last": "+5%",   # compared to previous semester
        "top_percentile": "Top 10%",       # ranking in class/school
        "consistency": "High (low variance in scores)",
        "study_recommendation": "Focus more on Economics and Writing courses"
    }
    
    return render_template(
        "grades.html",
        user=user,
        insights=insights,
        progress=progress,
        semesters=semesters,
        current_semester=current_semester,
        scores=scores,
        summary=summary,
        stats=stats
    )


@index_bp.route("/course/<course_id>")
def course(course_id):
    user = get_current_user()
    if not user:
        flash("請先登入。")
        return redirect(url_for("index.login"))

    # Full course catalog
    course_catalog = {
        "MATH101": {
            "name": "數學 101",
            "code": "MATH101",
            "professor": "Dr. Alan Turing",
            "tas": ["Alice Wang", "Brian Chen"],
            "description": "Introduction to calculus: limits, derivatives, integrals, and applications.",
            "materials": [
                {"name": "Lecture Notes", "url": "#"},
                {"name": "Assignment Set 1", "url": "#"}
            ],
            "reviews": [
                {"user": "StudentX", "rating": 5, "comment": "Clear explanations!"},
                {"user": "StudentY", "rating": 4, "comment": "Homework-heavy but useful."}
            ],
            "progress": {"completed": 5, "total": 10},
            "enrollment": 90,
            "tags": ["數學", "Core", "STEM"]
        },
        "PHYS202": {
            "name": "物理 202",
            "code": "PHYS202",
            "professor": "Dr. Marie Curie",
            "tas": ["David Lin", "Sophie Müller"],
            "description": "Classical mechanics with focus on dynamics, oscillations, and waves.",
            "materials": [
                {"name": "試驗室 Manual", "url": "#"},
                {"name": "Simulation Toolkit", "url": "#"}
            ],
            "reviews": [
                {"user": "StudentZ", "rating": 5, "comment": "試驗室s are fun and engaging."},
                {"user": "StudentW", "rating": 3, "comment": "Challenging exams."}
            ],
            "progress": {"completed": 7, "total": 12},
            "enrollment": 120,
            "tags": ["物理", "試驗室oratory", "Core"]
        },
        "HIST303": {
            "name": "歷史 303",
            "code": "HIST303",
            "professor": "Dr. Yuval Harari",
            "tas": ["Catherine Liu"],
            "description": "World history from 1500 to present, emphasizing global interactions.",
            "materials": [
                {"name": "Reading List", "url": "#"},
                {"name": "Primary Sources Packet", "url": "#"}
            ],
            "reviews": [
                {"user": "StudentA", "rating": 4, "comment": "Great storytelling."}
            ],
            "progress": {"completed": 3, "total": 8},
            "enrollment": 60,
            "tags": ["歷史", "Humanities"]
        },
        "CS404": {
            "name": "Computer Science 404",
            "code": "CS404",
            "professor": "Dr. Grace Hopper",
            "tas": ["Lin Mei", "Oscar Ramirez"],
            "description": "Advanced algorithms: graph theory, NP-completeness, approximation algorithms.",
            "materials": [
                {"name": "Algorithm Workbook", "url": "#"},
                {"name": "Project Guidelines", "url": "#"}
            ],
            "reviews": [
                {"user": "StudentB", "rating": 5, "comment": "Inspiring professor."},
                {"user": "StudentC", "rating": 4, "comment": "Projects are tough but rewarding."}
            ],
            "progress": {"completed": 4, "total": 10},
            "enrollment": 80,
            "tags": ["Computer Science", "Algorithms", "Advanced"]
        },
        "BIO150": {
            "name": "Biology 150",
            "code": "BIO150",
            "professor": "Dr. Rosalind Franklin",
            "tas": ["Kunal Patel"],
            "description": "Foundations of molecular biology and genetics.",
            "materials": [{"name": "試驗室 Notebook", "url": "#"}],
            "reviews": [{"user": "StudentD", "rating": 5, "comment": "Hands-on labs are excellent."}],
            "progress": {"completed": 6, "total": 10},
            "enrollment": 100,
            "tags": ["Biology", "試驗室oratory", "STEM"]
        },
        "CHEM220": {
            "name": "Chemistry 220",
            "code": "CHEM220",
            "professor": "Dr. Dmitri Mendeleev",
            "tas": ["Anna Rossi"],
            "description": "Organic chemistry with emphasis on reaction mechanisms.",
            "materials": [{"name": "Reaction Mechanisms Notes", "url": "#"}],
            "reviews": [{"user": "StudentE", "rating": 3, "comment": "Hard but useful for med school."}],
            "progress": {"completed": 2, "total": 12},
            "enrollment": 75,
            "tags": ["Chemistry", "Pre-Med"]
        },
        "PHIL110": {
            "name": "哲學 110",
            "code": "PHIL110",
            "professor": "Dr. Aristotle Papadopoulos",
            "tas": ["Nina Zhang"],
            "description": "Introduction to philosophy: logic, ethics, metaphysics.",
            "materials": [{"name": "Logic Practice Sheets", "url": "#"}],
            "reviews": [{"user": "StudentF", "rating": 4, "comment": "Made me think deeply."}],
            "progress": {"completed": 8, "total": 10},
            "enrollment": 45,
            "tags": ["哲學", "Humanities", "Elective"]
        },
        "ENG205": {
            "name": "English Literature 205",
            "code": "ENG205",
            "professor": "Dr. Emily Brontë",
            "tas": ["Tom Harris"],
            "description": "British literature from Shakespeare to modern poetry.",
            "materials": [{"name": "Poetry Anthology", "url": "#"}],
            "reviews": [{"user": "StudentG", "rating": 5, "comment": "Loved the class discussions."}],
            "progress": {"completed": 7, "total": 9},
            "enrollment": 50,
            "tags": ["English", "Literature", "Humanities"]
        },
        "ECON201": {
            "name": "Economics 201",
            "code": "ECON201",
            "professor": "Dr. Adam Smith",
            "tas": ["Yuki Tanaka"],
            "description": "Principles of microeconomics: markets, supply and demand, elasticity.",
            "materials": [{"name": "Problem Sets", "url": "#"}],
            "reviews": [{"user": "StudentH", "rating": 4, "comment": "Clear explanations."}],
            "progress": {"completed": 5, "total": 10},
            "enrollment": 110,
            "tags": ["Economics", "Social Sciences"]
        },
        "DS310": {
            "name": "Data Science 310",
            "code": "DS310",
            "professor": "Dr. Geoffrey Hinton",
            "tas": ["Lara Kim", "Sam Wu"],
            "description": "Applied data science: machine learning, data visualization, big data tools.",
            "materials": [
                {"name": "Jupyter Notebooks", "url": "#"},
                {"name": "Dataset Samples", "url": "#"}
            ],
            "reviews": [{"user": "StudentI", "rating": 5, "comment": "Very practical course."}],
            "progress": {"completed": 3, "total": 8},
            "enrollment": 130,
            "tags": ["Data Science", "Machine Learning", "STEM"]
        }
    }

    if course_id not in course_catalog:
        flash("找不到此課程。")
        return redirect(url_for("index.courses"))

    course_semesters = ["Fall 2022", "Spring 2023", "Fall 2023"]
    course_scores = [78, 82, 88]

    return render_template(
        "course.html",
        user=user,
        course=course_catalog[course_id],
        courseSemesters=course_semesters,
        courseScores=course_scores
    )
