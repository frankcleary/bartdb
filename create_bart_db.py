"""
Read in BART ETD data from files and write to SQL.
"""
import sqlite3

import numpy as np
import pandas as pd

DATABASE = 'bart.db'
FILES = ['plza.csv', 'mont.csv']


def define_weekday(dt_index):
    """Return an array with 0's for elements of dt_series that are on a
    weekday, 1 if a Saturday, 2 if a Sunday.

    :param obs_time: DatetimeIndex
    """
    result = np.zeros(len(dt_index))
    weekdays = dt_index.weekday
    result[weekdays == 5] = 1
    result[weekdays == 6] = 2
    return result


def parse_data(file_name, chunksize=1E5):
    """Return a dataframe from csv file, with times parsed.

    :param file_name: csv file
    :return: DataFrame from csv file
    """
    return pd.read_csv(file_name, names=['time','dest','dir','len','etd'],
                       header=None, chunksize=chunksize)


def time2minute_of_day(dt_index):
    """Return the minute of day (12:00 midnight = 0) for each time in
    dt_series.

    :param obs_time: DatetimeIndex
    """
    return dt_index.hour * 60 + dt_index.minute


def csv2sql(conn, files):
    """Read in BART ETD data from files and write that data to the SQL database
    accessed by conn.

    :param conn: SQL database connection
    :param files: the files to read data from
    """
    output_cols = ['dest', 'dir', 'etd', 'station', 'minute_of_day',
                   'day_of_week']
    conn.execute("DROP TABLE IF EXISTS etd")
    for sta_file in files:
        for i, df in enumerate(parse_data(sta_file)):
            print 'Working on chunk {} of {}'.format(i, sta_file)
            dt_index = (pd.DatetimeIndex(pd.to_datetime(df['time'], unit='s'))
                        .tz_localize('UTC')
                        .tz_convert('US/Pacific'))
            df['station'] = sta_file.split('.')[0]
            df['day_of_week'] = define_weekday(dt_index)
            df['etd'] = df['etd'].replace('Leaving', 0).dropna().astype(np.int)
            df['minute_of_day'] = time2minute_of_day(dt_index)
            df[output_cols].to_sql('etd', conn, index=False, if_exists='append')

    conn.cursor().execute(
        """CREATE INDEX idx1
        ON etd(station, dest, minute_of_day, day_of_week)
        """
        )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE)
    csv2sql(conn, FILES)
