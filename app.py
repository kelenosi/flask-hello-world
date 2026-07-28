import os

import psycopg2

from flask import Flask
app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def hello_world():
    return 'Hello World from Kevin B in 3308'
