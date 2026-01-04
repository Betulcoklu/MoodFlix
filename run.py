from app import create_app
from app.extensions import db
from app.services.movie_service import MovieService

app = create_app()

if __name__ == '__main__':
    # Create the database and fetch movies before the server starts
    with app.app_context():
        # 1. Create Tables (if moodflix.db doesn't exist)
        db.create_all()
        print("✅ Database tables checked/created.")

        # 2. Populate Movies (Logic inside service handles duplicates)
        MovieService.fetch_top_100()

    # Start the application
    app.run(debug=True)