from flask import session, redirect, url_for
from functools import wraps
from re import fullmatch
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlparse

from ...models.user import User
from ...models.admin import Admin

def get_current_user() -> User:
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

def is_valid_avatar_url(url: str) -> bool:
    parsed = urlparse(url)
    if not (parsed.scheme in ("http", "https") and parsed.netloc):
        return False

    try:
        req = Request(url, method="HEAD")
        with urlopen(req, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "").lower()
            return content_type.startswith("image/")
    except URLError:
        return False