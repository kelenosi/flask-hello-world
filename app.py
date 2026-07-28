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


@app.route("/db_insert")
def db_insert():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Basketball (First, Last, City, Name, Number)
            VALUES
            ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
            ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
            ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
            ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
            ('Kevin', 'Bell', 'CU Boulder', 'Buffaloes', 3308);
        """)

        conn.commit()
        return "Basketball Table Populated"

    except Exception as e:
        if conn is not None:
            conn.rollback()
        return f"Error populating table: {e}", 500

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


@app.route("/db_select")
def db_select():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT * FROM Basketball;")
        records = cur.fetchall()

        html = "<html><body>"
        html += "<h2>Basketball Table</h2>"
        html += "<table border='1'>"
        html += (
            "<tr>"
            "<th>First</th>"
            "<th>Last</th>"
            "<th>City</th>"
            "<th>Name</th>"
            "<th>Number</th>"
            "</tr>"
        )

        for row in records:
            html += "<tr>"
            for value in row:
                html += f"<td>{value}</td>"
            html += "</tr>"

        html += "</table>"
        html += "</body></html>"

        return html

    except Exception as e:
        return f"Error retrieving data: {e}", 500

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

