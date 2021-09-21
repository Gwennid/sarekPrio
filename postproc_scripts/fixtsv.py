#!/usr/bin/env python
import sys

def main(filename):
    samplelist=[]
    with open(filename) as f:
        for line in f:
            line=line.rstrip()
            parts=line.split()
            print(parts)
            sample=parts[0]
            filepart=parts[3]
            if sample not in samplelist:
                samplelist.append(sample)
                g=open('tsv/'+sample+'.tsv','w+')
            else:
                g=open('tsv/'+sample+'.tsv','a')
            g.write(line+'\t'+'/tmp/tobiastmp/'+filepart+'_R1_001_trimmed_fixed.fastq.gz'+'\t'+'/tmp/tobiastmp/'+filepart+'_R2_001_trimmed_fixed.fastq.gz'+'\n')
            g.close()

if __name__=='__main__':
    main(sys.argv[1])
                    
