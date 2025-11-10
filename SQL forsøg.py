import sqlite3 as sql

conn = sql.connect("Lysniveau.db")
cursor = conn.cursor()

data = [
    (1, "D2110", 1400, 3000, 250),  # updated values
    (1, "D2115", 150, 200, 950),
    (2, "D2221", 1200, 1300, 175),
    (2, "D2111", 1200, 1300, 175)
]

cursor.executemany("""
INSERT INTO lokaledata (etage, lokale, x, y, lys_niveau)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(etage, lokale)
DO UPDATE SET
    x = excluded.x,
    y = excluded.y,
    lys_niveau = excluded.lys_niveau
""", data)

conn.commit()

cursor.execute("SELECT * FROM lokaledata")
rows = cursor.fetchall()

print("✅ Updated table contents:")
for row in rows:
    print(row)

conn.close()
