from app.extensions import db


class MoodCategory(db.Model):
    __tablename__ = "mood_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<MoodCategory {self.id}: {self.name}>"

    # Getter methods
    def get_name(self) -> str:
        """Get mood category name."""
        return self.name

    def get_description(self) -> str:
        """Get mood category description."""
        return self.description

    # Setter methods
    def set_name(self, new_name: str) -> None:
        """Set mood category name."""
        self.name = new_name
        db.session.commit()

    def set_description(self, new_description: str) -> None:
        """Set mood category description."""
        self.description = new_description
        db.session.commit()
