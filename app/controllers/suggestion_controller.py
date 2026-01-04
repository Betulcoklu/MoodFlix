from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user

from app.services.suggestion_service import SuggestionService
from app.services.movie_service import MovieService

suggestion_bp = Blueprint("suggestion", __name__, url_prefix="/suggestions")


@suggestion_bp.get("/")
def list_suggestions():
    if not current_user.is_authenticated:
        flash("Please log in to view suggestions.", "error")
        return redirect(url_for("auth.login"))

    suggestions = SuggestionService.listUserSuggestions(current_user.id)
    return render_template("suggestions/list.html", suggestions=suggestions)


@suggestion_bp.route("/add", methods=["GET", "POST"])
def submit_suggestion_route():
    if not current_user.is_authenticated:
        flash("Please log in to submit suggestions.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        categories = MovieService.listCategories()
        return render_template("suggestions/add.html", categories=categories)

    category_id = request.form.get("category_id")
    title = request.form.get("title")
    year = request.form.get("year") or None

    try:
        category_id_int = int(category_id) if category_id else None
    except ValueError:
        category_id_int = None

    if not title or not category_id_int:
        flash("Title and category are required.", "error")
        return redirect(url_for("suggestion.submit_suggestion_route"))

    SuggestionService.submitSuggestion(current_user.id, category_id_int, title, int(year) if year else None)
    flash("Suggestion submitted.", "success")
    return redirect(url_for("suggestion.list_suggestions"))
