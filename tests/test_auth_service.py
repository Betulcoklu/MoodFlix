"""Tests for authentication service."""

import sys
from pathlib import Path

# Add project root to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.extensions import db
from app.services.auth_service import (
    register_user,
    authenticate,
    get_user_profile,
    update_profile,
    delete_account,
)
from app.models.user import User


def test_register_user():
    """Test user registration."""
    app = create_app()
    with app.app_context():
        # Clean up any existing test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

        # Test successful registration
        print("\n--- Testing register_user ---")
        user = register_user('test@example.com', 'testuser', 'password123')
        assert user is not None, "User should be created"
        assert user.email == 'test@example.com', "Email should match"
        assert user.username == 'testuser', "Username should match"
        print(f"✓ User registered: {user.username} ({user.email})")

        # Test duplicate email registration
        print("\n--- Testing duplicate email ---")
        duplicate = register_user('test@example.com', 'testuser2', 'password456')
        assert duplicate is None, "Duplicate email should be rejected"
        print("✓ Duplicate email rejected")


def test_authenticate():
    """Test user authentication."""
    app = create_app()
    with app.app_context():
        # Ensure test user exists
        test_user = User.query.filter_by(email='auth_test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

        register_user('auth_test@example.com', 'authuser', 'secure123')

        # Test authenticate with correct credentials
        print("\n--- Testing authenticate (correct credentials) ---")
        auth_user = authenticate('auth_test@example.com', 'secure123')
        assert auth_user is not None, "Authentication should succeed"
        assert auth_user.username == 'authuser', "Username should match"
        print(f"✓ Authentication successful: {auth_user.username}")

        # Test authenticate with wrong password
        print("\n--- Testing authenticate (wrong password) ---")
        auth_fail = authenticate('auth_test@example.com', 'wrongpassword')
        assert auth_fail is None, "Wrong password should fail"
        print("✓ Wrong password rejected")

        # Test authenticate with nonexistent email
        print("\n--- Testing authenticate (nonexistent email) ---")
        auth_none = authenticate('nonexistent@example.com', 'password')
        assert auth_none is None, "Nonexistent user should fail"
        print("✓ Nonexistent email rejected")


def test_get_user_profile():
    """Test retrieving user profile."""
    app = create_app()
    with app.app_context():
        # Ensure test user exists
        test_user = User.query.filter_by(email='profile_test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

        user = register_user('profile_test@example.com', 'profileuser', 'pass123')

        # Test get user profile
        print("\n--- Testing get_user_profile ---")
        retrieved = get_user_profile(user.id)
        assert retrieved is not None, "User should be found"
        assert retrieved.username == 'profileuser', "Username should match"
        print(f"✓ User profile retrieved: {retrieved.username}")

        # Test get nonexistent user
        print("\n--- Testing get_user_profile (nonexistent) ---")
        not_found = get_user_profile(99999)
        assert not_found is None, "Nonexistent user should return None"
        print("✓ Nonexistent user returns None")


def test_update_profile():
    """Test updating user profile."""
    app = create_app()
    with app.app_context():
        # Ensure test user exists
        test_user = User.query.filter_by(email='update_test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

        user = register_user('update_test@example.com', 'updateuser', 'pass123')
        user_id = user.id

        # Test update email
        print("\n--- Testing update_profile (email) ---")
        updated = update_profile(user_id, new_email='newemail@example.com')
        assert updated is not None, "Update should succeed"
        assert updated.email == 'newemail@example.com', "Email should be updated"
        print(f"✓ Email updated to {updated.email}")

        # Test update password
        print("\n--- Testing update_profile (password) ---")
        updated = update_profile(user_id, new_password='newpass456')
        assert updated is not None, "Update should succeed"
        auth_new = authenticate('newemail@example.com', 'newpass456')
        assert auth_new is not None, "New password should work"
        print("✓ Password updated and verified")

        # Test update nonexistent user
        print("\n--- Testing update_profile (nonexistent) ---")
        not_found = update_profile(99999, new_email='test@example.com')
        assert not_found is None, "Nonexistent user should return None"
        print("✓ Nonexistent user update returns None")


def test_delete_account():
    """Test deleting user account."""
    app = create_app()
    with app.app_context():
        # Ensure test user exists
        test_user = User.query.filter_by(email='delete_test@example.com').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

        user = register_user('delete_test@example.com', 'deleteuser', 'pass123')
        user_id = user.id

        # Test delete account
        print("\n--- Testing delete_account ---")
        deleted = delete_account(user_id)
        assert deleted is True, "Delete should succeed"

        # Verify user is deleted
        found = get_user_profile(user_id)
        assert found is None, "Deleted user should not be found"
        print("✓ Account deleted successfully")

        # Test delete nonexistent user
        print("\n--- Testing delete_account (nonexistent) ---")
        not_found = delete_account(99999)
        assert not_found is False, "Deleting nonexistent user should fail"
        print("✓ Deleting nonexistent user returns False")


if __name__ == '__main__':
    print("=" * 50)
    print("Running Auth Service Tests")
    print("=" * 50)

    try:
        test_register_user()
        test_authenticate()
        test_get_user_profile()
        test_update_profile()
        test_delete_account()

        # print("\n" + "=" * 50)
        # print("✓ All tests passed!")
        # print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
