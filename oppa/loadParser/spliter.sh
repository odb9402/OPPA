:'
    This script will split narrowPeak file by chromosome.
    It sholud be extended to other format.
'

#!/bin/sh

sort -k 1V,1 -k 2n,2 $1 -o $1

SUBSTRING=$(echo $1| cut -d'.' -f 1)

awk '{close(f);f=$1}{print > "'$SUBSTRING'.REF_"f".narrow_peaks.narrowPeak"}' "$1"
