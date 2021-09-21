#!/bin/bash
module load bedtools/2.17.0
mutectfile=mutect2*vcf
strelkafile=Strelka_*vs*_somatic_snvs.vcf
strelkaindelfile=Strelka_*vs*_somatic_indels.vcf
freebayesfile=freebayes*vcf

grep -e 'PASS' -e '^#' $mutectfile > mutect_all_pass.vcf
grep -e 'PASS' -e '^#' $strelkafile > strelka_all_pass.vcf
intersectBed -wo -header -a mutect_all_pass.vcf -b strelka_all_pass.vcf > mutect_strelka_pass.vcf
intersectBed -header -c -a mutect_strelka_pass.vcf -b $freebayesfile > test.vcf
intersectBed -wo -header -a $mutectfile -b $strelkafile > tmp.vcf
grep -e 'PASS' -e '^#' tmp.vcf > mutect_strelka_onepass.vcf
intersectBed -header -c -a mutect_strelka_onepass.vcf -b $freebayesfile > test_snv_onepass.vcf
echo 'SNVs:'
echo 'mutect variants pass' "$(grep -c -v -e '^#' mutect_all_pass.vcf)"
echo 'strelka variants pass' "$(grep -c -v -e '^#' strelka_all_pass.vcf)"
echo 'mutect_strelka variants' "$(grep -c -v -e '^#' mutect_strelka_pass.vcf)"
echo 'common variants' "$(grep -c -v -e '^#' test.vcf)"
echo 'mutect or strelka pass' "$(grep -c -v -e '^#' mutect_strelka_onepass.vcf)"
echo 'common variants' "$(grep -c -v -e '^#' test_snv_onepass.vcf)"

#indels
grep 'PASS' $strelkaindelfile > strelka_indels_pass.vcf
intersectBed -wo -a mutect_all_pass.vcf -b strelka_indels_pass.vcf > both_pass_indels.vcf
if [ -s both_pass_indels.vcf ]
then 
    intersectBed -a both_pass_indels.vcf -b $freebayesfile > test_indels.vcf
else
    touch test_indels.vcf
fi
intersectBed -wo -header -a $mutectfile -b $strelkaindelfile >mutect_strelka_indels.vcf
grep 'PASS' mutect_strelka_indels.vcf > mutect_strelka_indels_pass.vcf
intersectBed -header -a mutect_strelka_indels_pass.vcf -b $freebayesfile > test_indels_onepass.vcf
echo 'INDELS:'
echo 'mutect and strelka pass' "$(grep -c -v -e '^#' both_pass_indels.vcf)"
echo 'common indels' "$(grep -c -v -e '#^' test_indels.vcf)"
echo 'mutect or strelka pass' "$(grep -c -v -e '^#' mutect_strelka_indels_pass.vcf)"
echo 'common indels' "$(grep -c -v -e '^#' test_indels_onepass.vcf)"
