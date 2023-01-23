import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('first_user', 'first_password')
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('second_user', 'second_password')
            )

connection.commit()
connection.close()
