import sqlite3
import time

from flask import Flask, request, g

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

@app.route("/dest/<dest>")
def print_data(dest):
    c = get_db().cursor()
    hour, minute = request.args.get('time', '8:00').split(':')
    try:
        hour = int(hour)
        minute = int(minute)
    except ValueError:
        return "Time formatted incorrectly"
    output = []
    for row in c.execute('select etd, count(*) from etd where dest = ? and hour = ? and minute = ? group by etd',
                         (dest, hour, minute)):
        output.append(','.join(map(str, row)))
    return '<br>'.join(output)

if __name__ == "__main__":
    app.run(debug=True)
