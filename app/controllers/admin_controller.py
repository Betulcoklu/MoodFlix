from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user

from app.services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _require_admin():
    if not current_user.is_authenticated:
        flash("Please log in as admin.", "error")
        return redirect(url_for("auth.login"))
    if getattr(current_user, "role", None) != "admin":
        flash("Admin access required.", "error")
        return redirect(url_for("home.index"))
    return None


@admin_bp.get("/")
def admin_index():
    guard = _require_admin()
    if guard:
        return guard
    return render_template("admin/index.html")


@admin_bp.get("/movies")
def list_movies():
    guard = _require_admin()
    if guard:
        return guard
    movies = AdminService.adminListMovies()
    return render_template("admin/movies.html", movies=movies)


@admin_bp.route("/movies/add", methods=["GET", "POST"])
def add_movie():
    guard = _require_admin()
    if guard:
        return guard
    if request.method == "GET":
        categories = AdminService.adminListCategories()
        return render_template("admin/add_movie.html", categories=categories)

    movie_data = {
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "description": request.form.get("description"),
        "posterUrl": request.form.get("posterUrl"),
        "imdbRating": request.form.get("imdbRating"),
        "is_active": request.form.get("is_active", "true").lower() == "true",
        "mood_category_ids": request.form.getlist("mood_category_ids"),
    }

    AdminService.adminAddMovie(movie_data)
    return redirect(url_for("admin.list_movies"))


@admin_bp.route("/movies/<int:movie_id>/edit", methods=["GET", "POST"])
def edit_movie(movie_id: int):
    guard = _require_admin()
    if guard:
        return guard
    if request.method == "GET":
        movie_list = AdminService.adminListMovies()
        # Find specific movie from the list
        movie = next((m for m in movie_list if m.id == movie_id), None)
        categories = AdminService.adminListCategories()
        return render_template("admin/edit_movie.html", movie=movie, categories=categories)

    movie_data = {
        key: val
        for key, val in {
            "title": request.form.get("title"),
            "year": request.form.get("year"),
            "description": request.form.get("description"),
            "posterUrl": request.form.get("posterUrl"),
            "imdbRating": request.form.get("imdbRating"),
            "is_active": request.form.get("is_active", "true").lower() == "true",
            "mood_category_ids": request.form.getlist("mood_category_ids"),
        }.items()
        if val is not None
    }

    AdminService.adminEditMovie(movie_id, movie_data)
    return redirect(url_for("admin.list_movies"))


@admin_bp.post("/movies/<int:movie_id>/delete")
def delete_movie(movie_id: int):
    guard = _require_admin()
    if guard:
        return guard
    AdminService.adminDeleteMovie(movie_id)
    return redirect(url_for("admin.list_movies"))


@admin_bp.get("/categories")
def list_categories():
    guard = _require_admin()
    if guard:
        return guard
    categories = AdminService.adminListCategories()
    return render_template("admin/categories.html", categories=categories)


@admin_bp.route("/categories/add", methods=["GET", "POST"])
def add_category():
    guard = _require_admin()
    if guard:
        return guard
    if request.method == "GET":
        return render_template("admin/add_category.html")

    category_data = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
    }
    AdminService.adminCreateCategory(category_data)
    return redirect(url_for("admin.list_categories"))


@admin_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id: int):
    guard = _require_admin()
    if guard:
        return guard
    if request.method == "GET":
        categories = AdminService.adminListCategories()
        category = next((c for c in categories if c.id == category_id), None)
        return render_template("admin/edit_category.html", category=category)

    category_data = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
    }
    AdminService.adminEditCategory(category_id, category_data)
    return redirect(url_for("admin.list_categories"))


@admin_bp.post("/categories/<int:category_id>/deactivate")
def deactivate_category(category_id: int):
    guard = _require_admin()
    if guard:
        return guard
    AdminService.adminDeactivateCategory(category_id)
    return redirect(url_for("admin.list_categories"))


@admin_bp.get("/comments")
def list_comments():
    guard = _require_admin()
    if guard:
        return guard
    movie_id = request.args.get("movie_id", type=int)
    comments = AdminService.adminListComments(movie_id)
    return render_template("admin/comments.html", comments=comments, movie_id=movie_id)


@admin_bp.post("/comments/<int:comment_id>/delete")
def delete_comment(comment_id: int):
    guard = _require_admin()
    if guard:
        return guard
    AdminService.adminDeleteComment(comment_id)
    return redirect(url_for("admin.list_comments"))


@admin_bp.get("/suggestions")
def list_pending_suggestions():
    guard = _require_admin()
    if guard:
        return guard
    suggestions = AdminService.adminListPendingSuggestions()
    return render_template("admin/suggestions.html", suggestions=suggestions)


@admin_bp.route("/suggestions/<int:suggestion_id>/edit", methods=["GET", "POST"])
def edit_suggestion(suggestion_id: int):
    guard = _require_admin()
    if guard: return guard

    suggestion = AdminService.adminGetSuggestion(suggestion_id)
    if not suggestion:
        flash("Suggestion not found.", "error")
        return redirect(url_for("admin.list_pending_suggestions"))

    if request.method == "GET":
        categories = AdminService.adminListCategories()
        return render_template("admin/edit_suggestion.html", suggestion=suggestion, categories=categories)

    # Gather form data
    data = {
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "mood_category_id": request.form.get("mood_category_id"),
        "description": request.form.get("description"),
        "posterUrl": request.form.get("posterUrl"),
        "imdbRating": request.form.get("imdbRating"),
    }

    # Check which button was clicked (Save or Approve)
    action = request.form.get("action")

    if action == "save":
        AdminService.adminUpdateSuggestion(suggestion_id, data)
        flash("Suggestion updated.", "info")
        return redirect(url_for("admin.list_pending_suggestions"))
    
    elif action == "approve":
        # First save any changes made in the form
        AdminService.adminUpdateSuggestion(suggestion_id, data)
        # Then approve and create movie
        AdminService.adminApproveSuggestion(suggestion_id)
        flash("Suggestion approved and movie created!", "success")
        return redirect(url_for("admin.list_pending_suggestions"))
        
    return redirect(url_for("admin.list_pending_suggestions"))


@admin_bp.post("/suggestions/<int:suggestion_id>/reject")
def reject_suggestion(suggestion_id: int):
    guard = _require_admin()
    if guard:
        return guard
    AdminService.adminRejectSuggestion(suggestion_id)
    flash("Suggestion rejected.", "info")
    return redirect(url_for("admin.list_pending_suggestions"))


@admin_bp.post("/movies/<int:movie_id>/affiliate/add")
def add_affiliate_link(movie_id: int):
    guard = _require_admin()
    if guard:
        return guard
    link_data = {
        "platformName": request.form.get("platformName"),
        "url": request.form.get("url"),
    }
    AdminService.adminAddAffiliateLink(movie_id, link_data)
    return redirect(url_for("admin.edit_movie", movie_id=movie_id))


@admin_bp.post("/affiliate/<int:link_id>/delete")
def remove_affiliate_link(link_id: int):
    guard = _require_admin()
    if guard:
        return guard
        
    AdminService.adminRemoveAffiliateLink(link_id)
    
    # Get movie_id from the form to redirect back to the edit page
    movie_id = request.form.get("movie_id")
    if movie_id:
        return redirect(url_for("admin.edit_movie", movie_id=movie_id))
        
    return redirect(url_for("admin.list_movies"))