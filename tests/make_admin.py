import sys
import os

# 1. Add the parent directory (project root) to Python's path
# This allows us to import 'app' even though we are inside 'tests'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

def promote_user_to_admin(username):
    with app.app_context():
        print(f"🔎 Searching for user: {username}...")
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"   Found user ID {user.id} with role: '{user.role}'")
            if user.role == 'admin':
                print(f"   ℹ️  {user.username} is ALREADY an admin.")
            else:
                user.role = "admin"
                db.session.commit()
                print(f"   ✅ SUCCESS! {user.username} has been promoted to Admin.")
        else:
            print(f"❌ User '{username}' not found. Make sure you registered first!")

if __name__ == "__main__":
    # Change "mert" to your username if different
    promote_user_to_admin("mert")