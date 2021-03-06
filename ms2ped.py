#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 16:53:12 2019
ms2ped --msFile FOO --thin 1000
@author: stsmall
"""
from __future__ import print_function
from __future__ import division
import numpy as np
import argparse
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument("--msFile", type=str, required=True,
                    help="msformatted file")
parser.add_argument("--locusLen", type=int, help="locus len")
parser.add_argument("--thin", type=int, default=0, help="thin snps")
args = parser.parse_args()


def read_msformat_file(msFile, loclen):
    """Read and parse simulations from ms formatted file from folder of files
    with basename
    """
    pos_list = []
    pos_count = 0
    block = 10000
    gtdict = defaultdict(list)
    with open(msFile, 'r') as ms:
        next(ms)
        for line in ms:
            if line.startswith("positions"):
                # collisions can result here when theta is high
                pos = np.round(np.array(line.strip().split()[1:], dtype=np.float64) * loclen)
                prev = 0
                for idx, item in enumerate(pos, start=0):
                    while prev >= item:
                        item += 1
                    pos[idx] = item
                    prev = pos[idx]
                pos_list.append(pos.astype(np.int64) + pos_count)  # append
                pos_count += block  # the two loci are unlinked
                line = next(ms)
                cix = 0
                try:
                    while line.strip():
                        try:
                            gtdict[cix].extend(map(int, line.strip()))
                        except IndexError:
                            break
                        cix += 1
                        line = next(ms)
                except StopIteration:
                    break
    return(gtdict, np.concatenate(pos_list, axis=0))


def ms2ped(gtdict, pos_list, thin):
    """
    """
    f = open("sim.ped", 'w')
    samp = 0
    haps = len(gtdict.keys())
    haplist = range(0, haps, 2)
    for i in haplist:
        geno = np.array(gtdict[i]) + np.array(gtdict[i + 1])
        geno12 = []
        for base in geno:  # prob a smarter way, like interweaving by insert
            if base == 2:
                geno12.extend([1, 1])
            elif base == 0:
                geno12.extend([2, 2])
            elif base == 1:
                geno12.extend([2, 1])
        f.write("Ind-{} Ind-{} 0 0 0 -9 {}\n".format(samp, samp, " ".join(map(str, geno12))))
        samp += 1
    f.close()
    return(None)


if __name__ == "__main__":
    gt, pos = read_msformat_file(args.msFile, args.locusLen)
    ms2ped(gt, pos, args.thin)
