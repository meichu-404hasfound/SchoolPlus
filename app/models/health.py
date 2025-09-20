from ..extensions import db

class Grade(db.Model):
    __tablename__ = "health"

    account = db.Column(db.String(16), db.ForeignKey("users.account"), primary_key=True)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(256), nullable=True)

    user = db.relationship("User", back_populates="grades")