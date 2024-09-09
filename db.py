import sqlite3
import os

def get_db_cursor():
    db_path = os.getenv("DB_PATH")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    return cursor