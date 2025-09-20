from pathlib import Path
import os
import secrets
from sqlalchemy.pool import NullPool

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

class Config:
    # TODO: Add a dev config
    ...


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{INSTANCE_DIR / 'app.db'}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool}
    
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"