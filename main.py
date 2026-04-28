from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import Calculator
import stocks
import sqlite3
import os
from server.app import create_app, get_db_connection, initialize_database, \
    create_user_account, add_transaction, get_recent_transactions, \
    get_finances, get_finances_full, get_stocks, delete_transaction, \
    add_or_update_stock, set_finances, generate_tests

app = create_app()


"""
==========================================================
Below are the flask pages and very simple test pages (in templates folder, .gitignored)
for making sure we can connect to the database, create users,
display information.
==========================================================
"""
# Home page
# @app.route('/Hackathon/')
# def index():
#     if 'username' in session:
#         return jsonify({'authenticated': True, 'redirect': '/Hackathon/dashboard'}), 200
#     return jsonify({'authenticated': False, 'redirect': '/Hackathon/login'}), 200

# Login page
@app.route('/Hackathon/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        #hashed_password = generate_password_hash(password)
        with get_db_connection() as connection:
            user = connection.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?',
                (username, password),
            ).fetchone()
        if user:
            session['username'] = username
            return jsonify({'message': 'Login successful', 'username': username}), 200
        else:
            return jsonify({'error': 'Invalid username or password.'}), 401
    return jsonify({'message': 'Login endpoint ready'}), 200

# Registration page
@app.route('/Hackathon/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        if not username or not password or not email:
            return jsonify({'error': 'All fields are required.'}), 400
        else:
            result = create_user_account(username, password, email)
            if result is None:
                return jsonify({'error': 'Username or email already taken.'}), 409
            else:
                return jsonify({'message': 'Account created! Please log in.'}), 201
    return jsonify({'message': 'Register endpoint ready'}), 200

# Users dashboard page. If this is accessed without being logged in, 
# it returns an unauthorized error.
@app.route('/Hackathon/api/dashboard')
def dashboard():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
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
        finance_data = [{'label': label, 'value': value} for label, value in zip(finance_labels, finances)]

    return jsonify({
        'username': username,
        'transactions': transactions,
        'stocks': stocks,
        'finance_data': finance_data,
        'finances_full': finances_full,
    }), 200

# Logout endpoint. Removes the username from the session.
@app.route('/Hackathon/api/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Option to add a transaction. If the user is not logged in, it redirects to the login page.
# flash messages are used to display success or error messages to the user after attempting 
# to add a transaction.
@app.route('/Hackathon/api/add_transaction', methods=['POST'])
def route_add_transaction():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    username = session['username']
    name = request.form.get('transaction_name', '').strip()
    amount = request.form.get('amount', '').strip()
    if not name or not amount:
        return jsonify({'error': 'Transaction name and amount are required.'}), 400
    else:
        try:
            transaction_id = add_transaction(username, name, float(amount))
            return jsonify({'message': f'Transaction "{name}" added.', 'transaction_id': transaction_id}), 201
        except (ValueError, sqlite3.Error) as e:
            return jsonify({'error': f'Error adding transaction: {e}'}), 400

# Option to delete a transaction
@app.route('/Hackathon/api/delete_transaction', methods=['POST'])
def route_delete_transaction():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    username = session['username']
    transaction_id = request.form.get('transaction_id', '').strip()
    if not transaction_id:
        return jsonify({'error': 'Transaction ID is required.'}), 400
    else:
        try:
            delete_transaction(username, int(transaction_id))
            return jsonify({'message': 'Transaction deleted.'}), 200
        except (ValueError, sqlite3.Error) as e:
            return jsonify({'error': f'Error deleting transaction: {e}'}), 400


# Update the users finances
@app.route('/Hackathon/api/update_finances', methods=['POST'])
def route_update_finances():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
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
        return jsonify({'message': 'Finances updated.'}), 200
    except (ValueError, sqlite3.Error) as e:
        return jsonify({'error': f'Error updating finances: {e}'}), 400


# Update the users stocks records.
# Only stock_symbol and count are required — name and price are looked up
# automatically from the stocks.py CSV data.
@app.route('/Hackathon/api/add_stock', methods=['POST'])
def route_add_stock():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    username = session['username']
    stock_symbol = request.form.get('stock_symbol', '').strip().upper()
    count = request.form.get('count', '').strip()
    if not stock_symbol or not count:
        return jsonify({'error': 'Stock symbol and count are required.'}), 400
    try:
        info = stocks.getStockInfo(stock_symbol)
        if info is None:
            return jsonify({'error': f'Stock symbol {stock_symbol} not found in database.'}), 404
        stock_name = info['name']
        current_price = info['current_price'] or 0.0
        add_or_update_stock(username, stock_name, stock_symbol, current_price, int(count))
        return jsonify({
            'message': f'Stock {stock_symbol} added/updated.',
            'stock': {
                'stock_name': stock_name,
                'stock_symbol': stock_symbol,
                'current_price': current_price,
                'count': int(count),
            },
        }), 201
    except (ValueError, sqlite3.Error) as e:
        return jsonify({'error': f'Error adding stock: {e}'}), 400


# Look up a stock by symbol — returns name, beta, price-to-book, and current price.
@app.route('/Hackathon/api/lookup_stock', methods=['GET'])
def route_lookup_stock():
    symbol = request.args.get('symbol', '').strip().upper()
    if not symbol:
        return jsonify({'error': 'Symbol query parameter is required.'}), 400
    info = stocks.getStockInfo(symbol)
    if info is None:
        return jsonify({'error': f'Stock symbol {symbol} not found.'}), 404
    return jsonify(info), 200


# Refresh current prices for every stock in the logged-in user's portfolio
# using the data from stocks.py / stocks.csv.
@app.route('/Hackathon/api/update_stock_prices', methods=['POST'])
def route_update_stock_prices():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    username = session['username']
    user_stocks = get_stocks(username)
    if not user_stocks:
        return jsonify({'message': 'No stocks in portfolio to update.'}), 200

    updated = []
    not_found = []
    for s in user_stocks:
        info = stocks.getStockInfo(s['stock_symbol'])
        if info and info['current_price'] is not None:
            try:
                add_or_update_stock(
                    username,
                    info['name'],
                    s['stock_symbol'],
                    info['current_price'],
                    s['count'],
                )
                updated.append({
                    'stock_symbol': s['stock_symbol'],
                    'old_price': s['current_price'],
                    'new_price': info['current_price'],
                })
            except (ValueError, sqlite3.Error):
                not_found.append(s['stock_symbol'])
        else:
            not_found.append(s['stock_symbol'])

    return jsonify({
        'message': f'{len(updated)} stock(s) updated.',
        'updated': updated,
        'not_found': not_found,
    }), 200

if __name__ == '__main__':
    initialize_database()
    generate_tests()
    app.run(debug=True, host='0.0.0.0', port=5003)