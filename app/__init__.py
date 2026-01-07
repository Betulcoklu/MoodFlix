import os
from flask import Flask
from app.extensions import db, import_models, migrate, login_manager
from app.config import Config

# Import your blueprints here
from app.controllers.home_controller import home_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.movie_controller import movie_bp
from app.controllers.comment_controller import comment_bp
from app.controllers.favorite_controller import favorite_bp
from app.controllers.rating_controller import rating_bp
from app.controllers.suggestion_controller import suggestion_bp
from app.controllers.admin_controller import admin_bp

def create_app(config_object: str | object = "app.config.Config") -> Flask:
    """Application factory for the Flask app configured for MVC layout."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "views", "templates"),
        static_folder=os.path.join(base_dir, "views", "static"),
    )

    # Load config
    app.config.from_object(config_object)

    # Ensure instance folder exists for runtime files (uploads, SQLite DB, etc.)
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    return app


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    db.init_app(app)
    import_models()
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask) -> None:
    """Register all Flask blueprints."""
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(rating_bp)
    app.register_blueprint(suggestion_bp)
    app.register_blueprint(admin_bp)
