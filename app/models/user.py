from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"
    
    account = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
