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

    # 1. Gather ALL data from the form (This was missing before!)
    data = {
        "user_id": current_user.id,
        "category_id": request.form.get("category_id"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "description": request.form.get("description"),  # Added
        "posterUrl": request.form.get("posterUrl"),      # Added
        "imdbRating": request.form.get("imdbRating"),    # Added
    }

    # 2. Basic Validation
    if not data["title"] or not data["category_id"]:
        flash("Title and category are required.", "error")
        return redirect(url_for("suggestion.submit_suggestion_route"))

    # 3. Send the dictionary to the Service
    SuggestionService.submitSuggestion(data)
    
    flash("Suggestion submitted successfully!", "success")
    return redirect(url_for("suggestion.list_suggestions"))