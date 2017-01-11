# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

# problem 7
print("==========================")
print("problem 7")

def runTraining(transformX, N, total_iteration, D_N):
    
    X = np.random.uniform(-1,1,(D_N,1))
    Y = np.sin(np.pi * X)
    
    X = transformX(X)
    w = np.zeros((total_iteration,X.shape[1]))
    
    for i in range(0,total_iteration):
        
        # generate random points index
        
        r_indices = np.random.randint(1,D_N,N)
        w_dim_issue = np.linalg.lstsq(X[r_indices],Y[r_indices])[0]
        w_dim_issue = np.squeeze(w_dim_issue)
        w[i] = w_dim_issue
    
    
#    print("w: ",w.shape)
    g_bar = np.mean(w,axis=0)
    g_bar = np.expand_dims(g_bar, axis=0)
#    print("g_bar: ",g_bar.shape)
    pred = np.sum(X * g_bar, axis=1)
    pred = np.expand_dims(pred, axis=1)
#    print("pred: ",pred.shape)

    bias = np.mean(np.square(pred - Y));
    
    # apply gbar on every X to get g_d
    g_d = X.dot(w.T)
    
    variance = np.mean(np.mean(np.square(g_d - pred), axis=1))
    
    print("g_bar: ", g_bar)
    print("bias: ", bias)
    print("variance: ", variance)
    print("Eout: ", bias + variance)

########################################################################

N = 2
total_iteration = 10000
D_N = 10000

########################################################################
# constant
# h = a
print("--------------- h = a ------------------")
transformX = lambda X: np.ones((D_N,1))
runTraining(transformX, N, total_iteration, D_N)

########################################################################
# line passing thru origin
# h = ax
print("--------------- h = ax ------------------")
transformX = lambda X: X
runTraining(transformX, N, total_iteration, D_N)

########################################################################
# line with intercept
# h = ax + b
print("--------------- h = ax + b ------------------")
def transformX(X):
    X_t = np.ones((D_N,2))
    X_t[:,1] = np.squeeze(X)
    return X_t
runTraining(transformX, N, total_iteration, D_N)

########################################################################
# parabola passing thru origin
# h = ax^2
print("--------------- h = ax^2 ------------------")
transformX = lambda X: np.square(X)
runTraining(transformX, N, total_iteration, D_N)


########################################################################
# parabola with intercept
# h = ax + b
print("--------------- h = ax^2 + b ------------------")
def transformX(X):
    X_t = np.ones((D_N,2))
    X_t[:,1] = np.squeeze(np.square(X))
    return X_t
runTraining(transformX, N, total_iteration, D_N)


