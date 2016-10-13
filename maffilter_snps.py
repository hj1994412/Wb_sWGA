#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:42:02 2016
filter maf
@author: scott
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('INvcf', metavar="INvcf",type=str,help='path to vcf IN file') 
parser.add_argument('-s', '--samples', type=int, required=True, help="number of samples to expect")
args = parser.parse_args()

def mafFilter(vcfin,samples):
    f = open(vcfin + ".maffilter",'w')
    with open(vcfin,'r') as vcf:
        for line in vcf:
            if line.startswith("#"):
                f.write(line)
            else:    
                x=line.split()
                for i in range(0,samples):
                    if "0/1" in x[9+i].split(":")[0]:
                        dp = int(x[9+i].split(":")[2])
                        ao = int(x[9+i].split(":")[6])
                        maf = float(ao)/dp
                        if maf < 0.3:
                            x9 = x[9+i].split(":")
                            x9[0] = "0/0"
                            x[9+i] = ":".join(x9)
                        elif maf > 0.7:
                            x9 = x[9+i].split(":")
                            x9[0] = "1/1"
                            x[9+i] = ":".join(x9)
                f.write("%s\n" %"\t".join(x))
    f.close()
def main():
    mafFilter(args.INvcf, args.samples)

if __name__ == '__main__':
    main()
            
