from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/")
def index():
    """Render the landing page."""
    context = {
        "title": "MoodFlix",
        "message": "Welcome to the Flask MVC starter.",
    }
    return render_template("home.html", **context)
