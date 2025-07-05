import sqlite3
conn = sqlite3.connect('wallpapers.db')
cur = conn.cursor()
cur.execute("Select * From wallpapers")
rows = cur.fetchall()
print(rows)