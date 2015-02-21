#!/home/ubuntu/anaconda/bin/python
import sqlite3
import urllib2
import time
import datetime
import pytz

STATIONS = ['PLZA', 'MONT']
URLBASE = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key=MW9S-E7SL-26DU-VV8V'

result = []
for sta in STATIONS:
    dt = datetime.datetime.now(pytz.timezone('US/Pacific'))
    result.append((
        time.time(),
        60*dt.hour + dt.minute,
        sta,
        urllib2.urlopen(URLBASE.format(sta)).read()))

conn = sqlite3.connect('/home/ubuntu/bart-data/bart-data.db')
c = conn.cursor()
c.executemany('INSERT INTO etd VALUES (?,?,?,?)', result)
conn.commit()
conn.close()
    
