import sqlite3
db = sqlite3.connect('my_db.db')

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     name TEXT,
     age INTERGER
)
""")
db.commit()
cursor.execute("""INSERT INTO users(name, age) VALUES(?, ?)""", ("test2", 10))
#db.commit()
cursor.execute("""SELECT id,name,age FROM users""")
user1 = cursor.fetchone()
while (user1 != None):
    print(user1)
    user1 = cursor.fetchone()
print(user1)

db.close()
