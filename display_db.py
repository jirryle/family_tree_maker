import sqlite3

DATABASE_NAME = "family_tree.db"

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

cursor.execute('SELECT * FROM relatives')  # Select all columns
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Gender: {row[2]}, Birth Date: {row[3]}, Photo URL: {row[4]}, Father ID: {row[5]}, Mother ID: {row[6]}")

conn.close()
