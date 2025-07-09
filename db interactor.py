import sqlite3
conn = sqlite3.connect('wallpapers.db')
cur = conn.cursor()
command="CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,wallpaper_filename TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id));"
cur.execute(command)
rows = cur.fetchall()
print(rows)