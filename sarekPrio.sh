#!/bin/bash -l
#$ -cwd
#$ -o run_sarekPrio_210507.stdout
#$ -e run_sarekPrio_210507.stderr
#$ -q batch.q
#$ -pe mpi 40
#$ -l excl=1

tsv=tsv/TL-2784-SARK027-B.tsv
