#!/bin/bash

START=$1
END=$2
echo "ARGS: $START $END AND $@"

cd /gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/db-loader
mkdir -p lotus-loader-jobs

export PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin:$PATH
source /apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin/activate jaspy3.7-m3-4.5.11-r20181219

/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/envs/jaspy3.7-m3-4.5.11-r20181219/bin/python create-sql.py $START $END

