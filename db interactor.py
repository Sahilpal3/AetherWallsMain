import sqlite3
conn = sqlite3.connect('wallpapers.db')
cur = conn.cursor()
command="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,username TEXT NOT NULL UNIQUE);"
cur.execute(command)
rows = cur.fetchall()
print(rows)