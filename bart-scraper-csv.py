#!/home/ubuntu/anaconda/bin/python
import urllib2
import time
import datetime
import pytz
import xml.etree.ElementTree as ET

STATIONS = ['plza', 'mont']
URLBASE = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key=MW9S-E7SL-26DU-VV8V'

for sta in STATIONS:
    lines = []
    timestamp = time.time()
    root = ET.fromstring(urllib2.urlopen(URLBASE.format(sta)).read())
    for etd in root.findall('station/etd'):
        lines.append(str(timestamp) + "," + \
                     etd.findtext('destination') + "," + \
                     etd.findtext('estimate/direction') + "," + \
                     etd.findtext('estimate/length') + "," + \
                     etd.findtext('estimate/minutes')
                     )
    with open('/home/ubuntu/bart-data/' + sta + '.csv', 'a') as f:
        f.write('\n'.join(lines) + '\n')
 
