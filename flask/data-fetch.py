import sqlite3

from flask import Flask, request
app = Flask(__name__)

@app.route("/dest/<dest>")
def print_data(dest):
    conn = sqlite3.connect('bart.db')
    c = conn.cursor()
    hour, minute = request.args.get('time', '8:00').split(':')
    try:
        hour = int(hour)
        minute = int(minute)
    except ValueError:
        return "Time formatted incorrectly"
    output = []
    for row in c.execute('select etd, count(*) from etd where dest = ? and hour = ? and minute = ? group by etd',
                         (dest, hour, minute)):
        print row
        output.append(row)
    result = ['hour,minute,etd,sta,dest']
    for row in output:
        result.append(','.join(map(str, row)))
    return '<br>'.join(result)

if __name__ == "__main__":
    app.run(debug=True)
