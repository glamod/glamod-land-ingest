#!/usr/bin/env python

"""
report-land-contents.py
=======================

"""

import os
import re
import subprocess
import shutil

DBHOST = os.environ['DBHOST']
DBUSER = os.environ['DBUSER']
DBNAME = os.environ['DBNAME']

BASE_SQL = 'psql -U {} -h {} {} -f'.format(DBUSER, DBHOST, DNAME).split()
TABLE_TYPES = ['header', 'observations']

REPORT_TYPES = {
    'sub_daily': 0,
    'monthly': 2, 
    'daily': 3
}


LOG = 'report.log'


if not os.environ.get('PGPASSWORD', ''):
    raise Exception('Must set environment var: PGPASSWORD')


PARTS = None


def log(msg, level='INFO'):

    log_msg = '[{}] {}'.format(level, msg)

    with open(LOG, 'a') as writer:
        writer.write(log_msg + '\n')

    print(log_msg)


def run_sql(query):
    args = BASE_SQL + [query]
    resp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [_.strip() for _ in resp.stdout.decode('utf-8').strip().split('\n')]


def get_partition_name(dtype, year, report_type):
    indx = REPORT_TYPES[report_type]
    return 'cdm_v1.{}_{}_land_{}'.format(dtype, year, indx)


def get_count(dtype, year, report_type):
    partition = get_partition_name(dtype, year, report_type)
    resp = run_sql("SELECT COUNT(*) FROM {};".format(partition))

    count = int([re.match('^(\d+)$', resp[2]).groups()[0] for _ in resp][0])
    return count


def get_station_id(report_id):
    try: 
        match = re.match('^(.+)-\d+-\d{4}.*', report_id)
        return match.groups()[0]
    except Exception as err:
        import pdb; pdb.set_trace()


def get_stations_by_partition(dtype, year, report_type):
    partition = get_partition_name(dtype, year, report_type)
    query = "SELECT DISTINCT report_id FROM {};".format(partition)

#    log(query)
    resp = run_sql(query.format(partition))

    match = re.search('(\d+) rows', ' '.join(resp))
    report_ids = []

    if match:
        count = int(match.groups()[0])

        if count > 0:
            report_ids = resp[2:-2]

    stations = set([get_station_id(report_id) for report_id in report_ids])
    return stations


def get_distinct_stations(report_type):

    all_stations = set()

    for year in range(1800, 2019):
        header_partn = get_stations_by_partition('header', year, report_type)
        obs_partn = get_stations_by_partition('observations', year, report_type)

        all_stations.update(header_partn.intersection(obs_partn))

    return sorted(list(all_stations))


def get_partitions_dict():

    d = {}

    for dtype in TABLE_TYPES:

        d.setdefault(dtype, {})
        resp = run_sql("SELECT i.inhrelid::regclass AS child FROM pg_inherits i WHERE i.inhparent = 'cdm_v1.{}_table'::regclass;".format(dtype))
        partitions = [_.strip() for _ in resp if dtype in _]

        for year in range(1800, 2019):
            d[dtype].setdefault(year, {})

            for report_type in REPORT_TYPES:

                partition = get_partition_name(dtype, year, report_type)
                assert(partition in partitions)

                d[dtype][year][report_type] = partition

    return d
 

def report_counts():

    counts = {}
    for dtype in TABLE_TYPES:
        counts[dtype] = {}

        for report_type in REPORT_TYPES:
            counts[dtype][report_type] = 0
    

    for report_type in REPORT_TYPES:
        for year in range(1800, 2019):

            for dtype in TABLE_TYPES: 
                count = get_count(dtype, year, report_type)
                print('{}|{}|{}|{}'.format(dtype, year, report_type, count))

                counts[dtype][report_type] += count

    print('\n-------------------------------------')

    for dtype in TABLE_TYPES:

        for report_type in REPORT_TYPES:
            print('TOTAL Counts|{}|{}|{}'.format(dtype, report_type, counts[dtype][report_type]))


def report_stations():
    
    for report_type in REPORT_TYPES:
        stations = get_distinct_stations(report_type)

        print('\nStations for report_type: {} (count={})'.format(report_type, len(stations)))
        for station in stations:
            print('\t{}'.format(station))


def main():

    global PARTS
    PARTS = get_partitions_dict()
   
    report_counts()
    print()
    report_stations()



if __name__ == '__main__':

    main()
