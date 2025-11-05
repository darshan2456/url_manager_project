import json
import sqlite3
from urllib.parse import urlparse

def migrate_json_to_db():
    print("🚀 Starting migration from JSON to Database...")
    
    # 1. Read existing JSON data
    try:
        with open('urls.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON file loaded successfully")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return

    # 2. Connect to database
    try:
        conn = sqlite3.connect('url_manager.db')
        cursor = conn.cursor()
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return

    # 3. Get all tags from database for mapping
    cursor.execute("SELECT id, name FROM tags")
    tag_map = {name: id for id, name in cursor.fetchall()}
    print("✅ Tag mapping loaded:", tag_map)

    # 4. Migrate ACTIVE URLs
    active_count = 0
    for url_data in data.get('active', []):
        try:
            # Insert URL
            cursor.execute(
                "INSERT INTO urls (url, title, is_archived) VALUES (?, ?, ?)",
                (url_data['url'], url_data['title'], 0)  # is_archived = 0
            )
            url_id = cursor.lastrowid
            
            # Add tag relationships
            for tag_name in url_data.get('tags', []):
                if tag_name in tag_map:
                    cursor.execute(
                        "INSERT OR IGNORE INTO url_tags (url_id, tag_id) VALUES (?, ?)",
                        (url_id, tag_map[tag_name])
                    )
            
            active_count += 1
        except Exception as e:
            print(f"❌ Error migrating URL {url_data['url']}: {e}")

    # 5. Migrate ARCHIVED URLs
    archived_count = 0
    for url_data in data.get('archived', []):
        try:
            # Insert URL
            cursor.execute(
                "INSERT INTO urls (url, title, is_archived) VALUES (?, ?, ?)",
                (url_data['url'], url_data['title'], 1)  # is_archived = 1
            )
            url_id = cursor.lastrowid
            
            # Add tag relationships
            for tag_name in url_data.get('tags', []):
                if tag_name in tag_map:
                    cursor.execute(
                        "INSERT OR IGNORE INTO url_tags (url_id, tag_id) VALUES (?, ?)",
                        (url_id, tag_map[tag_name])
                    )
            
            archived_count += 1
        except Exception as e:
            print(f"❌ Error migrating archived URL {url_data['url']}: {e}")

    # 6. Commit and close
    conn.commit()
    conn.close()

    print(f"🎉 Migration completed!")
    print(f"📊 Active URLs migrated: {active_count}")
    print(f"📊 Archived URLs migrated: {archived_count}")
    print(f"💾 Total URLs in database: {active_count + archived_count}")

if __name__ == '__main__':
    migrate_json_to_db()