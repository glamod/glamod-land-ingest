#!/usr/bin/env python

import os, re, sys


def get_partition(path):

    if 'header_table' in path:
        ftype = 'header'
    elif 'observations_table' in path:
        ftype = 'observations'
    else:
        raise Exception('Cannot work out file type: {}'.format(ftype))

    fname = os.path.basename(path)
    year = fname[-8:-4]

    if not re.match('\d{4}', year):
        raise Exception('Cannot work out year: {}'.format(year))

    if '/sub_daily' in path:
        report_type = '0'
    elif '/monthly' in path:
        report_type = '2'
    elif '/daily' in path:
        report_type = '3'
    else:
        raise Exception('Cannot work out report_type: {}'.format(year))

    partition = '{}_{}_land_{}'.format(ftype, year, report_type)
    return partition
    

if __name__ == '__main__':

    print(get_partition(sys.argv[1]))
