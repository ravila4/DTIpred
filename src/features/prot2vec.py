#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:04:08 2018
@author: ravila
"""

from Bio import SeqIO
import glob
import pandas as pd
from multiprocessing import Pool
import numpy as np
import sys


def get_reading_frame(seq, n):
    """Takes a sequence string and an integer shift
    retruns a list of triplets shifted by the given ammount."""
    frame = []
    for f in (seq[i:i+3] for i in range(n, len(seq), 3)):
        if len(f) % 3 == 0:
            frame.append(f)
    return frame


def vectorize(r):
    fasta = SeqIO.read(r, 'fasta')
    sequence = str(fasta.seq)
    # Get reading frames
    rf1 = get_reading_frame(sequence, 0)
    rf2 = get_reading_frame(sequence, 1)
    rf3 = get_reading_frame(sequence, 2)
    # Get the sum of vectors for all the triplets.
    vec = np.zeros(100)
    for l in [rf1, rf2, rf3]:
        for t in l:
            component = np.array(model.loc[model[0] == t])[0][1:]
            vec = np.add(vec, component)
    name = r.split("/")[-1].rstrip(".txt")
    return [name] + [i for i in vec]


if __name__ == "__main__":
    # Import pre-trained model
    model = pd.read_csv("protVec_100d_3grams.csv", header=None)
    # List to store results
    vecs = []
    # Read receptor data
    dir_name = sys.argv[1].rstrip("/")
    receptors = glob.glob(dir_name + "/*.txt")
    # Start process pool
    pool = Pool(processes=4)
    vecs.append(pool.map(vectorize, receptors))
    vecs = vecs[0]
    vecs_df = pd.DataFrame(vecs)
    vecs_df.to_csv(dir_name + "_vec.csv", index=False)
