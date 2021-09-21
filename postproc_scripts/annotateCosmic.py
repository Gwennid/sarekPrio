#!/usr/bin/env python
import sys       
import os
import pickle
def load_cosmic_database(filename):
    cosmic={}
    n=0
    with open(filename) as f:
        line=f.readline()
        for line in f:
            line=line.rstrip()
            parts=line.split('\t')
            position=parts[23]
            if position not in cosmic:
                cosmic[position]=1
            else:
                cosmic[position]+=1
            n+=1
            if n%1e6==0:
                print(n)
    return(cosmic)
class Bed_region:
    def read_bed(self,bedentry):
        parts=bedentry.split('\t')
        coords=parts[3]
        self.contig=coords.split(':')[0]
        self.start=coords.split(':')[1].split('-')[0]
        self.end=coords.split(':')[1].split('-')[1]
        self.name=parts[0]

def parse_census(filename):
    bed_regions=[]
    with open(filename) as infile:
        line=infile.readline()
        for line in infile:
            line=line.rstrip()
            region=Bed_region()
            region.read_bed(line)
            if region.start not in "" and region.end not in "":
                bed_regions.append(region)
    return(bed_regions)

def overlap_with_bed(contig,position,bed_regions):
    overlap=None
    for r in bed_regions:
        if r.contig==contig:
            if int(position) > int(r.start) and int(position) < int(r.end):
                overlap=r.name
    return(overlap)

def main():
    if not os.path.isfile('cosmic_database.pickle'):
        cosmic_database_filename='/medstore/Illumina_Tobias/db/COSMIC/CosmicDownload.tsv'
        cosmic=load_cosmic_database(cosmic_database_filename)
        with open('cosmic_database.pickle','wb') as g:
            pickle.dump(cosmic,g)
    else:
        with open('cosmic_database.pickle','rb') as f:
            cosmic=pickle.load(f)
    if not os.path.isfile('census.pickle'):
        census=parse_census('/medstore/Illumina_Tobias/db/COSMIC/Census_all.tsv')
        with open('census.pickle','wb') as g:
            pickle.dump(census,g)
    else:
        with open('census.pickle','rb') as f:
            census=pickle.load(f)
     
    n=0
    g=open(sys.argv[2],'w')
    with open(sys.argv[1]) as f:
        #line=f.readline()
        #line=line.rstrip()
        #line=line.split('\t')
        #line.append("Cosmic count")
        #line.append("Census gene")
        #g.write('\t'.join(line)+'\n')
        g.write('Line\ttype\tGene, genomic change, amino acid change\tChromosome\tPosition start\tPosition end\tRef allele\tObserved allele\tMuTect2 call\tStrelka call\tDepth in tumor (ref allele)\tDepth in tumor (observed allele)\tAllele frequency in tumor\tDepth in normal (ref allele)\tDepth in normal (observed allele)\tAllele frequency in normal\tCosmic count\tCensus gene\n')
        for line in f:
            census_overlap=''
            line=line.rstrip()
            line=line.split('\t')
            parts=line
            chrx=parts[3]
            position='{}:{}-{}'.format(chrx,parts[4],parts[4])
            positionplus1='{}:{}-{}'.format(chrx,int(parts[4])+1,int(parts[4])+1)
            positionminus1='{}:{}-{}'.format(chrx,int(parts[4])-1,int(parts[4])-1)
            census_overlap=overlap_with_bed(chrx,parts[4],census)
            if position in cosmic:
                cosmiccount=cosmic[position]
                n+=1
            else:
                cosmiccount=''
            if census_overlap==None:
                census_overlap=''
            line.append(str(cosmiccount))
            line.append(census_overlap)
            #line[0]=line[0].lstrip('"')
            g.write('\t'.join(line)+'\n')
    print(n)
    g.close()

if __name__=='__main__':
    main()
