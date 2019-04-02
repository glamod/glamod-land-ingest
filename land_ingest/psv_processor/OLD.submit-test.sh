#!/bin/bash
#BSUB -J land_fix_[1-2]
#BSUB -o lotus-outputs/land_fix_%I.o
#BSUB -e lotus-outputs/land_fix_%I.e
#BSUB -q short-serial
#BSUB -W 24:00

export PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin:$PATH
source /apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin/activate jaspy3.7-m3-4.5.11-r20181219

cd /gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/beta-refactor
/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/envs/jaspy3.7-m3-4.5.11-r20181219/bin/python generate-new-files.py -index ${LSB_JOBINDEX} -job_size 4 -array_size 2
