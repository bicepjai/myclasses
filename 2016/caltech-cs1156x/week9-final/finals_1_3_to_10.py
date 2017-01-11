import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

from sklearn import svm

features_train = np.loadtxt("data/features.train")
features_test  = np.loadtxt("data/features.test")
R_train,C_train = features_train.shape
R_test,C_test = features_test.shape

print("==========================")
print("problem 1")
Q = 10
nof_terms = 0
for s in range(1,Q+1):
    for i in range(Q+1):
        for j in range(Q+1):
            if(i+j == s):
                # print (i,"+",j,"=",s)
                nof_terms += 1

print ("Q",Q,"nof_terms",nof_terms)

def one_vs_all(X_in, Y_in, X_out, Y_out, digit, l, z_d):
    # linear regression with regularizer
    
    # in sample calculation
    X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + l * np.eye(z_d))
    X_in_dagger=np.dot(X_XT_in,X_in.T)
    w_in = np.dot(X_in_dagger,Y_in)
    
    g_of_x_in = np.sign((w_in.T).dot(X_in.T))
    p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))
    
    # out of sample calculation
    g_of_x_out = np.sign((w_in.T).dot(X_out.T))
    p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))
    
    print("digit:",digit,"E_in:",p_in,"E_out:",p_out)
    return (p_in, p_out)
    

digits = [0,1,2,3,4,5,6,7,8,9]

# index are digits
# variables used for 9
e_out_with_z = []
e_out_without_z = []

print("==========================")
print("problem 7,9")

N_in,C_in = features_train.shape
X_in = np.ones((N_in,3))
X_in[:,1] = features_train[:,1]
X_in[:,2] = features_train[:,2]

N_out,C_out = features_test.shape
X_out = np.ones((N_out,3))
X_out[:,1] = features_test[:,1]
X_out[:,2] = features_test[:,2]

lam = 1
z_d = 3
for digit in digits:
    
    Y_in = -1*np.ones(N_in)
    Y_in[features_train[:,0] == digit] = 1.0
    
    Y_out = -1*np.ones(N_out)
    Y_out[features_test[:,0] == digit] = 1.0
    
    p_in, p_out = one_vs_all(X_in, Y_in, X_out, Y_out, digit, lam, z_d)
    e_out_without_z.append(p_out)
    
print("==========================")
print("problem 8,9")

N_in,C_in = features_train.shape
X_in = np.ones((N_in,6))
X_in[:,1] = features_train[:,1]
X_in[:,2] = features_train[:,2]
X_in[:,3] = features_train[:,1] *  features_train[:,2]
X_in[:,4] = np.square(features_train[:,1])
X_in[:,5] = np.square(features_train[:,2])

N_out,C_out = features_test.shape
X_out = np.ones((N_out,6))
X_out[:,1] = features_test[:,1]
X_out[:,2] = features_test[:,2]
X_out[:,3] = features_test[:,1] *  features_test[:,2]
X_out[:,4] = np.square(features_test[:,1])
X_out[:,5] = np.square(features_test[:,2])

lam = 1
z_d = 6
for digit in digits:
    
    Y_in = -1*np.ones(N_in)
    Y_in[features_train[:,0] == digit] = 1.0
    
    Y_out = -1*np.ones(N_out)
    Y_out[features_test[:,0] == digit] = 1.0
    
    p_in, p_out = one_vs_all(X_in, Y_in, X_out, Y_out, digit, lam, z_d)
    e_out_with_z.append(p_out)
    
print("==========================")
print("problem 9")

for digit in digits:
    p_out = e_out_without_z[digit]
    p_out_z = e_out_with_z[digit]
    diff = (p_out_z - p_out)/p_out_z
    print("digit:",digit,"p_out  :",p_out,"p_out_z:",p_out_z,"improvement:",diff)

print("==========================")
print("problem 10")
z_d = 6
digit1 = 1
digit2 = 5
#feature train
X_in_d1 = features_train[features_train[:,0] == digit1]
X_in_d2 = features_train[features_train[:,0] == digit2]
X_in_d1_d2 = np.vstack([X_in_d1,X_in_d2])

N_in,C_in = X_in_d1_d2.shape
X_in = np.ones((N_in,6))
X_in[:,1] = X_in_d1_d2[:,1]
X_in[:,2] = X_in_d1_d2[:,2]
X_in[:,3] = X_in_d1_d2[:,1] *  X_in_d1_d2[:,2]
X_in[:,4] = np.square(X_in_d1_d2[:,1])
X_in[:,5] = np.square(X_in_d1_d2[:,2])

Y_in = -1*np.ones(N_in)
Y_in[X_in_d1_d2[:,0] == digit1] = 1.0

# feature test
X_out_d1 = features_test[features_test[:,0] == digit1]
X_out_d2 = features_test[features_test[:,0] == digit2]
X_out_d1_d2 = np.vstack([X_out_d1,X_out_d2])

N_out,C_out = X_out_d1_d2.shape
X_out = np.ones((N_out,6))
X_out[:,1] = X_out_d1_d2[:,1]
X_out[:,2] = X_out_d1_d2[:,2]
X_out[:,3] = X_out_d1_d2[:,1] *  X_out_d1_d2[:,2]
X_out[:,4] = np.square(X_out_d1_d2[:,1])
X_out[:,5] = np.square(X_out_d1_d2[:,2])

Y_out = -1*np.ones(N_out)
Y_out[X_out_d1_d2[:,0] == digit1] = 1.0

lams = [0.01,1]
# linear regression with regularizer
for lam in lams:
    # in sample calculation
    X_XT_in = np.linalg.pinv(np.dot(X_in.T,X_in) + lam * np.eye(z_d))
    X_in_dagger=np.dot(X_XT_in,X_in.T)
    w_in = np.dot(X_in_dagger,Y_in)
    
    g_of_x_in = np.sign((w_in.T).dot(X_in.T))
    p_in  = np.mean((g_of_x_in != Y_in.T).astype(int))
    
    # out of sample calculation
    g_of_x_out = np.sign((w_in.T).dot(X_out.T))
    p_out  = np.mean((g_of_x_out != Y_out.T).astype(int))
    
    print("lam:",lam,"E_in:",p_in,"E_out:",p_out)
    

