#!/bin/bash

for dtype in header observations ; do 
  for y in $(seq 1800 2018) ; do 
    psql -U ${DBUSER} -h ${DBHOST} ${DBNAME} -c "DELETE FROM cdm_v1.${dtype}_${y}_land_0 WHERE (report_id NOT LIKE 'AFWA%') AND (report_id NOT LIKE 'ICAO%');"
  done
done

