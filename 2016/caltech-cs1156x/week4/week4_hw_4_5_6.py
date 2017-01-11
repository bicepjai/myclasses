# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

# problem 4,5,6
print("==========================")
print("problem 4,5,6")

# training sample size
N = 2
total_iteration = 10000
w = np.zeros((total_iteration,1))

bias = 0
variance = 0

#creating data set
D_N = 10000
X = np.random.uniform(-1,1,D_N)
X.shape = (D_N,1)

# y outputs
Y = np.tanh(np.pi * X)
#Y = np.sin(np.pi * X)

for i in range(0,total_iteration):
    
    # generate random points index
    r_indices = np.random.randint(1,D_N,N)
    w[i] = ((np.linalg.lstsq(X[r_indices],Y[r_indices]))[0])

g_bar = np.mean(w)
pred = X * g_bar
bias = np.mean(np.square(pred - Y));

# apply gbar on every X to get g_d
g_d = X.dot(w.T)

variance = np.mean(np.mean(np.square(g_d - pred), axis=1))

print("g_bar: ", g_bar)
print("bias: ", bias)
print("variance: ", variance)