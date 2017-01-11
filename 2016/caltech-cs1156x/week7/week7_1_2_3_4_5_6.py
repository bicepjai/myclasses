# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 10:47:12 2016

@author: bicepjai
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.spatial.distance import cdist
import random

data_in = np.loadtxt("data/data.in")
data_out = np.loadtxt("data/data.out")

N_in,C_in = data_in.shape
X_in = np.ones((N_in,8))
X_in[:,1] = data_in[:,0]
X_in[:,2] = data_in[:,1]
X_in[:,3] = np.square(X_in[:,1])
X_in[:,4] = np.square(X_in[:,2])
X_in[:,5] = X_in[:,1] *  X_in[:,2]
X_in[:,6] = np.abs(X_in[:,1] -  X_in[:,2])
X_in[:,7] = np.abs(X_in[:,1] +  X_in[:,2])

Y_in = np.expand_dims(data_in[:,2],0).T

N_out,C_out = data_out.shape
X_out = np.ones((N_out,8))
X_out[:,1] = data_out[:,0]
X_out[:,2] = data_out[:,1]
X_out[:,3] = np.square(X_out[:,1])
X_out[:,4] = np.square(X_out[:,2])
X_out[:,5] = X_out[:,1] *  X_out[:,2]
X_out[:,6] = np.abs(X_out[:,1] -  X_out[:,2])
X_out[:,7] = np.abs(X_out[:,1] +  X_out[:,2])

Y_out = np.expand_dims(data_out[:,2],0).T

# problem 1,2
print("\nproblem 1,2 ================================================")
ks = [3,4,5,6,7]

for k in ks:
    
    Xin = X_in[:25,:k+1]
    Yin = Y_in[:25,:k+1]
    Xv = X_in[25:,:k+1]
    Yv = Y_in[25:,:k+1]
    Xout = X_out[:,:k+1]
    Yout = Y_out[:,:k+1]
    
    # in sample calculation
    Xin_dagger=np.dot(np.linalg.pinv(np.dot(Xin.T,Xin)),Xin.T)
    win = np.dot(Xin_dagger,Yin)
    
    g_of_xin = np.sign((win.T).dot(Xin.T))
    p_in  = np.mean((g_of_xin != Yin.T).astype(int))
    
    # validation calculation
    g_of_xv = np.sign((win.T).dot(Xv.T))
    p_v  = np.mean((g_of_xv != Yv.T).astype(int))

    # out of sample calculation
    g_of_xout = np.sign((win.T).dot(Xout.T))
    p_out  = np.mean((g_of_xout != Yout.T).astype(int))
    
    print("--k:",k," -- p_in",p_in, "p_v",p_v, "p_out",p_out)

# problem 3,4
print("\nproblem 3,4 ================================================")
ks = [3,4,5,6,7]

for k in ks:
    
    Xv = X_in[:25,:k+1]
    Yv = Y_in[:25,:k+1]
    Xin = X_in[25:,:k+1]
    Yin = Y_in[25:,:k+1]
    Xout = X_out[:,:k+1]
    Yout = Y_out[:,:k+1]
    
    # in sample calculation
    Xin_dagger=np.dot(np.linalg.pinv(np.dot(Xin.T,Xin)),Xin.T)
    win = np.dot(Xin_dagger,Yin)
    
    g_of_xin = np.sign((win.T).dot(Xin.T))
    p_in  = np.mean((g_of_xin != Yin.T).astype(int))
    
    # validation calculation
    g_of_xv = np.sign((win.T).dot(Xv.T))
    p_v  = np.mean((g_of_xv != Yv.T).astype(int))

    # out of sample calculation
    g_of_xout = np.sign((win.T).dot(Xout.T))
    p_out  = np.mean((g_of_xout != Yout.T).astype(int))
    
    print("--k:",k," -- p_in",p_in, "p_v",p_v, "p_out",p_out)

print("\nproblem 5 ================================================")
pts = [(0.0,0.1),(0.1,0.2),(0.1,0.3),(0.2,0.2),(0.2,0.3)]
p_out_p1_p3 =[ (0.084,0.192)]
print(cdist(pts, p_out_p1_p3, 'euclidean'))

print("\nproblem 6 ================================================")
N = 100000000
e1 = np.random.uniform(0,1,N)
e2 = np.random.uniform(0,1,N)
e = np.minimum(e1,e2)

print(np.mean(e1))
print(np.mean(e2))
print(np.mean(e))



