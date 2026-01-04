from datetime import datetime
from app.extensions import db


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Rating {self.id}>"

    # Getter methods
    def get_value(self) -> float:
        """Get rating value."""
        return self.value

    def get_created_at(self) -> datetime:
        """Get rating creation timestamp."""
        return self.createdAt

    def get_updated_at(self) -> datetime:
        """Get rating last update timestamp."""
        return self.updatedAt

    # Setter methods
    def set_value(self, new_value: float) -> None:
        """Set rating value."""
        self.value = new_value
        self.updatedAt = datetime.utcnow()
        db.session.commit()
