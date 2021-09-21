#!/usr/bin/env python3
import sys
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description="annotate the vcf file with coverage etc and prepare for annovar input.")
    parser.add_argument('-i','--infile',dest='infile', help='The path to the input file',required=True)
    parser.add_argument('-o','--outfile',dest='outfile',help='The path to the output file',required=True)
    parser.add_argument('-m','--mode',dest='mode',help='Mode, can be combined,mutect2,strelka,freebayes, default=%(default)s',default='combined')
    parser.add_argument('-t','--strelkatier',dest='strelkatier', help='Strelka tier, 1 or 2, default=%(default)s',default=1)
    args=parser.parse_args(sys.argv[1:])
    return(args)


def convert2annovar_combined(inputfile,outputfile):
    
    with open(inputfile) as f, open(outputfile,'w') as g:
        n=0
        g.write('#Chromosome\tPosition start\tPosition end\tRef allele\tMutect2 call\tStrelka call\tObserved allele\tDepth in tumor (ref allele)\tDepth in tumor (observed allele)\tAllele frequency in tumor\tDepth in normal (ref allele)\tDepth in normal (observed allele)\tAllele frequency in normal\n')
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

def convert2annovar_mutect2(inputfile,outputfile):
   with open(inputfile) as f, open(outputfile,'w') as g:
        n=0
        g.write('#Chromosome\tPosition start\tPosition end\tRef allele\tMutect2 call\tObserved allele\tDepth in tumor (ref allele)\tDepth in tumor (observed allele)\tAllele frequency in tumor\tDepth in normal (ref allele)\tDepth in normal (observed allele)\tAllele frequency in normal\n')
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
                g.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(chrx,start,end,ref,alt,mutectfilter,ADt_ref,ADt_alt,AFt,ADn_ref,ADn_alt,AFn))

def convert2annovar_strelka(inputfile,outputfile,strelkatier):
   with open(inputfile) as f, open(outputfile,'w') as g:
        if strelkatier=='1':
            tierindex=0
        if strelkatier=='2':
            tierindex=1
        n=0
        g.write('#Chromosome\tPosition start\tPosition end\tRef allele\tMutect2 call\tObserved allele\tDepth in tumor (ref allele)\tDepth in tumor (observed allele)\tAllele frequency in tumor\tDepth in normal (ref allele)\tDepth in normal (observed allele)\tAllele frequency in normal\n')
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
                if len(ref)==1:
                    start=pos
                    end=pos
                else:
                    start=pos
                    end=int(pos)+len(ref)-1
                tumor=parts[9]
                normal=parts[10]
                DPt,FDPt, SDPt, subDPt ,AUt,CUt,GUt,TUt,*rest=tumor.split(':')
                Ut={'A':AUt, 'C':CUt, 'G':GUt, 'T':TUt}
                DPn,FDPn, SDPn, subDPn ,AUn,CUn,GUn,TUn,*rest=normal.split(':')
                Un={'A':AUn, 'C':CUn, 'G':GUn, 'T':TUn}
                ADt_ref=int(Ut[ref].split(',')[tierindex])
                ADt_alt=int(Ut[alt].split(',')[tierindex])
                ADn_ref=int(Un[ref].split(',')[tierindex])
                ADn_alt=int(Un[alt].split(',')[tierindex])
                if ADt_ref+ADt_alt>0:
                    AFt=1.0*ADt_alt/(ADt_ref+ADt_alt)
                else:
                    AFt=0
                if ADn_ref+ADn_alt>0:
                    AFn=1.0*int(ADn_alt)/(int(ADn_ref)+int(ADn_alt))
                else:
                    AFn=0
                g.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(chrx,start,end,ref,alt,mutectfilter,ADt_ref,ADt_alt,AFt,ADn_ref,ADn_alt,AFn))

def main(infile,outfile,mode,strelkatier):
    if mode.lower()=='combined':
        convert2annovar_combined(infile,outfile)
    elif mode.lower()=='mutect2':
        convert2annovar_mutect2(infile,outfile)
    elif mode.lower()=='strelka':
        convert2annovar_strelka(infile,outfile,strelkatier)
if __name__=='__main__':
    args=parseArgs()
    main(args.infile,args.outfile,args.mode,args.strelkatier)
