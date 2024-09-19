import sqlite3
import os
from dotenv import load_dotenv

def get_db_cursor():
    load_dotenv()
    db_path = os.getenv("DB_PATH")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    return cursor