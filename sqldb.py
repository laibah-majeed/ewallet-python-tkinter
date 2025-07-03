import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect('ewallet.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    phone TEXT UNIQUE,
    balance REAL
)
''')

# Delete existing data
cursor.execute("DELETE FROM users")

# Insert sample user data
cursor.execute("INSERT INTO users (username, phone, balance) VALUES (?, ?, ?)", ('Ali', '03123456789', 1000.0))
cursor.execute("INSERT INTO users (username, phone, balance) VALUES (?, ?, ?)", ('Fatima', '03987654321', 800.0))
cursor.execute("INSERT INTO users (username, phone, balance) VALUES (?, ?, ?)", ('Usman', '03001234567', 1500.0))
cursor.execute("INSERT INTO users (username, phone, balance) VALUES (?, ?, ?)", ('Ayesha', '03211234567', 500.0))
conn.commit()

# Test case: Deposit Rs.500 to Ali (id = 1)
cursor.execute("UPDATE users SET balance = balance + 500 WHERE id = 1")

# Test case: Fatima sends Rs.300 to Ayesha
cursor.execute("UPDATE users SET balance = balance - 300 WHERE id = 2")  # Fatima
cursor.execute("UPDATE users SET balance = balance + 300 WHERE id = 4")  # Ayesha

# Test case: Usman pays Electricity Bill Rs.700
cursor.execute("UPDATE users SET balance = balance - 700 WHERE id = 3")

# Test case: Ayesha buys Mobile Package Rs.200
cursor.execute("UPDATE users SET balance = balance - 200 WHERE id = 4")

# Retrieve and print final user balances
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()
