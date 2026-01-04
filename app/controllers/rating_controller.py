from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import current_user

from app.services.rating_service import rate_movie, get_user_rating_for_movie, remove_rating

rating_bp = Blueprint("rating", __name__, url_prefix="/ratings")


@rating_bp.get("/")
def list_ratings():
    return {"message": "Rating controller placeholder"}


@rating_bp.post("/add/<int:movie_id>")
def rate_movie_route(movie_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to rate movies.", "error")
        return redirect(url_for("auth.login"))

    try:
        value = float(request.form.get("value"))
    except (TypeError, ValueError):
        flash("Invalid rating value.", "error")
        return redirect(url_for("movie.view_movie_details", movie_id=movie_id))

    rate_movie(current_user.id, movie_id, value)
    flash("Rating saved.", "success")
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))


@rating_bp.get("/<int:movie_id>")
def get_user_rating_route(movie_id: int):
    if not current_user.is_authenticated:
        return jsonify({"rating": None})
    rating = get_user_rating_for_movie(current_user.id, movie_id)
    return jsonify({"rating": rating.value if rating else None})


@rating_bp.post("/remove/<int:movie_id>")
def remove_rating_route(movie_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to update ratings.", "error")
        return redirect(url_for("auth.login"))

    remove_rating(current_user.id, movie_id)
    flash("Rating removed.", "info")
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))
