#!/usr/bin/env python

import os
import subprocess
import shutil


DBHOST = os.environ['DBHOST']
DBUSER = os.environ['DBUSER']
DBNAME = os.environ['DBNAME']

BASE_SQL = 'psql -U {} -h {} {} -f'.format(DBUSER, DBHOST, DNAME).split() 

LOG_DIR = 'logged-sqls'


if not os.environ.get('PGPASSWORD', ''):
    raise Exception('Must set environment var: PGPASSWORD')


def process_result(sql_file, resp):

    if not resp.stderr:
        state = 'SUCCESS'
        print('[INFO] successfully ran {}'.format(sql_file))

    else:
        state = 'ERROR'
        print('[ERROR] failed to run   {}'.format(sql_file))

    dr = os.path.join(LOG_DIR, state)
    if not os.path.isdir(dr): os.makedirs(dr)

    shutil.copy(sql_file, os.path.join(dr, sql_file))

    return state == 'SUCCESS'


def run_sql(sql_file):

    args = BASE_SQL + [sql_file]
    resp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process_result(sql_file, resp)

    return result


def main():

    sql_files = ('good.sql', 'bad.sql')

    successes = 0

    for count, sql_file in enumerate(sql_files):

        result = run_sql(sql_file) 
        if result: successes += 1        

    print('\n[INFO] Total files processed: {}'.format(count))
    print('[INFO] Successes: {}'.format(successes))
    print('[INFO] Failures:  {}'.format(count - successes))


if __name__ == '__main__':

    main()
