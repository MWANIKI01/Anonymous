import sqlite3

try:
    conn = sqlite3.connect('database.db')
    print("Connected to SQLite database.")
except sqlite3.Error as e:
    print(e)
