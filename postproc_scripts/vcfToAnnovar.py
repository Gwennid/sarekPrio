#!/usr/bin/env python3
import sys
def convert2annovar(inputfile,outputfile):
    with open(inputfile) as f, open(outputfile,'w') as g:
        n=0
        g.write('Chromosome\tPosition start\tPosition end\tRef allele\tMutect2 call\tStrelka call\tObserved allele\tDepth in tumor (ref allele)\tDepth in tumor (observed allele)\tAllele frequency in tumor\tDepth in normal (ref allele)\tDepth in normal (observed allele)\tAllele frequency in normal\n')
        for line in f:
            if not line.startswith('#'):
                n+=1
                line=line.rstrip()
                parts=line.split('\t')
                chrx=parts[0]
                ref=parts[3]
                alt=parts[4]
                pos=parts[1]
                mutectfilter=parts[6]
                strelkafilter=parts[17]
                if len(ref)==1:
                    start=pos
                    end=pos
                else:
                    start=pos
                    end=int(pos)+len(ref)-1
                tumor=parts[9]
                normal=parts[10]
                GTt,ADt,AFt,*rest=tumor.split(':')
                ADt_ref,ADt_alt,*rest=ADt.split(',')
                
                GTn,ADn,AFn,*rest=normal.split(':')
                ADn_ref,ADn_alt,*rest=ADn.split(',')
                g.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(chrx,start,end,ref,alt,mutectfilter,strelkafilter,ADt_ref,ADt_alt,AFt,ADn_ref,ADn_alt,AFn))

if __name__=='__main__':
    convert2annovar(sys.argv[1],sys.argv[2])
