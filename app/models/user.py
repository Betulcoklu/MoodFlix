from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # "user" or "admin"
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    comments = db.relationship('Comment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    suggestions = db.relationship('Suggestion', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

    # Getter methods
    def get_id(self) -> int:
        """Get user ID."""
        return self.id

    def get_email(self) -> str:
        """Get user email."""
        return self.email

    def get_username(self) -> str:
        """Get user username."""
        return self.username

    def get_role(self) -> str:
        """Get user role."""
        return self.role

    def is_active_user(self) -> bool:
        """Check if user is active."""
        return self.is_active

    # Setter methods
    def set_email(self, new_email: str) -> None:
        """Set user email."""
        self.email = new_email
        db.session.commit()

    def set_username(self, new_username: str) -> None:
        """Set user username."""
        self.username = new_username
        db.session.commit()

    def set_role(self, new_role: str) -> None:
        """Set user role."""
        self.role = new_role
        db.session.commit()

    # Account status methods
    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
        db.session.commit()

    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        db.session.commit()

    # Password methods
    def set_password_hash(self, new_password_hash: str) -> None:
        """Set password hash directly (internal use)."""
        self.password_hash = new_password_hash
        db.session.commit()

    def check_password(self, candidate_password: str) -> bool:
        """Check if provided password matches the stored hash."""
        return check_password_hash(self.password_hash, candidate_password)