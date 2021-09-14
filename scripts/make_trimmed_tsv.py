#!/usr/bin/python
from os.path import basename
import sys

def main(tsvfile, outputpath):
    newfilename=outputpath+'/trimmed/'+basename(tsvfile)
    print(newfilename)
    with open(tsvfile) as f, open(newfilename,'w') as g:
        for line in f:
            line=line.rstrip()
            parts=line.split()
            name=basename(parts[5]).replace('_R1_001.fastq.gz','')
            parts[5]=outputpath+'/trimmed/'+name+"_R1_001_trimmed_fixed.fastq.gz"
            parts[6]=outputpath+'/trimmed/'+name+"_R2_001_trimmed_fixed.fastq.gz"
            g.write('\t'.join(parts)+'\n')

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2])
