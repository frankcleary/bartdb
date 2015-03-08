import sqlite3
import time
import logging

from flask import Flask, request, g

logging.basicConfig(filename='bartdb.log', level=logging.INFO)

DATABASE = 'bart.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    return '<br>'.join(str(row) for row in execute_query(
        """SELECT *
           FROM etd
           LIMIT 1000"""
    ))


@app.route("/schema")
def view_schema():
    return '<br>'.join(str(row) for row in execute_query(
        """pragma table_info('etd')"""
    ))


@app.route("/")
def print_data():
    """Respond to a query of the format:
    myapp/?dest=Fremont&time=600&station=plza&day=0
    with ETD data for the time and location specified in the query"""
    start_time = time.time()
    cur = get_db().cursor()
    try:
        minute_of_day = int(request.args.get('time'))
    except ValueError:
        return "Time must be an integer"
    station = request.args.get('station')
    print minute_of_day
    day = request.args.get('day')
    dest = request.args.get('dest')
    result = execute_query(
        """SELECT etd, count(*)
           FROM etd
           WHERE dest = ? AND minute_of_day = ?
                 AND station = ? AND day_of_week = ?
           GROUP BY etd""",
        (dest, minute_of_day, station, day)
    )
    str_rows = [','.join(map(str, row)) for row in result]
    query_time = time.time() - start_time
    logging.info("executed query in %s" % query_time)
    cur.close()
    header = 'etd,count\n'
    return header + '\n'.join(str_rows)

if __name__ == "__main__":
    app.run()
