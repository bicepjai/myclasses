# version code 3ebd92e7eece+
coursera = 1
# Please fill out this stencil and submit using the provided submission script.

import random
import os, binascii
from GF2 import one
from vecutil import list2vec
from independence import is_independent, rank
from itertools import combinations

## 1: (Task 1) Choosing a Secret Vector
def randGF2(): return random.randint(0,1)*one

a0 = list2vec([one, one,   0, one,   0, one])
b0 = list2vec([one, one,   0,   0,   0, one])

def choose_secret_vector(s,t):
    while True:
    	u = list2vec([randGF2() for i in range(6)])
    	if u*a0 == s and u*b0 == t:
    		return u



## 2: (Task 2) Finding Secret Sharing Vectors
TOTALVECS = 2**6
def allPossibleVectors():
	binaryInOne = lambda n: n>0 and [one if n&1 == 1 else 0]+binaryInOne(n>>1) or []
	allVecs = []
	for v in list({list2vec(binaryInOne(n)) for n in range(TOTALVECS)} - {a0,b0}):
		v.D = set(range(6))
		allVecs.append(v)
	return allVecs

def is_comb_3pairs_independent(listOfPairs):
	allCombs = [[v for pair in pairs3 for v in pair]for pairs3 in combinations(listOfPairs,3)]
	return all(is_independent(comb) for comb in allCombs)

def get10RandomVecs():
	allVecs = allPossibleVectors()
	vecs 	= [(a0, b0)]
	rand = random.SystemRandom()
	while len(vecs) < 5:
		rand.shuffle(allVecs)
		i1 = rand.randint(0,len(allVecs)-1)
		i2 = rand.randint(0,len(allVecs)-1)
		if i1 != i2:
			a = allVecs[i1]
			b = allVecs[i2]
			if is_comb_3pairs_independent(vecs+[(a,b)]):
					vecs.append((a,b))
					print("independant dude")
					print(a,b)
	return vecs

# Give each vector as a Vec instance
vecs = get10RandomVecs()

secret_a0 = vecs[0][0]
secret_b0 = vecs[0][1]
secret_a1 = vecs[1][0]
secret_b1 = vecs[1][1]
secret_a2 = vecs[2][0]
secret_b2 = vecs[2][1]
secret_a3 = vecs[3][0]
secret_b3 = vecs[3][1]
secret_a4 = vecs[4][0]
secret_b4 = vecs[4][1]

