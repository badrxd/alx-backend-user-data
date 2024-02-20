import sqlite3

# Connect to the SQLite database file
conn = sqlite3.connect('a.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a simple query (replace with your own SQL)
cursor.execute('SELECT * FROM users;')

# Fetch the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()
