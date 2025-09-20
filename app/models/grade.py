from ..extensions import db

class Grade(db.Model):
    __tablename__ = "grades"

    account = db.Column(db.String(16), db.ForeignKey("users.account"), primary_key=True)
    grade = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(16), nullable=False)
    description = db.Column(db.String(256), nullable=True)

    user = db.relationship("User", back_populates="grades")