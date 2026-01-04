from datetime import datetime
from app.extensions import db


class AffiliateLink(db.Model):
    __tablename__ = "affiliate_links"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    platformName = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AffiliateLink {self.id}: {self.platformName}>"

    # Getter methods
    def get_platform_name(self) -> str:
        """Get affiliate link platform name."""
        return self.platformName

    def get_url(self) -> str:
        """Get affiliate link URL."""
        return self.url

    # Setter methods
    def set_platform_name(self, new_name: str) -> None:
        """Set affiliate link platform name."""
        self.platformName = new_name
        db.session.commit()

    def set_url(self, new_url: str) -> None:
        """Set affiliate link URL."""
        self.url = new_url
        db.session.commit()
