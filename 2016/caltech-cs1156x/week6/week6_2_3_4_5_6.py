# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:36:21 2016

@author: bicepjai
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
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

# problem 2
print("\nproblem 2 ================================================")
# in sample calculation
X_in_dagger=np.dot(np.linalg.pinv(np.dot(X_in.T,X_in)),X_in.T)
w_in = np.dot(X_in_dagger,Y_in)

g_of_x_in = np.sign((w_in.T).dot(X_in.T))
p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))

# out of sample calculation
g_of_x_out = np.sign((w_in.T).dot(X_out.T))
p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))

print("---- p_in",p_in, "p_out",p_out)

lambda_k = lambda k: 10**k

# problem 3
print("\nproblem 3 ================================================")
k = -3

# in sample calculation
X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + lambda_k(k) * np.eye(8))
X_in_dagger=np.dot(X_XT_in,X_in.T)
w_in = np.dot(X_in_dagger,Y_in)

g_of_x_in = np.sign((w_in.T).dot(X_in.T))
p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))

# out of sample calculation
g_of_x_out = np.sign((w_in.T).dot(X_out.T))
p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))

print("lambda_k",k,"---- p_in",p_in, "p_out",p_out)


print("\nproblem 4 ================================================")
k = 3

# in sample calculation
X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + lambda_k(k) * np.eye(8))
X_in_dagger=np.dot(X_XT_in,X_in.T)
w_in = np.dot(X_in_dagger,Y_in)

g_of_x_in = np.sign((w_in.T).dot(X_in.T))
p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))

# out of sample calculation
g_of_x_out = np.sign((w_in.T).dot(X_out.T))
p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))

print("lambda_k",k,"---- p_in",p_in, "p_out",p_out)

print("\nproblem 5 ================================================")
ks = [2,1,0,-1,-2]

for k in ks:
    # in sample calculation
    X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + lambda_k(k) * np.eye(8))
    X_in_dagger=np.dot(X_XT_in,X_in.T)
    w_in = np.dot(X_in_dagger,Y_in)
    
    g_of_x_in = np.sign((w_in.T).dot(X_in.T))
    p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))
    
    # out of sample calculation
    g_of_x_out = np.sign((w_in.T).dot(X_out.T))
    p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))
    
    print("lambda_k",k,"---- p_in",p_in, "p_out",p_out)

print("\nproblem 6 ================================================")
ks = range(-5,5)

for k in ks:
    # in sample calculation
    X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + lambda_k(k) * np.eye(8))
    X_in_dagger=np.dot(X_XT_in,X_in.T)
    w_in = np.dot(X_in_dagger,Y_in)
    
    g_of_x_in = np.sign((w_in.T).dot(X_in.T))
    p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))
    
    # out of sample calculation
    g_of_x_out = np.sign((w_in.T).dot(X_out.T))
    p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))
    
    print("lambda_k",k,"---- p_in",p_in, "p_out",p_out)
    
    