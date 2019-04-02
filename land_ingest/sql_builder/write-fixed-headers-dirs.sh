#!/bin/bash


DATA_DIR="/gws/nopw/j04/c3s311a_lot2/data/beta_fix7/header_table"
HEADER_DIRS_FILE="beta_fix7_header_dirs.txt"

find $DATA_DIR -name "header_table_BETA_*" -type d > $HEADER_DIRS_FILE
