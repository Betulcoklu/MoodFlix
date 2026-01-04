from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"

    # Getter methods
    def get_text(self) -> str:
        """Get comment text."""
        return self.text

    def get_created_at(self) -> datetime:
        """Get comment creation timestamp."""
        return self.createdAt

    def get_updated_at(self) -> datetime:
        """Get comment last update timestamp."""
        return self.updatedAt

    # Setter methods
    def set_text(self, new_text: str) -> None:
        """Set comment text."""
        self.text = new_text
        self.updatedAt = datetime.utcnow()
        db.session.commit()
