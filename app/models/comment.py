from ..extensions import db
from ..models.user import User

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(9), db.ForeignKey("users.account"), nullable=False)
    issue_id = db.Column(
        db.Integer,
        db.ForeignKey("issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    body = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, default=0, nullable=False)

    issue = db.relationship("Issue", back_populates="comments")
    author = db.relationship("User", back_populates="comments")