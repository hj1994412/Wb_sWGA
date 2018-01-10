# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:27:07 2016
make a bedfile mask for use with bedtools mask fasta from a lower-case fasta
where the lower case is considered a masked site
python make_maskbed.py foo.MASK.fa

@author: stsmall
"""
import re
import sys
from operator import itemgetter
from itertools import groupby
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--fasta", type=str, required=True,
                    help='fasta name')
args = parser.parse_args()


def make_negmaskbed(masked_fasta):
    f = open(masked_fasta + "-negmask.bed", 'w')
    with open(masked_fasta, 'r') as fasta:
        for line in fasta:
            if line.startswith(">"):
                contig = line.strip(">\n")
                length = 0
            else:
                line = line.rstrip("\n")
                length += len(line)
                bed_locate = [m.start() for m in re.finditer("[agtcnN]", line)]
                ranges = []
                for k, g in groupby(enumerate(bed_locate), lambda (i, x): i-x):
                    group = map(itemgetter(1), g)
                    ranges.append((group[0]+length, group[-1]+length))
                for item in ranges:
                    if len(item) > 1:
                        f.write("{}\t{}\t{}\n".format(contig, item[0], item[1]+1))
                    else:
                        f.write("{}\t{}\t{}\n".format(contig, item[0], item[0]+1))
        f.close()


def make_posmaskbed(masked_fasta):
    f = open(masked_fasta + "-posmask.bed", 'w')
    with open(masked_fasta, 'r') as fasta:
        for line in fasta:
            if line.startswith(">"):
                contig = line.strip(">\n")
                length = 0
            else:
                line = line.rstrip("\n")
                length += len(line)
                bed_locate = [m.start() for m in re.finditer("[AGTC]", line)]
                ranges = []
                for k, g in groupby(enumerate(bed_locate), lambda (i, x): i-x):
                    group = map(itemgetter(1), g)
                    ranges.append((group[0]+length, group[-1]+length))
                for item in ranges:
                    if len(item) > 1:
                        f.write("{}\t{}\t{}\n".format(contig, item[0], item[1]+1))
                    else:
                        f.write("{}\t{}\t{}\n".format(contig, item[0], item[0]+1))
        f.close()


if __name__ == "__main__":
    make_negmaskbed(args.fasta)
    make_posmaskbed(args.fasta)
