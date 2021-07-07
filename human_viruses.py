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

    for file_num in range(start,stop):
        print(f"{file_num} of {start}:{stop}")

        file = open(f"./Data/hmm_sequences/{file_num}.fasta",'r')
        sequences = []
        for record in SeqIO.parse(file,"fasta"):
            sequences.append(record.seq.upper())
        file.close()

        n_sequences = len(sequences)
        distances = np.zeros((n_sequences,n_sequences))
        print(f"{file_num} Calculating distances..")
        for i in range(n_sequences):
            for j in range(i+1,n_sequences):
                align_score = pairwise_alignment(sequences[i],sequences[j])
                distances[i,j] = align_score
                distances[j,i] = align_score
        print(distances)

        print(f"{file_num} Ordering sequences..")
        ordered_sequences = []
        idx = random.choice(np.arange(n_sequences))
        distances[:,idx] = 0
        ordered_sequences.append(sequences[idx])
        while len(ordered_sequences)<n_sequences:
            idx = np.argmax(distances[idx])
            distances[:,idx] = 0
            ordered_sequences.append(sequences[idx])

        print("lengths", len(ordered_sequences),n_sequences)
        print(f"{file_num} Running RKMK..")
        def Y(t):
            seq = ordered_sequences[t]
            y_t = expm(Sequence(seq).run())
            return y_t

        y_array = []
        for n in range(n_sequences):
            y = Y(n)
            next_y = rkmk_step(Y,y,n)
            y_array.append(next_y)
        print(f"{file_num} Writing output..")
        #np.savetxt(f"{outdir}/f{file_num}_yarray.txt", y_array, fmt='%.18e', delimiter=' ', newline='\n')
        with open(f"{outdir}/f{file_num}_yarray.pkl",'w') as outfile:
            pkl.dump(y_array,outfile)

    return


for start_file_num in range(1,1001,100):
    thread = threading.Thread(target=per_thread, name = str(start_file_num), args=(start_file_num,start_file_num+100))
    thread.start()
