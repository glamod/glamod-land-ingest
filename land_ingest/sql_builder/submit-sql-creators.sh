#!/bin/bash

N=$(wc -l beta_fix7_header_dirs.txt | cut -d' ' -f1)
interval=5000

for i in `seq 1 $interval $N` ; do
    start=$i
    end=$(( $start + $interval ))

    if [ $end -gt $N ]; then
        end=$N
    fi

    echo $start $end
    cmd="bsub -q short-serial -W 24:00 -o lotus-loader-jobs/job-${start}-${end}.o -e lotus-loader-jobs/job-${start}-${end}.e wrap-create-sql.sh $start $end"
    echo "[INFO] $cmd"
    $cmd
done

echo "Submitted for $N header file directories."
