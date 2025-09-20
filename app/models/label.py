from ..extensions import db

# Association table (Issue ⇄ Label)
issue_labels = db.Table(
    "issue_labels",
    db.Column("issue_id", db.Integer, db.ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True),
    db.Column("label_id", db.Integer, db.ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True),
)

class Label(db.Model):
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
