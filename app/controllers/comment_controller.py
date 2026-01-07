from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user

from app.services.comment_service import add_comment, edit_comment, delete_comment
from app.models.comment import Comment

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")


@comment_bp.get("/")
def list_comments():
    return {"message": "Comment controller placeholder"}


@comment_bp.post("/add/<int:movie_id>")
def add_comment_route(movie_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to comment.", "error")
        return redirect(url_for("auth.login"))

    text = request.form.get("text")
    if not text:
        flash("Comment cannot be empty.", "error")
        # Fixed: Redirect back to the movie, not the list
        return redirect(url_for("movie.view_movie_details", movie_id=movie_id))

    add_comment(current_user.id, movie_id, text)
    flash("Comment added.", "success")
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))


@comment_bp.route("/<int:comment_id>/edit", methods=["GET", "POST"])
def edit_comment_route(comment_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to edit your comment.", "error")
        return redirect(url_for("auth.login"))

    # 1. Fetch the comment first
    comment = Comment.query.get(comment_id)
    
    # Handle case where comment doesn't exist
    if not comment:
        flash("Comment not found.", "error")
        return redirect(url_for("movie.list_movies"))

    # 2. SAVE the movie_id so we know where to go back to
    movie_id = comment.movie_id

    # Check permission
    if comment.user_id != current_user.id:
        flash("You can only edit your own comments.", "error")
        return redirect(url_for("movie.view_movie_details", movie_id=movie_id))

    if request.method == "GET":
        return render_template("comments/edit_comment.html", comment=comment)

    # 3. Process the Update
    new_text = request.form.get("text")
    updated = edit_comment(current_user.id, comment_id, new_text)
    
    if updated:
        flash("Comment updated.", "success")
    else:
        flash("Update failed.", "error")

    # 4. Redirect back using the SAVED movie_id
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))


@comment_bp.post("/<int:comment_id>/delete")
def delete_own_comment(comment_id: int):
    if not current_user.is_authenticated:
        flash("Please log in to delete your comment.", "error")
        return redirect(url_for("auth.login"))

    # 1. Fetch the comment first
    comment = Comment.query.get(comment_id)
    
    if not comment:
        flash("Comment already deleted or not found.", "error")
        return redirect(url_for("movie.list_movies"))

    # 2. SAVE the movie_id so we know where to go back to
    movie_id = comment.movie_id

    # 3. Delete
    # Note: We use the service, but we already verified existence above.
    delete_comment(current_user.id, comment_id)
    
    flash("Comment deleted.", "info")
    
    # 4. Redirect back using the SAVED movie_id
    return redirect(url_for("movie.view_movie_details", movie_id=movie_id))