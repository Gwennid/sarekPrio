#!/bin/bash
module load trim_galore
module load cutadapt
module load fastqc
module load bbmap
TSV_FILE=$1
OUTPUT_DIRECTORY=$2

if [ ! -d $OUTPUT_DIRECTORY ]
then
    mkdir $OUTPUT_DIRECTORY
fi

if [ ! -d $OUTPUT_DIRECTORY"/trimmed" ]
then mkdir $OUTPUT_DIRECTORY"/trimmed"
fi

R1_PATHS=( $( awk '{print $6}' $TSV_FILE ) )
R2_PATHS=( $( awk '{print $7}' $TSV_FILE ) )


for i in "${!R1_PATHS[@]}"
do
   name=$( basename "${R1_PATHS[i]}" | sed s/'_R1_001.fastq.gz'//g)
   outputdir=$(dirname "${R1_PATHS[i]}")
   echo $i'_R1_001.fastq.gz'
   trim_galore --fastqc "${R1_PATHS[i]}" "${R2_PATHS[i]}" --stringency 3 -o $OUTPUT_DIRECTORY/trimmed &
done
wait
for i in "${!R1_PATHS[@]}"
do
    outputdir=$(dirname "${R1_PATHS[i]}")
    name=$( basename "${R1_PATHS[i]}" | sed s/'_R1_001.fastq.gz'//g)
    repair.sh in1=$OUTPUT_DIRECTORY/trimmed/$name"_R1_001_trimmed.fq.gz" in2=$OUTPUT_DIRECTORY/trimmed/$name"_R2_001_trimmed.fq.gz" out1=$OUTPUT_DIRECTORY/trimmed/$name"_R1_001_trimmed_fixed.fastq.gz" out2=$OUTPUT_DIRECTORY/trimmed/$i"_R2_001_trimmed_fixed.fastq.gz" outsingle=$OUTPUT_DIRECTORY/trimmed/$i"_single.fastq.gz" &
done
wait

#create trimmed tsv_file
newfilename=$OUTPUT_DIRECTORY/trimmed/"$( basename $TSV_FILE)"


