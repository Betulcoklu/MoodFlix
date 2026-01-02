import os
from flask import Flask
from app.extensions import db, import_models, migrate
from app.config import Config

# Import your blueprints here
from app.controllers.home_controller import home_bp
# import other blueprints as needed
# from app.controllers.auth_controller import bp as auth_bp

def create_app(config_object: str | object = "app.config.Config") -> Flask:
    """Application factory for the Flask app configured for MVC layout."""
    app = Flask(
        __name__,
        template_folder=os.path.join("app", "views", "templates"),
        static_folder=os.path.join("app", "views", "static"),
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
    # Add more extensions here if needed (e.g., Flask-Login)


def register_blueprints(app: Flask) -> None:
    """Register all Flask blueprints."""
    app.register_blueprint(home_bp)
    # Register other blueprints
    # app.register_blueprint(auth_bp)
