# PSV Processor code

## Main processing code

The main processing code is:

 generate-new-files.py

This uses an input file containing the paths of all the PSV Header Table
files provided, at:

 header_table_files.txt 

This is wrapped in a LOTUS script:

 wrap-submit-jobs.py

## Running on a test file

You can run in test mode (locally) for a single Header Table file using:

 generate-test-mode.py


# Running all jobs on LOTUS

## Empty the output and logs areas

```
rm -fr /gws/nopw/j04/c3s311a_lot2/data/beta_fix2/*
rm -f /gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/beta-refactor/lotus-outputs/*
```

## Run a quick couple of test jobs

```
ssh <you>@jasmin-sci6.ceda.ac.uk
cd /gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/beta-refactor

# Run a quick test with just a few
bsub < submit-test.sh

# Check they are running
bjobs

# Check they ran
cat lotus-outputs/*

# Look for output files
find /gws/nopw/j04/c3s311a_lot2/data/beta_fix2 -type f

# Compare two outputs
fpath=$(find /gws/nopw/j04/c3s311a_lot2/data/beta_fix2 -type f | tail -1)
fpath_old=$(echo $fpath | sed 's/beta_fix2/beta_fix/')

export PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin:$PATH
source /apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/bin/activate jaspy3.7-m3-4.5.11-r20181219
/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/envs/jaspy3.7-m3-4.5.11-r20181219/bin/python -i ../concatente_files.py $fpath_old $fpath

# In python session do
>>> df
# And have a good compare of the outputs
```

## Run all jobs

```
ssh <you>@jasmin-sci6.ceda.ac.uk
cd /gws/nopw/j04/c3s311a_lot2/code/land_code/land_ingest/beta-refactor

# Run a quick test with just a few
bsub < submit-jobs.sh
```

