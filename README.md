# sarekPrio


### Shortcut on tsv-file making

The Sarek tsv-file should have 7 columns (tab-separated) and no headers

| Col1        | Col2 | Col3 | Col4        | Col5                 | Col6             | Col7             |
| ----------- | --- | - | --------------- | -------------------- | ---------------- | ---------------- |
| Patient 1   | XX  | 1 | Patient1-Tumor  | Patient1-Tumor-L001  | p1-T_R1.fastq.gz | p1-T_R2.fastq.gz |
| Patient 1   | XX  | 0 | Patient1-Normal | Patient1-Normal-L001 | p1-N_R1.fastq.gz | p1-N_R2.fastq.gz |

Col 1 is Patient ID, col 2 is gender, col 3 is 1 for Tumor and 0 for Normal. col4 is Sample name, col5 is sample name (+ lane if sequenced in multiple lanes), col6 is path to R1 fastq file, col7 is path to R2 fastq file.

Start by automatically generate col6 and col7 for all samples, then edit the resulting file and type in col 1-5 manually.

Go to a parent folder of the fastq files, list all R1 fastq.gz files, then R2 files. `pwd` is the path to the current directory. Keep this to get full paths.

```bash
find `pwd` -name *R1*.fastq.gz | sort > r1files.txt
find `pwd` -name *R2*.fastq.gz | sort > r2files.txt
paste r1files.txt r2files.txt > all.tsv
```

Open the all.tsv file in a text editor and add the missing columns.

