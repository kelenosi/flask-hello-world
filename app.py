import os

import psycopg2

from flask import Flask
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


@app.route('/')
def hello_world():
    return 'Hello World from Kevin B in 3308'


@app.route("/db_test")
def db_test():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return "Database connection successful"
    except Exception as e:
        return f"Database connection failed: {e}"
    finally:
        if conn is not None:
            conn.close()