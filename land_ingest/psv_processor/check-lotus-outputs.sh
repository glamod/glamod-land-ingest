#!/bin/bash

OUTDIR=lotus-outputs-7

end=${1:-1000}

echo "[INFO] Check all outputs exist"

for i in `seq 1 $end`; do 
    base=$OUTDIR/land_fix_${i}

    for ftype in e o; do
        fpath=${base}.${ftype}

        if [ ! -f $fpath ]; then
            echo "[ERROR] Missing: $fpath"
            continue
        fi

        if [ $ftype == "e" ]; then
            size=$(stat -c%s $fpath)
            
            if [ $size -ne 0 ]; then
                echo "[ERROR] Non-zero error file: $fpath"
            fi

        fi

    done
done
