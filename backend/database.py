
import sqlite3

DATABASE_NAME = "travel.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Countries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT
        )
    """)

    # Cities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """)

    # Attractions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            address TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    """)

    # South Korea
    cursor.execute("""
        INSERT OR IGNORE INTO countries (name, code)
        VALUES ('South Korea', 'KR')
    """)

    cursor.execute(
        "SELECT id FROM countries WHERE code = 'KR'"
    )
    country_id = cursor.fetchone()["id"]

    # Korean cities
    cities = [
        ("Seoul", "South Korea's capital city."),
        ("Busan", "A coastal city famous for beaches."),
        ("Jeju", "A popular island destination."),
        ("Incheon", "A major coastal city and airport hub."),
        ("Gyeongju", "A historic city with cultural heritage."),
        ("Cheongju", "A city in North Chungcheong Province.")
    ]

    for city_name, description in cities:
        cursor.execute("""
            INSERT OR IGNORE INTO cities
            (country_id, name, description)
            VALUES (?, ?, ?)
        """, (country_id, city_name, description))

    # Tourist attractions
    attractions = {
        "Seoul": [
            ("Gyeongbokgung Palace", "History",
             "A famous royal palace in Seoul."),
            ("N Seoul Tower", "Viewpoint",
             "A popular observation tower."),
            ("Myeongdong", "Shopping",
             "A popular shopping and street food district.")
        ],
        "Busan": [
            ("Haeundae Beach", "Beach",
             "One of Busan's most famous beaches."),
            ("Gamcheon Culture Village", "Culture",
             "A colorful hillside village."),
            ("Haedong Yonggungsa Temple", "Temple",
             "A beautiful Buddhist temple by the sea.")
        ],
        "Jeju": [
            ("Seongsan Ilchulbong", "Nature",
             "A volcanic tuff cone and UNESCO World Heritage site."),
            ("Hallasan National Park", "Nature",
             "A national park around Hallasan Mountain."),
            ("Manjanggul Lava Tube", "Nature",
             "A famous volcanic lava tube.")
        ],
        "Incheon": [
            ("Songdo Central Park", "Park",
             "A modern waterfront park."),
            ("Chinatown", "Culture",
             "A historic Chinese cultural district."),
            ("Wolmido", "Entertainment",
             "A popular island leisure area.")
        ],
        "Gyeongju": [
            ("Bulguksa Temple", "History",
             "A historic Buddhist temple."),
            ("Donggung Palace and Wolji Pond", "History",
             "A historic palace site and scenic pond."),
            ("Cheomseongdae", "History",
             "An ancient astronomical observatory.")
        ],
        "Cheongju": [
            ("Cheongju National Museum", "Museum",
             "A museum featuring regional history."),
            ("Sangdangsanseong Fortress", "History",
             "A historic mountain fortress."),
            ("Cheongnamdae", "Attraction",
             "A former presidential retreat.")
        ]
    }

    for city_name, places in attractions.items():
        cursor.execute(
            "SELECT id FROM cities WHERE name = ?",
            (city_name,)
        )
        city = cursor.fetchone()

        if city:
            for name, category, description in places:
                cursor.execute("""
                    INSERT INTO attractions
                    (city_id, name, category, description)
                    SELECT ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM attractions
                        WHERE city_id = ? AND name = ?
                    )
                """, (
                    city["id"], name, category, description,
                    city["id"], name
                ))

    connection.commit()
    connection.close()

    print("Database created successfully!")
    print("South Korea cities and attractions added.")


if __name__ == "__main__":
    create_database()
