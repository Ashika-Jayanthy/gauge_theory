from Bio import pairwise2
from Bio import SeqIO
from core import *
import glob
import sys
import numpy as np
import random
import threading

indir = "./Data/hmm_sequences/"
outdir = "./Data/yarrays"
files = glob.glob(f"{indir}/*")

def matrix_to_c2(m):
    return np.array([m[0,0],m[1,0]])

def pairwise_alignment(s1,s2):
    score = pairwise2.align.globalxx(s1, s2, score_only=True, one_alignment_only=True)
    return score

def per_thread(start,stop):
    ff = start
    for file in files[start:stop]:
        print(f"{ff} of {start}:{stop}")
        sequences = []
        for record in SeqIO.parse(file,"fasta"):
            sequences.append(record.seq.upper())
        n = len(sequences)
        distances = np.zeros((n,n))
        print(f"{start}:{stop} Calculating distances..")
        for i in range(n):
            for j in range(i+1,n):
                align_score = pairwise_alignment(sequences[i],sequences[j])
                distances[i,j] = align_score
                distances[j,i] = align_score

        print(f"{start}:{stop} Ordering sequences..")
        ordered_sequences = []
        idx = random.choice(np.arange(n))
        distances[:,idx] = 0
        ordered_sequences.append(sequences[idx])
        while len(ordered_sequences)<len(sequences):
            idx = np.argmax(distances[idx])
            distances[:,idx] = 0
            ordered_sequences.append(sequences[idx])

        print(f"{start}:{stop} Running RKMK..")
        def Y(t):
            seq = ordered_sequences[t]
            y_t = expm(Sequence(seq).run())
            return y_t
        n_sequences = len(ordered_sequences)
        y_array = []
        for n in range(n_sequences):
            y = Y(n)
            next_y = rkmk_step(Y,y,n)
            y_array.append(matrix_to_c2(next_y))
        print(f"{start}:{stop} Writing output..")
        np.savetxt(f"{outdir}/f{ff}_yarray.txt", y_array, fmt='%.18e', delimiter=' ', newline='\n')
        ff+=1
        return


for start_file_num in range(0,1000,50):
    thread = threading.Thread(target=per_thread, name = str(start_file_num), args=(start_file_num,start_file_num+50))
    thread.start()
