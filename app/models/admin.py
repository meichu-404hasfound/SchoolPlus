from ..extensions import db

class Admin(db.Model):
    __tablename__ = "admins"

    account = db.Column(db.String(16), db.ForeignKey("users.account"), primary_key=True)

    user = db.relationship("User", back_populates="admin_entry")