activate_this = '/home/ubuntu/pelicanenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/bartdb")

from bartdb import app as application