from datetime import datetime
from app.extensions import db


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Favorite {self.id}>"

    # Getter methods
    def get_id(self) -> int:
        """Get favorite ID."""
        return self.id

    def get_user_id(self) -> int:
        """Get user ID."""
        return self.user_id

    def get_movie_id(self) -> int:
        """Get movie ID."""
        return self.movie_id

    def get_created_at(self) -> datetime:
        """Get favorite creation timestamp."""
        return self.createdAt
