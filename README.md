# sarekPrio


### Shortcut on tsv-file making

The Sarek tsv-file should have 7 columns and no headers

|-------------|-----|---|-----------------|----------------------|------------------|------------------|
| Patient 1   | XX  | 1 | Patient1-Tumor  | Patient1-Tumor-L001  | p1-T_R1.fastq.gz | p1-T_R2.fastq.gz |
| Patient 1   | XX  | 0 | Patient1-Normal | Patient1-Normal-L001 | p1-N_R1.fastq.gz | p1-N_R2.fastq.gz |

Col 1 is Patient ID, col 2 is gender, col 3 is 1 for Tumor and 0 for Normal. col4 is Sample name, col5 is sample name (+ lane if sequenced in multiple lanes), col6 is path to R1 fastq file, col7 is path to R2 fastq file.

