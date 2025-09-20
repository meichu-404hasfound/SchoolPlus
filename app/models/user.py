from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"
    
    account = db.Column(db.String(9), primary_key=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    name = db.Column(db.String(64), nullable=False)
    display_name = db.Column(db.String(16), nullable=False)
    avatar_url = db.Column(db.String(512), nullable=True)
    
    create_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
