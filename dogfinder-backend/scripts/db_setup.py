import sqlite3
import json
import os

DB_PATH = "dogs.db"
JSON_PATH = "dogs_metadata.json"

def setup_database():
    if not os.path.exists(JSON_PATH):
        print(f"No se encontró el archivo {JSON_PATH}")
        return


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dogs (
        id TEXT PRIMARY KEY,
        name TEXT,
        size TEXT,
        color TEXT,
        age INTEGER,
        zone TEXT,
        hasCollar BOOLEAN
    )
    """)


    with open(JSON_PATH, "r", encoding="utf-8") as f:
        dogs = json.load(f)


    for dog in dogs:
        cursor.execute("""
        INSERT OR REPLACE INTO dogs (id, name, size, color, age, zone, hasCollar)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dog["id"],
            dog["name"],
            dog["size"],
            dog["color"],
            int(dog["age"]),
            dog["zone"],
            int(dog["hasCollar"])
        ))

    conn.commit()
    conn.close()
    print(f"Base de datos '{DB_PATH}' creada con {len(dogs)} registros.")

if __name__ == "__main__":
    setup_database()
