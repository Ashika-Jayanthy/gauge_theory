import numpy as np
from main import *
import math
import matplotlib.pyplot as plt
from scipy.linalg import expm
import random

t_i = 0
t_f = 20
h = 1
T = t_f - t_i

def random_image_array(num_images = 10,num_pixels = 20):
    return np.array([np.random.choice((0,255),n_pixels) for a in range(n_images)])

def random_sequence_evolve(sequence,n_replacements = 10, l_replacement=1):
    replacement = ''.join(random.choice('CGTA') for _ in range(l_replacement))
    replacement_index = random.choice(np.arange(0,len(sequence)))
    for i in range(n_replacements):
        s = sequence[:(replacement_index-l_replacement)] + replacement + sequence[replacement_index + 1:]
    return s

sequence_array = []
init_sequence = ''.join(random.choice('CGTA') for _ in range(20))
s = random_sequence_evolve(init_sequence)
sequence_array.append(s)
for t in range(T):
    s = random_sequence_evolve(s)
    sequence_array.append(s)

print(sequence_array)


def G(t,g):
    s_t = sequence_array[int(t)]
    g = Sequence(s_t).run()
    gg = expm(g)
    g_t = np.array([gg[0,0], gg[1,0]])
    return g_t


g0 = np.array([complex(0,0),complex(0,1)])
solution = solve(G, g0, t_i, t_f, h)
print(solution[0])



for x in solution[0]:
    plt.polar([0,np.angle(x[1])],[0,np.abs(x[1])],marker='o')
plt.show()
