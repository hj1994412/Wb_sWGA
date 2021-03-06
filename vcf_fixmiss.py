# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 16:48:24 2015
fixmissing to be in line with vcf 4.0 as ./. rather than .:.:.:.:.
@author: stsmall
"""

import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('INvcf', metavar="INvcf", type=str,
                    help='path to vcf IN file')
args = parser.parse_args()


def fixmissing(vcfin):
    """
    """
    f = open(vcfin + ".fixmiss", 'w')
    with open(vcfin, 'r') as vcf:
        for line in vcf:
            if "#" not in line:
                x = line.split()
                dots = [i for i, s in enumerate(x[9:]) if re.search(r'^\.', s)]
                for i in dots:
                    if ("|" in x[i+9]):
                        x[i+9] = ".|."
                    else:
                        x[i+9] = "./."
                f.write('{}\n'.format('\t'.join(x)))  # writes line with snps
            else:  # this is header
                f.write(line)
    f.close()
    return(None)


if __name__ == '__main__':
    fixmissing(args.INvcf)
