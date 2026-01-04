import requests
from app.models.movie import Movie
from app.models.mood_category import MoodCategory
from app import db

class MovieService:
    BASE_URL = "https://api.imdbapi.dev"
    
    @staticmethod
    def fetch_top_100():
        """
        Fetches top rated movies from the external API.
        Uses 'types=MOVIE' (UPPERCASE) to exclude TV shows.
        """
        # 1. Check if DB is already populated
        if Movie.query.count() >= 50:
            print("✅ Database has movies. Skipping API fetch.")
            return

        print("🔄 Fetching Top Movies from API...")
        
        url = f"{MovieService.BASE_URL}/titles"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        
        # 2. Configure Parameters 
        params = {
            'list': 'top_rated_250',
            'limit': 50,       
            'types': 'MOVIE',   # <--- FIX: Must be UPPERCASE "MOVIE"
            'info': 'base_info' 
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                movies_list = data.get('titles', []) or data.get('results', [])
                
                print(f"🔎 DEBUG: API returned {len(movies_list)} valid movies.")

                count = 0
                for item in movies_list:
                    # Double check just in case
                    if item.get('titleType', {}).get('text') == 'TV Series': 
                        continue

                    title_text = item.get('primaryTitle')
                    if not title_text: continue 

                    if Movie.query.filter_by(title=title_text).first():
                        continue

                    year = item.get('startYear')
                    poster_data = item.get('primaryImage', {})
                    poster_url = poster_data.get('url') if poster_data else None
                    rating_data = item.get('rating', {})
                    rating_val = rating_data.get('aggregateRating', 0.0)
                    plot_text = item.get('plot', 'No description available.')

                    # 3. Create Movie Object
                    new_movie = Movie(
                        title=title_text,
                        year=year,
                        posterUrl=poster_url,
                        imdbRating=rating_val,
                        description=plot_text,
                        is_active=True
                    )
                    
                    # 4. Link to Category
                    category = MoodCategory.query.first()
                    if category:
                        new_movie.categories.append(category)

                    db.session.add(new_movie)
                    count += 1
                
                db.session.commit()
                print(f"✅ Successfully imported {count} MOVIES!")
            else:
                print(f"❌ API Request Failed: {response.status_code}")
                print(response.text)

        except Exception as e:
            print(f"❌ Service Error: {e}")