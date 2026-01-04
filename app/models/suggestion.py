from datetime import datetime
from app.extensions import db


class Suggestion(db.Model):
    __tablename__ = "suggestions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reviewedAt = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Suggestion {self.id}: {self.title}>"

    # Getter methods
    def get_title(self) -> str:
        """Get suggestion title."""
        return self.title

    def get_year(self) -> int:
        """Get suggestion year."""
        return self.year

    def get_status(self) -> str:
        """Get suggestion status (pending, approved, rejected)."""
        return self.status

    # Setter methods
    def set_title(self, new_title: str) -> None:
        """Set suggestion title."""
        self.title = new_title
        db.session.commit()

    def set_year(self, new_year: int) -> None:
        """Set suggestion year."""
        self.year = new_year
        db.session.commit()

    # Status action methods
    def approve(self) -> None:
        """Approve the suggestion."""
        self.status = "approved"
        self.reviewedAt = datetime.utcnow()
        db.session.commit()

    def reject(self) -> None:
        """Reject the suggestion."""
        self.status = "rejected"
        self.reviewedAt = datetime.utcnow()
        db.session.commit()
