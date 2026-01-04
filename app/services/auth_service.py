"""Authentication-related business logic."""

from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User


def register_user(email: str, username: str, password: str) -> User | None:
    """
    Register a new user.

    Args:
        email: User's email address
        username: User's username
        password: User's plaintext password

    Returns:
        User object if successful, None if user already exists
    """
    if User.query.filter_by(email=email).first():
        return None  # User already exists

    user = User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> User | None:
    """
    Authenticate a user by email and password.

    Args:
        email: User's email address
        password: User's plaintext password

    Returns:
        User object if credentials are valid, None otherwise
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def get_user_profile(user_id: int) -> User | None:
    """
    Retrieve a user's profile by ID.

    Args:
        user_id: User's ID

    Returns:
        User object if found, None otherwise
    """
    return User.query.get(user_id)


def update_profile(user_id: int, new_email: str | None = None, new_password: str | None = None) -> User | None:
    """
    Update a user's profile.

    Args:
        user_id: User's ID
        new_email: New email address (optional)
        new_password: New plaintext password (optional)

    Returns:
        Updated User object if successful, None if user not found
    """
    user = User.query.get(user_id)
    if not user:
        return None

    if new_email:
        if User.query.filter_by(email=new_email).first():
            return None  # Email already in use
        user.email = new_email

    if new_password:
        user.password_hash = generate_password_hash(new_password)

    db.session.commit()
    return user


def delete_account(user_id: int) -> bool:
    """
    Delete a user account.

    Args:
        user_id: User's ID

    Returns:
        True if successful, False if user not found
    """
    user = User.query.get(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True


def request_password_reset(email: str) -> bool:
    """
    Request a password reset for a user.

    Args:
        email: User's email address

    Returns:
        True if user exists, False otherwise
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    # TODO: Generate and store reset token in a password_reset_tokens table
    # TODO: Send reset email with token link
    return True


def reset_password(token: str, new_password: str) -> bool:
    """
    Reset a user's password using a reset token.

    Args:
        token: Password reset token
        new_password: New plaintext password

    Returns:
        True if successful, False if token invalid or expired
    """
    # TODO: Validate token and retrieve associated user
    # TODO: Check if token is not expired
    # TODO: Update user's password_hash
    # TODO: Delete/invalidate the token
    return False


