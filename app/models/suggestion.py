from datetime import datetime
from app.extensions import db


class Suggestion(db.Model):
    __tablename__ = "suggestions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reviewedAt = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Suggestion {self.id}: {self.title}>"
