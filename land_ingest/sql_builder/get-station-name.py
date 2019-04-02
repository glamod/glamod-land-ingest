#!/usr/bin/env python

import re
import os
import sys

fpath = sys.argv[1]
filename = os.path.basename(fpath)

station_id = re.match('^header_table_BETA_(.+)_\d+$', filename).groups()[0]
print(station_id)
