from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Having issues finding accounts.db. Changed this to use os path library for documentation
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accounts.db')

# Sets up the database connections
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON;')
    return connection

# Create tables if they dont exist already (rare usage)
#
# The create_idx_transactions_user_date index is added to try to 
# optimize finding transactions for a user sorted by date, 
# which is a common thing we do
"""
Users
    - id
    - username
    - password
    - email
    - creation timestamp
Transactions
    - id
    - user_id
    - transaction_name
    - transaction_date
    - amount
Stocks
    - id
    - user_id
    - stock_name
    - stock_symbol
    - current_price
    - count
Finances
    - id
    - user_id
    - hourly_income
    - hours_per_week
    - rent
    - groceries
    - utilities
    - transportation
"""
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
                hourly_income REAL NOT NULL,
                hours_per_week REAL NOT NULL,
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

# A function to return the users current finances in a list of floats.
# returns them as a list of floats in the following order:
# [rent, groceries, utilities, transportation, entertainment, subscriptions, other]
def get_finances(username):
    with get_db_connection() as connection:
        row = connection.execute(
            '''
            SELECT rent, groceries, utilities, transportation, entertainment, subscriptions, other
            FROM finances AS f
            JOIN users AS u ON u.id = f.user_id
            WHERE u.username = ?
            ''',
            (username,),
        ).fetchone()
    return list(row) if row else None


# Returns all finance fields for a user as a dict (for form pre-fill).
def get_finances_full(username):
    with get_db_connection() as connection:
        row = connection.execute(
            '''
            SELECT f.hourly_income, f.hours_per_week, f.rent, f.groceries,
                   f.utilities, f.transportation, f.entertainment,
                   f.subscriptions, f.other
            FROM finances AS f
            JOIN users AS u ON u.id = f.user_id
            WHERE u.username = ?
            ''',
            (username,),
        ).fetchone()
    return dict(row) if row else None


# Returns all stocks for a user as a list of dicts.
def get_stocks(username):
    with get_db_connection() as connection:
        rows = connection.execute(
            '''
            SELECT s.stock_name, s.stock_symbol, s.current_price, s.count
            FROM stocks AS s
            JOIN users AS u ON u.id = s.user_id
            WHERE u.username = ?
            ORDER BY s.stock_symbol
            ''',
            (username,),
        ).fetchall()
    return [dict(row) for row in rows]


# Deletes a specific transaction by its ID, but only if it belongs to the given user.
# takes in the username of the connected user and the ID of the transaction.
def delete_transaction(username, transaction_id):
    with get_db_connection() as connection:
        user_id = _get_user_id(connection, username)
        if user_id is None:
            raise ValueError('User not found')

        cursor = connection.execute(
            'DELETE FROM transactions WHERE id = ? AND user_id = ?',
            (transaction_id, user_id),
        )
        if cursor.rowcount == 0:
            raise ValueError('Transaction not found')
        return True


# A function to add a stock or change how many you have registered to your account.
# get_db_connection() gets the connection object
# _get_user_id() gets the user id from the connection object.
def add_or_update_stock(username, stock_name, stock_symbol, current_price, count):
    with get_db_connection() as connection:
        user_id = _get_user_id(connection, username)
        if user_id is None:
            raise ValueError('User not found')

        cursor = connection.execute(
            '''
            INSERT INTO stocks (user_id, stock_name, stock_symbol, current_price, count)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, stock_symbol)
            DO UPDATE SET
                stock_name = excluded.stock_name,
                current_price = excluded.current_price,
                count = excluded.count
            ''',
            (user_id, stock_name, stock_symbol, current_price, count),
        )
        return cursor.lastrowid

# A function to set finances for a user. 
# If the user already has finances set, it will update the existing 
# entry for it instead of duplicating it.
def set_finances(
    username,
    hourly_income,
    hours_per_week,
    rent,
    groceries,
    utilities,
    transportation,
    entertainment,
    subscriptions,
    other,
):
    with get_db_connection() as connection:
        user_id = _get_user_id(connection, username)
        if user_id is None:
            raise ValueError('User not found')

        # If the uiser already has finances set, update the existing entry instead of creating a new one.
        # INSERT - into finances
        # VALUES - the values to insert
        # ON CONFLICT(user_id) - if there is a conflict on the user_id (i.e. the user already has finances set)
        # DO UPDATE SET - update the existing entry with the new values
        cursor = connection.execute(
            '''
            INSERT INTO finances (
                user_id,
                hourly_income,
                hours_per_week,
                rent,
                groceries,
                utilities,
                transportation,
                entertainment,
                subscriptions,
                other
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET
                hourly_income = excluded.hourly_income,
                hours_per_week = excluded.hours_per_week,
                rent = excluded.rent,
                groceries = excluded.groceries,
                utilities = excluded.utilities,
                transportation = excluded.transportation,
                entertainment = excluded.entertainment,
                subscriptions = excluded.subscriptions,
                other = excluded.other
            ''',
            (
                user_id,
                hourly_income,
                hours_per_week,
                rent,
                groceries,
                utilities,
                transportation,
                entertainment,
                subscriptions,
                other,
            ),
        )
        return cursor.lastrowid

# Simple test case to ensure databases are working correctly.
#  Creates 3 test users with a variety of transactions, stocks, and finances.
# Finances format: (hourly_income, hours_per_week, rent, groceries, utilities, 
#                   transportation, entertainment, subscriptions, other)
def generate_tests():
    test_users = [
        {
            'username': 'test_dragon',
            'password': 'derg_pw_123',
            'email': 'dragon@wyrms.com',
            'transactions': [
                ('Paycheck', 1450.00),
                ('Rent Payment', -900.00),
                ('Groceries', -127.45),
                ('Coffee', -6.75),
                ('Electric Bill', -72.10),
            ],
            'stocks': [
                ('Apple Inc.', 'AAPL', 191.32, 10),
                ('NVIDIA Corp.', 'NVDA', 789.50, 3),
            ],
            'finances': (35.00, 40.0, 900.0, 420.0, 140.0, 120.0, 150.0, 45.0, 80.0),
        },
        {
            'username': 'test_wyrm',
            'password': 'wyrm_pw_123',
            'email': 'wyrm@dragons.com',
            'transactions': [
                ('Freelance Invoice', 820.00),
                ('Internet', -64.99),
                ('Gas', -58.20),
                ('Restaurant', -48.00),
                ('Movie Tickets', -29.50),
                ('Book Sale', 44.00),
            ],
            'stocks': [
                ('Microsoft Corp.', 'MSFT', 421.08, 6),
                ('Tesla Inc.', 'TSLA', 203.41, 2),
                ('Vanguard S&P 500 ETF', 'VOO', 481.27, 4),
            ],
            'finances': (29.50, 32.0, 700.0, 300.0, 90.0, 85.0, 110.0, 20.0, 50.0),
        },
        {
            'username': 'JustDragon',
            'password': 'dragonPass123',
            'email': 'JDragon@example.com',
            'transactions': [
                ('Scholarship Disbursement', 2100.00),
                ('Tuition', -1600.00),
                ('Campus Dining', -90.25),
                ('Bus Pass', -35.00),
                ('Textbooks', -220.40),
                ('Part-time Shift', 180.00),
                ('Streaming Subscription', -14.99),
            ],
            'stocks': [
                ('Amazon.com Inc.', 'AMZN', 176.54, 1),
            ],
            'finances': (18.00, 18.0, 500.0, 260.0, 55.0, 40.0, 95.0, 15.0, 35.0),
        },
    ]

    # Clear existing test users (creates conflicts for testing)
    with get_db_connection() as connection:
        for user in test_users:
            connection.execute('DELETE FROM users WHERE username = ?', (user['username'],))

    # Create test users and populate their transactions, stocks, and finances
    for user in test_users:
        create_user_account(user['username'], user['password'], user['email'])

        for transaction_name, amount in user['transactions']:
            add_transaction(user['username'], transaction_name, amount)

        for stock_name, stock_symbol, current_price, count in user['stocks']:
            add_or_update_stock(user['username'], stock_name, stock_symbol, current_price, count)

        set_finances(user['username'], *user['finances'])

    # Return summary of created test data for confirmation
    return {
        'users_created': len(test_users),
        'transactions_created': sum(len(user['transactions']) for user in test_users),
        'stocks_created': sum(len(user['stocks']) for user in test_users),
        'finances_created': len(test_users),
    }


"""
==========================================================
Below are the flask pages and very simple test pages (in templates folder, .gitignored)
for making sure we can connect to the database, create users,
display information.
==========================================================
"""
# Home page
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login page
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        with get_db_connection() as connection:
            user = connection.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?',
                (username, password),
            ).fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Registration page
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        if not username or not password or not email:
            flash('All fields are required.')
        else:
            result = create_user_account(username, password, email)
            if result is None:
                flash('Username or email already taken.')
            else:
                flash('Account created! Please log in.')
                return redirect(url_for('login'))
    return render_template('register.html')

# Users dashboard page. If this is accessed without being logged in, 
# it redirects to the login page.
@app.route('/api/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    transactions = get_recent_transactions(username, limit=50)
    stocks = get_stocks(username)
    finances = get_finances(username)
    finances_full = get_finances_full(username)

    # Order: rent, groceries, utilities, transportation, 
    #        entertainment, subscriptions, other
    finance_labels = [
        'Rent', 'Groceries', 'Utilities', 'Transportation',
        'Entertainment', 'Subscriptions', 'Other',
    ]
    finance_data = None
    if finances:
        finance_data = list(zip(finance_labels, finances))

    # This is where we pass all the data to the dashboard template to be rendered.
    return render_template(
        'dashboard.html',
        username=username,
        transactions=transactions,
        stocks=stocks,
        finance_data=finance_data,
        finances_full=finances_full,
    )

# Logout page. Removes the username from the session 
# and redirects to the login page.
@app.route('/api/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Option to add a transaction. If the user is not logged in, it redirects to the login page.
# flash messages are used to display success or error messages to the user after attempting 
# to add a transaction.
@app.route('/api/add_transaction', methods=['POST'])
def route_add_transaction():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    name = request.form.get('transaction_name', '').strip()
    amount = request.form.get('amount', '').strip()
    if not name or not amount:
        flash('Transaction name and amount are required.')
    else:
        try:
            add_transaction(username, name, float(amount))
            flash(f'Transaction "{name}" added.')
        except (ValueError, sqlite3.Error) as e:
            flash(f'Error adding transaction: {e}')
    return redirect(url_for('dashboard'))

# Option to delete a transaction
@app.route('/api/delete_transaction', methods=['POST'])
def route_delete_transaction():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    transaction_id = request.form.get('transaction_id', '').strip()
    if not transaction_id:
        flash('Transaction ID is required.')
    else:
        try:
            delete_transaction(username, int(transaction_id))
            flash('Transaction deleted.')
        except (ValueError, sqlite3.Error) as e:
            flash(f'Error deleting transaction: {e}')
    return redirect(url_for('dashboard'))


# Update the users finances page
@app.route('/api/update_finances', methods=['POST'])
def route_update_finances():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    try:
        set_finances(
            username,
            float(request.form.get('hourly_income', 0)),
            float(request.form.get('hours_per_week', 0)),
            float(request.form.get('rent', 0)),
            float(request.form.get('groceries', 0)),
            float(request.form.get('utilities', 0)),
            float(request.form.get('transportation', 0)),
            float(request.form.get('entertainment', 0)),
            float(request.form.get('subscriptions', 0)),
            float(request.form.get('other', 0)),
        )
        flash('Finances updated.')
    except (ValueError, sqlite3.Error) as e:
        flash(f'Error updating finances: {e}')
    return redirect(url_for('dashboard'))


# Update the users stocks records
@app.route('/api/add_stock', methods=['POST'])
def route_add_stock():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    stock_name = request.form.get('stock_name', '').strip()
    stock_symbol = request.form.get('stock_symbol', '').strip().upper()
    current_price = request.form.get('current_price', '').strip()
    count = request.form.get('count', '').strip()
    if not stock_name or not stock_symbol or not current_price or not count:
        flash('All stock fields are required.')
    else:
        try:
            add_or_update_stock(username, stock_name, stock_symbol, float(current_price), int(count))
            flash(f'Stock {stock_symbol} added/updated.')
        except (ValueError, sqlite3.Error) as e:
            flash(f'Error adding stock: {e}')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    initialize_database()
    generate_tests()
    app.run(debug=False, host='0.0.0.0', port=5000)