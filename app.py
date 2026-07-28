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
    if not DATABASE_URL:
        return "Database connection failed: DATABASE_URL is not configured", 500

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        return "Database connection successful"

    except Exception as e:
        return f"Database connection failed: {e}", 500

    finally:
        if conn is not None:
            conn.close()


@app.route("/db_create")
def db_create():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Basketball(
                First varchar(255),
                Last varchar(255),
                City varchar(255),
                Name varchar(255),
                Number int
            );
        """)

        conn.commit()

        return "Basketball Table Created"

    except Exception as e:
        return f"Error creating table: {e}"

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()           