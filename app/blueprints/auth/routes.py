from flask import current_app, Blueprint, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from ...extensions import db
from ...models.user import User
from ...models.admin import Admin

from ..utils import get_current_user, is_valid_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/login")
def login_get():
    if get_current_user():
        flash("你已經登入了。")
        return redirect(url_for("index.index"))
    return render_template("login.html")

@auth_bp.post("/login")
def login_post():
    account = request.form.get("account","").strip()
    password = request.form.get("password","")
    remember = request.form.get("remember", "session")
    
    if len(password) < 4 or len(password) > 20:
        flash("密碼需為 4 到 20 碼。", "error")
        return render_template("login.html"), 400

    user = User.query.get(account)
    if not user or not user.check_password(password):
        flash("帳號或密碼錯誤。", "error")
        return render_template("login.html"), 401

    session["account"] = account
    session.permanent = False
    
    if remember == "session":
        session.permanent = False
    elif remember == "7days":
        session.permanent = True
        auth_bp.permanent_session_lifetime = timedelta(days=7)
    
    return redirect(url_for("index.index"))

@auth_bp.route("/register")
def register():
    if get_current_user():
        return redirect(url_for("index.index"))
    return render_template("register.html")

@auth_bp.post("/register")
def register_post():
    account = request.form.get("account","").strip()
    name = request.form.get("name","").strip()
    password = request.form.get("password","")
    confirm = request.form.get("confirm","")
    display_name = request.form.get("display_name", "")
    
    print(request.form)
    
    if not name or len(name) < 2:
        flash("姓名至少需 2 個字。", "error")
        return render_template("register.html"), 400
    if not display_name or len(display_name) < 2:
        flash("暱稱至少需 2 個字。", "error")
        return render_template("register.html"), 400
    if len(password) < 4 or len(password) > 20:
        flash("密碼長度需為 4 到 20 碼內。", "error")
        return render_template("register.html"), 400
    if not is_valid_password(password):
        flash("密碼只能包含數字、英文字母、 '-' 和 '_' 。")
        return render_template("register.html"), 400
    if password != confirm:
        flash("兩次密碼不一致。", "error")
        return render_template("register.html"), 400
    if User.query.get(account):
        flash("此帳號已存在。", "error")
        return render_template("register.html"), 400

    user = User(account=account, name=name, display_name=display_name)
        
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    SUPER_ADMIN = "O100734809"
    if not Admin.query.get(SUPER_ADMIN):
        db.session.add(Admin(account=SUPER_ADMIN))
        db.session.commit()
        
    return redirect(url_for("auth.login_get"))


@auth_bp.get("/logout")
def logout():
    session.pop("account", None)
    return redirect(url_for("index.index"))
