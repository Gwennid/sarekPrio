#!/bin/bash
module load annovar
source activate debarcer
#convert to annovar input
cat $1/test.vcf $1/test_indels.vcf > $1/test_both.vcf
./vcfToAnnovar.py $1/test_both.vcf $1/$1.avinput
annotate_variation.pl --buildver hg19 $1/$1.avinput /apps/bio/apps/annovar/20150322/humandb
./annotateCosmic.py $1/$1.avinput.exonic_variant_function $1/$1.exonic_variant_function.cosmic.txt


#onepass
cat $1/test_snv_onepass.vcf $1/test_indels_onepass.vcf > $1/test_both_onepass.vcf
./vcfToAnnovar.py $1/test_both_onepass.vcf $1/$1_onepass.avinput
annotate_variation.pl --buildver hg19 $1/$1_onepass.avinput /apps/bio/apps/annovar/20150322/humandb
./annotateCosmic.py $1/$1_onepass.avinput.exonic_variant_function $1/$1_onepass.exonic_variant_function.cosmic.txt
