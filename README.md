# glamod-land-ingest

Library and utilities for re-formatting and ingesting LAND observations into
the GLAMOD database.

Data is provided by NUIM in PSV (pipe-separated variable) format and is 
processed by this code to generate new PSV files.

SQL loader scripts are then generated to write the content of the PSV files
to the database.

Finally, the SQL files are written to the database.

## Pre-requisites

Needs access to GLAMOD Group Workspace and LOTUS batch cluster.

Python 3, requires:
 - pandas
