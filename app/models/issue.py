from ..extensions import db
from .label import issue_labels, Label
from .comment import Comment

class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(9), db.ForeignKey("users.account"), nullable=False)
    author_name = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, default=0, nullable=False)

    comments = db.relationship(
        "Comment", foreign_keys="Comment.issue_id", cascade="all, delete-orphan"
    )

    # NEW: many-to-many labels
    labels = db.relationship(
        "Label",
        secondary=issue_labels,
        lazy="joined",
        backref=db.backref("issues", lazy="dynamic"),
    )

    # image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=True)
    # image = db.relationship("Image", back_populates="issues", lazy=True)
    # author = db.relationship("User", back_populates="issues")
