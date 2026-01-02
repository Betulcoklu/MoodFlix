from app.extensions import db


class MoodCategory(db.Model):
    __tablename__ = "mood_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<MoodCategory {self.id}: {self.name}>"
