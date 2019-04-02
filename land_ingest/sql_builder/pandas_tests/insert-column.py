#!/usr/bin/env python

import sys
import pandas as pd


def add_col(df, name='advanced_uncertainty', after='advanced_qc', value='NULL'):
    loc = list(df.columns).index(after) + 1
    df.insert(loc, name, value)


def update_file(psv):
    df = pd.read_csv(psv, sep='|', dtype=object)
    s1 = set(df.columns)
    print(df.columns)
    add_col(df)
    s2 = set(df.columns)
    print(df.columns)


    print(s1.symmetric_difference(s2))
    df = df.replace('', 'NULL')
    df = df.fillna('NULL')
    df.to_csv(psv + "2", sep='|', index=False)


if __name__ == '__main__':

    update_file(sys.argv[1])

