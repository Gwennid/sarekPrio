#!/bin/bash -l
#$ -cwd
#$ -o run_sarekPrio_210507.stdout
#$ -e run_sarekPrio_210507.stderr
#$ -q batch.q
#$ -pe mpi 40
#$ -l excl=1
module load nextflow
module load singularity
Sarek_installation_path=/apps/bio/software/sarek/

#Setup
tsv=/medstore/Illumina_Tobias/cv/tsv/TL-2784-SARK012.tsv
outdirname=$(basename $tsv |sed s/'.tsv'//g)
echo $outdirname
genome=GRCh37
genome_base=/medstore/Illumina_Tobias/db/GRCh37/

#Run preprocessing
./scripts/run_trimming.sh $tsv $outdirname
newtsvname=$OUTPUT_DIRECTORY/trimmed/"$( basename $TSV_FILE)"


#Run Sarek pipeline
nextflow run $Sarek_installation_path/main.nf --sample $newtsvname --step mapping --genome $genome --genome_base $genome_base -profile singularityPath --outDir $outdirname --noReports
nextflow run $Sarek_installation_path/somaticVC.nf --outDir $outdirname --genome $genome --genome_base $genome_base -profile singualrityPath --tools mutect2,strelka,freebayes --noReports
nextflow run $Sarek_installation_path/runMultiQC.nf --outDir $outdirname -profile singularityPath

