#!/bin/bash 
module load picard-tools
filelist=(
TL-2784-SARK012
)
for i in "${filelist[@]}"
do
    cut -f5 $i/Preprocessing/Recalibrated/recalibrated.tsv > tmp.txt
    while read -r line;
    do
        echo $line
        j=${line#/tmp/tobiastmp/}
        #j=${/tmp/tobiastmp/#$line}
        #j="$( sed /\\/tmp\\/tobiastmp\\\///g $line )"
        echo $j

    done < tmp.txt
done
