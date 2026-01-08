from datetime import datetime
from app.extensions import db

# Association table for Movie-MoodCategory many-to-many relationship
movie_mood_categories = db.Table('movie_mood_categories',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('mood_category_id', db.Integer, db.ForeignKey('mood_categories.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    posterUrl = db.Column(db.String(500), nullable=True)
    imdbRating = db.Column(db.Float, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    mood_categories = db.relationship('MoodCategory', secondary=movie_mood_categories, backref=db.backref('movies', lazy='dynamic'))
    affiliate_links = db.relationship('AffiliateLink', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='movie', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"

    # Getter methods
    def get_id(self) -> int:
        """Get movie ID."""
        return self.id

    def get_title(self) -> str:
        """Get movie title."""
        return self.title

    def get_year(self) -> int:
        """Get movie year."""
        return self.year

    def get_description(self) -> str:
        """Get movie description."""
        return self.description

    def get_poster_url(self) -> str:
        """Get movie poster URL."""
        return self.posterUrl

    def get_imdb_rating(self) -> float:
        """Get movie IMDB rating."""
        return self.imdbRating


    # Setter methods
    def set_title(self, new_title: str) -> None:
        """Set movie title."""
        self.title = new_title
        db.session.commit()

    def set_year(self, new_year: int) -> None:
        """Set movie year."""
        self.year = new_year
        db.session.commit()

    def set_description(self, new_description: str) -> None:
        """Set movie description."""
        self.description = new_description
        db.session.commit()

    def set_poster_url(self, new_poster_url: str) -> None:
        """Set movie poster URL."""
        self.posterUrl = new_poster_url
        db.session.commit()

    def set_imdb_rating(self, new_rating: float) -> None:
        """Set movie IMDB rating."""
        self.imdbRating = new_rating
        db.session.commit()
