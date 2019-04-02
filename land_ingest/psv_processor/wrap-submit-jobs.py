#!/usr/bin/env python

import subprocess as sp
import os
import sys


FIX_NUMBER = '7'
tmpl = open('submit-jobs.sh.tmpl').read()

RUNNING_DIR = 'jobs-running'
CURRENT = 800

def write_submit_move(number):
    fname = f'submit-tmp-{number:04d}.sh'
    fix_number = FIX_NUMBER

    with open(fname, 'w') as writer:
        writer.write(tmpl.format(**vars()))

    os.system('bsub < {}'.format(fname))

    print('Done: for {}: {}'.format(number, fname))
    os.rename(fname, os.path.join(RUNNING_DIR, fname))


def submit_all(start, end):

    for i in range(start, end + 1):
        if i <= CURRENT:
            print('[WARNING: Ignoring <= {}'.format(CURRENT))
            continue

        write_submit_move(i)


if __name__ == '__main__':

    start, end = [int(arg) for arg in sys.argv[1:3]]
    submit_all(start, end)
