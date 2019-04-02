#!/usr/bin/env python

import pandas as pd

FPATH = '/gws/nopw/j04/c3s311a_lot2/data/glamod_land_delivery_2018_12_31_Beta/observations_table/sub_daily/AFWA_protect/observation_table_BETA_AFWA_077201_1.psv'


def parse_file(fpath=FPATH):
    lines = open(fpath).readlines()[1:]

    data = [_.strip().split('|')[0] for _ in lines]
    return data


data = parse_file()

