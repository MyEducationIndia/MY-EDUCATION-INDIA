import sqlite3, os
from app.core.config import settings

def init_database(fresh: bool = False):
    db_path = settings.DATABASE_PATH
    if fresh and os.path.exists(db_path):
        os.remove(db_path)

    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(db_path)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

init_db = init_database

if __name__ == "__main__":
    init_database()
