from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user

from app.services.auth_service import (
    register_user,
    authenticate,
    get_user_profile,
    update_profile,
    delete_account,
    request_password_reset,
    reset_password,
)
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/")
def auth_index():
    return {"message": "Auth controller placeholder"}


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = register_user(email, username, password)
    if user:
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    flash("Registration failed. Email may already be in use.", "error")
    return redirect(url_for("auth.register"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    user = authenticate(email, password)
    if user:
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for("home.home"))
    flash("Invalid credentials.", "error")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("home.home"))


@auth_bp.get("/profile/<int:user_id>")
def view_profile(user_id: int):
    user = get_user_profile(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("home.home"))
    return render_template("auth/profile.html", user=user)


@auth_bp.post("/profile/<int:user_id>/update")
def update_profile_route(user_id: int):
    new_email = request.form.get("email")
    new_password = request.form.get("password")
    user = update_profile(user_id, new_email=new_email, new_password=new_password)
    if user:
        flash("Profile updated.", "success")
    else:
        flash("Update failed.", "error")
    return redirect(url_for("auth.view_profile", user_id=user_id))


@auth_bp.post("/profile/<int:user_id>/delete")
def delete_account_route(user_id: int):
    deleted = delete_account(user_id)
    if deleted:
        if current_user.is_authenticated and current_user.id == user_id:
            logout_user()
        flash("Account deleted.", "info")
    else:
        flash("Delete failed.", "error")
    return redirect(url_for("home.home"))


@auth_bp.route("/password/request", methods=["GET", "POST"])
def request_password_reset_route():
    if request.method == "GET":
        return render_template("auth/request_password_reset.html")

    email = request.form.get("email")
    token = request_password_reset(email)
    if token:
        flash("Password reset email sent.", "success")
    else:
        flash("Could not start password reset.", "error")
    return redirect(url_for("auth.login"))


@auth_bp.route("/password/reset/<token>", methods=["GET", "POST"])
def reset_password_route(token: str):
    if request.method == "GET":
        return render_template("auth/reset_password.html", token=token)

    new_password = request.form.get("password")
    if reset_password(token, new_password):
        flash("Password reset successful.", "success")
        return redirect(url_for("auth.login"))
    flash("Password reset failed.", "error")
    return redirect(url_for("auth.reset_password_route", token=token))
