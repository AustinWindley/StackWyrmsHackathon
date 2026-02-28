from flask import Flask
import sqlite3
from datetime import datetime

app = Flask(__name__)

database = sqlite3.connect('accounts.db')
user_cursor = database.cursor()

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)