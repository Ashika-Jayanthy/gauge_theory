from Bio import pairwise2
from Bio import SeqIO
from core import *
import numpy as np
import random
import threading
import pickle as pkl

indir = "./Data/hmm_sequences/"
outdir = "./Data/ordered_sequences"


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

        print(f"{file_num} Ordering sequences..")
        ordered_sequences = []
        idx = random.choice(np.arange(n_sequences))
        distances[:,idx] = 0
        ordered_sequences.append(sequences[idx])
        while len(ordered_sequences)<n_sequences:
            idx = np.argmax(distances[idx])
            distances[:,idx] = 0
            ordered_sequences.append(sequences[idx])

        print(f"{file_num} Writing output..")
        with open(f"{outdir}/f{file_num}_ordered_sequence.pkl",'wb') as outfile:
            pkl.dump(ordered_sequences,outfile)

    return


for start_file_num in range(1,1001,100):
    thread = threading.Thread(target=per_thread, name = str(start_file_num), args=(start_file_num,start_file_num+100))
    thread.start()
