from datetime import datetime
from app.extensions import db


class AffiliateLink(db.Model):
    __tablename__ = "affiliate_links"

    id = db.Column(db.Integer, primary_key=True)
    platformName = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AffiliateLink {self.id}: {self.platformName}>"
