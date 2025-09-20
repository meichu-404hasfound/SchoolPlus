from flask import session, redirect, url_for
from functools import wraps
from re import fullmatch

from ...models.user import User
from ...models.admin import Admin

def get_current_user():
    account = session.get("account")
    if not account:
        return None
    return User.query.get(account)

def is_admin(user: User) -> bool:
    return Admin.query.get(user.account) is not None

def is_valid_password(password: str) -> bool:
    return bool(fullmatch(r"[a-zA-Z0-9-_]+", password))

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for("main.login_get"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = get_current_user()
        if not u:
            return redirect(url_for("main.login_get"))
        if not is_admin(u):
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return wrapper
