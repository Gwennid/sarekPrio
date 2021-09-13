#!/bin/bash -l
#$ -cwd
#$ -o run_sarekPrio_210507.stdout
#$ -e run_sarekPrio_210507.stderr
#$ -q batch.q
#$ -pe mpi 40
#$ -l excl=1

tsv=/medstore/Illumina_Tobias/cv/tsv/TL-2784-SARK012.tsv
outdirname=$(basename $tsv |sed s/'.tsv'//g)
echo $outdirname
genome=GRCh38
genome_base=/medstore/Illumina_Tobias/db/GRCh38/

./scripts/run_trimming.sh $tsv
nextflow run main.nf --sample $tsv --step mapping --genome $genome --genome_base $genome_base -profile docker --outDir $outdirname --noReports
nextflow run somaticVC.nf --outDir $outdirname --genome $genome --genome_base $genome_base -profile docker --tools mutect2,strelka,freebayes --noReports
nextflow run runMultiQC.nf --outDir $outdirname -profile docker
