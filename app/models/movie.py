from datetime import datetime
from app.extensions import db


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    posterUrl = db.Column(db.String(500), nullable=True)
    imdbRating = db.Column(db.Float, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"
