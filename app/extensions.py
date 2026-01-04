from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def import_models() -> None:
	"""Import all models so SQLAlchemy is aware of them."""

	
	from app.models.affiliate_link import AffiliateLink  # noqa: F401
	from app.models.comment import Comment  # noqa: F401
	from app.models.favorite import Favorite  # noqa: F401
	from app.models.mood_category import MoodCategory  # noqa: F401
	from app.models.movie import Movie  # noqa: F401
	from app.models.rating import Rating  # noqa: F401
	from app.models.suggestion import Suggestion  # noqa: F401
	from app.models.user import User  # noqa: F401
