from flask import Flask
import sqlite3
from datetime import datetime

app = Flask(__name__)

database = sqlite3.connect('accounts.db')
user_cursor = database.cursor()

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
    app.run(debug=True, host='0.0.0.0', port=5000)