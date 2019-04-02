#!/usr/bin/env python

import os
import subprocess
import shutil

DBHOST = os.environ['DBHOST']
DBUSER = os.environ['DBUSER']
DBNAME = os.environ['DBNAME']

BASE_SQL = 'psql -U {} -h {} {} -f'.format(DBUSER, DBHOST, DNAME).split()


LOGGED_SCRIPTS = 'logged-sqls'
LOG = 'sql-loading.log'


if not os.environ.get('PGPASSWORD', ''):
    raise Exception('Must set environment var: PGPASSWORD')


def log(msg, level='INFO'):

    log_msg = '[{}] {}'.format(level, msg)

    with open(LOG, 'a') as writer:
        writer.write(log_msg + '\n')

    print(log_msg)


def process_result(sql_file, resp):

    if not resp.stderr:
        state = 'SUCCESS'
        log('Successfully ran: {}'.format(sql_file))

    else:
        state = 'ERROR'
        log('Failed to run:    {}'.format(sql_file), 'ERROR')

    dr = os.path.join(LOGGED_SCRIPTS, state)
    if not os.path.isdir(dr): os.makedirs(dr)

    shutil.copy(sql_file, os.path.join(dr, os.path.basename(sql_file)))

    return state == 'SUCCESS'


def run_sql(sql_file):

    args = BASE_SQL + [sql_file]
    resp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = process_result(sql_file, resp)

    return result


def main():

    args = ['find', 'sql', '-name', '*.sql']
    resp = subprocess.run(args, stdout=subprocess.PIPE)
    sql_files = sorted([str(_, encoding='utf-8') for _ in resp.stdout.split()])

    if resp.returncode != 0 or len(sql_files) < 150:
        raise Exception('Could not get list of input sql files, found: {}'.format(sql_files))

    successes = 0

    for count, sql_file in enumerate(sql_files):

        result = run_sql(sql_file) 
        if result: successes += 1

    log('---------------------------------')
    log('Total files processed: {}'.format(count + 1))
    log('Successes: {}'.format(successes))
    log('Failures:  {}'.format(count + 1 - successes))


if __name__ == '__main__':

    main()
