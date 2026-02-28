from flask import Flask
import sqlite3

app = Flask(__name__)

DB_PATH = 'accounts.db'


def get_db_connection():
   connection = sqlite3.connect(DB_PATH)
   connection.row_factory = sqlite3.Row
   connection.execute('PRAGMA foreign_keys = ON;')
   return connection

# Create tables if they dont exist already (rare usage)
def initialize_database():
   with get_db_connection() as connection:
      connection.executescript(
         '''
         CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
         );

         CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_name TEXT NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
         );

         CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stock_name TEXT NOT NULL,
            stock_symbol TEXT NOT NULL,
            current_price REAL NOT NULL,
            count INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE (user_id, stock_symbol)
         );

         CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            income REAL NOT NULL,
            rent REAL NOT NULL,
            groceries REAL NOT NULL,
            utilities REAL NOT NULL,
            transportation REAL NOT NULL,
            entertainment REAL NOT NULL,
            subscriptions REAL NOT NULL,
            other REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
         );

         CREATE INDEX IF NOT EXISTS idx_transactions_user_date
         ON transactions(user_id, transaction_date DESC);
         '''
      )


# method. Adds user into the users table.
# user unique ID is auto-incremented. Creation timestamp is automatically generated.
def create_user_account(username, password, email):
   with get_db_connection() as connection:
      try:
         cursor = connection.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, password, email),
         )
         return cursor.lastrowid
      except sqlite3.IntegrityError:
         return None


# Pass through username and the connection object
def _get_user_id(connection, username):
   row = connection.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
   return None if row is None else row['id']


# Inserts a new transaftion
# --> get_db_connection() gets the connection object
# --> _get_user_id() gets the user id from the connection object. Keeps user and connection tied 
#                    together, and allows us to reuse the connection for multiple queries if needed.
def add_transaction(username, transaction_name, amount, transaction_date=None):
   with get_db_connection() as connection:
      user_id = _get_user_id(connection, username)
      # user not found -> shouldn't happen
      if user_id is None:
         raise ValueError('User not found')

      # transaction_date is optional. If not provided, 
      # it will default to the current timestamp in the database.
      if transaction_date is None:
         cursor = connection.execute(
            '''
            INSERT INTO transactions (user_id, transaction_name, amount)
            VALUES (?, ?, ?)
            ''',
            (user_id, transaction_name, amount),
         )
      # transaction_date provided -> use the provided date instead of the default timestamp
      else:
         cursor = connection.execute(
            '''
            INSERT INTO transactions (user_id, transaction_name, amount, transaction_date)
            VALUES (?, ?, ?, ?)
            ''',
            (user_id, transaction_name, amount, transaction_date),
         )
      return cursor.lastrowid


# Display the last 1000 transactions for a user, sorted by transaction date (most recent first) 
# and then by transaction ID in the scenario where multiple transactions have the same date. 
def get_recent_transactions(username, limit=1000):
   safe_limit = max(1, min(int(limit), 1000))
   with get_db_connection() as connection:
      rows = connection.execute(
         '''
         SELECT t.id, t.transaction_name, t.transaction_date, t.amount
         FROM transactions AS t
         JOIN users AS u ON u.id = t.user_id
         WHERE u.username = ?
         ORDER BY t.transaction_date DESC, t.id DESC
         LIMIT ?
         ''',
         (username, safe_limit),
      ).fetchall()
   return [dict(row) for row in rows]

# Home page --> Welcome screen, description of our services, links to
# login/signup, Current stock tickers, calculators, and homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Login Page --> Prompt for user name and password, or to sign up
# if they do not have an account. Keep general links at the top of the page.

# Calculators page --> Various calculators - Delegated to sabian.

# Stock tickers page -- > Display current stock tickers, with links to more detailed information about
# each stock. Delegated to John

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)