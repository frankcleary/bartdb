import sqlite3

__author__ = 'Frank'

conn = sqlite3.connect('bart.db')
c = conn.cursor()
c.execute('DROP TABLE etd')
c.execute('CREATE TABLE etd (hour integer, minute integer, etd integer, station text, dest text)')

def parse_time(timestamp):
    try:
        dt = pd.to_datetime(float(timestamp), unit='s')
        return dt.tz_localize('UTC').tz_convert('US/Pacific')
    except AttributeError, ValueError:
        return pd.NaT

plza = pd.read_csv('plza.csv', parse_dates=['time'], date_parser=parse_time)
plza['etd'] = plza['etd'].replace('Leaving', 0).astype(np.float)
plza['time_of_day'] = plza['time'].apply(lambda x: datetime.time(x.time().hour, x.time().minute))

rowdata = []
for row in plza.values:
    rowdata.append([row[-1].hour, row[-1].minute, row[-2], 'plza', row[1]])
c.execute('delete from etd')
c.executemany('INSERT INTO etd VALUES (?, ?, ?, ?, ?)', rowdata)
conn.commit()
conn.close()