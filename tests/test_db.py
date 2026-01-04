import sqlite3
import os

def inspect_database():
    print("🕵️‍♂️ Starting Manual Database Inspection...")

    # 1. Locate the database file relative to this test file
    # Go up one level (..) from 'tests' to root, then into 'instance'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "instance", "moodflix.db")

    if not os.path.exists(db_path):
        print(f"❌ Error: Database file not found at: {db_path}")
        print("   Make sure you have run 'python3 run.py' at least once.")
        return

    print(f"📂 Connected to database at: {db_path}")

    # 2. Connect to the DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("\n--- 📋 TABLE LIST ---")
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found. The database is empty.")
        
        for table in tables:
            table_name = table[0]
            print(f"Found Table: {table_name}")
            
            # 3. Inspect 'movies' table specifically
            if table_name == 'movies':
                print(f"\n--- 🎬 CONTENTS OF '{table_name}' ---")
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"Columns: {columns}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"Total Rows: {count}")
                
                if count > 0:
                    print("\n   👇 First 5 Movies:")
                    # Fetch first 5 rows
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    rows = cursor.fetchall()
                    for row in rows:
                        # Print row data safely
                        print(f"   - {row}") 

            # 4. Inspect 'mood_categories' table (to check connections)
            elif table_name == 'mood_categories':
                 print(f"\n--- 🎭 CONTENTS OF '{table_name}' ---")
                 cursor.execute(f"SELECT * FROM {table_name}")
                 rows = cursor.fetchall()
                 if not rows:
                     print("   (Table is empty)")
                 for row in rows:
                     print(f"   - {row}")

            # 5. Inspect the link table (movies_categories)
            elif table_name == 'movie_categories': 
                 print(f"\n--- 🔗 CONTENTS OF '{table_name}' (Links) ---")
                 cursor.execute(f"SELECT * FROM {table_name}")
                 rows = cursor.fetchall()
                 print(f"Total Links: {len(rows)}")
                 for row in rows[:5]:
                     print(f"   - MovieID: {row[0]} <-> CategoryID: {row[1]}")

    except Exception as e:
        print(f"❌ Database Error: {e}")

    finally:
        conn.close()
        print("\n-----------------------")

if __name__ == "__main__":
    inspect_database()