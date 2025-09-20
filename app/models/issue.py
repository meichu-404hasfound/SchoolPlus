from ..extensions import db
from .comment import Comment

class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(16), db.ForeignKey("users.account"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, default=0, nullable=False)
    label = db.Column(db.String(64), nullable=True)

    comments = db.relationship(
        "Comment", foreign_keys="Comment.issue_id", cascade="all, delete-orphan"
    )
    
    author = db.relationship(
        "User",
        foreign_keys=[author_id]
    )
