import sqlite3

# Connect to the database or create a new one
connection = sqlite3.connect('db.sqlite3')

# Get a cursor object to execute SQL commands
cursor = connection.cursor()

# Create a table for the User model (you can add more fields as needed)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()
