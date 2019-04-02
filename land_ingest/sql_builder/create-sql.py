#!/usr/bin/env python

import re, os, sys, glob
import pandas as pd

from get_partition import get_partition


OUTPUT_DIR = 'sql'
DATA_DIR = '/gws/nopw/j04/c3s311a_lot2/data/beta_fix7/header_table'
HEADER_DIRS_FILE = '/gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/db-loader/beta_fix7_header_dirs.txt'


if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def add_col(df, name='advanced_uncertainty', after='advanced_qc', value='NULL'):
    cols = list(df.columns)
    if name in cols: return

    loc = cols.index(after) + 1
    df.insert(loc, name, value)


def update_obs_file_columns(psv):
    
    df = pd.read_csv(psv, sep='|', dtype=object)
    add_col(df)

    cols = list(df.columns)
    if 'spatial_representativness' in cols:
        df.rename(columns={'spatial_representativness': 'spatial_representativeness'}, inplace=True)

    df = df.replace('', 'NULL')
    df = df.fillna('NULL')
    df.to_csv(psv, sep='|', index=False)


def get_station_id(path):

    basename = os.path.basename(path)
    station_id = re.match('^header_table_BETA_(.+)_\d+$', basename).groups()[0]
    return station_id


def get_dirs_for_first_n_stations(dir_list, n=1000000000):

    IGNORES = []

    stations = set()
    dirs = sorted(dir_list)

    for dr in dirs:

        station_id = get_station_id(dr)

        if station_id in IGNORES: continue

        stations.add(station_id)

        if len(stations) == n:
            break

    resp = []

    for dr in dirs:
        station_id = get_station_id(dr)
        if station_id in stations:
            resp.append(dr)    
 
    return sorted(resp)


def get_sql_file(path):

    if path.find('observations_table') > -1:
        splitter = 'observations_table'
    elif path.find('header_table') > -1:
        splitter = 'header_table'

    sql_file = os.path.join(OUTPUT_DIR, splitter, path.split(splitter + '/')[-1] + '.sql')
    dr = os.path.dirname(sql_file)

    if not os.path.isdir(dr):
        os.makedirs(dr)

    return sql_file


def get_obs_dir(header_dir):

    obs_dir = header_dir.replace('header_table', 'observations_table').replace('observations_table_BETA', 'observation_table_BETA')
    if not os.path.isdir(obs_dir):
        raise Exception('No observations dir: {}'.format(obs_dir))

    return obs_dir


def write_sql(header_dir):

    obs_dir = get_obs_dir(header_dir)
    header_sql = get_sql_file(header_dir)
    obs_sql = get_sql_file(obs_dir)


    for dr, sql in [(header_dir, header_sql), (obs_dir, obs_sql)]:

        print('Writing: {}'.format(sql))

        with open(sql, 'w') as writer:

            writer.write("\cd '{}/'\n".format(dr))

            for fname in os.listdir(dr):
                path = os.path.join(dr, fname)
                if os.path.getsize(path) == 0: 
                    print('[WARNING] Empty PSV file ignored: {}'.format(path))
                    continue

                if path.find('observation') > -1:  update_obs_file_columns(path)
                partition = get_partition(path)

                writer.write("\COPY cdm_v1.{} FROM '{}' WITH CSV HEADER DELIMITER AS '|' NULL AS 'NULL'\n".format(partition, fname))


def create_loader_sql(start, end):
    
    with open(HEADER_DIRS_FILE) as reader:

        for i in range(start - 1):
            reader.readline()

        print('Ignored {} lines'.format(start - 1))

        drs = []
        for i in range(end - start + 1):
            header_dr = reader.readline().strip()
            print('[INFO] Found: {}'.format(header_dr))
            drs.append(header_dr)
            
        print('Creating SQL for {} header files'.format(len(drs)))

        for header_dr in drs:
            print('[INFO] Working on header dir: {}'.format(header_dr))
            write_sql(header_dr)


if __name__ == '__main__':

    start, end = [int(_) for _ in sys.argv[1:3]]
    create_loader_sql(start, end)
