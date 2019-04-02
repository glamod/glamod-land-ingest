#!/bin/bash

for freq in monthly daily sub_daily; do

    find /gws/nopw/j04/c3s311a_lot2/data/beta_fix7/*/${freq} -type f | wc -l > ${freq}-count.txt 

done
