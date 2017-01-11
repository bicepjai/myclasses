import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

from sklearn import svm

# http://www.idryman.org/blog/2013/05/21/libsvm-on-mac-osx/

features_train = np.loadtxt("data/features.train")
features_test  = np.loadtxt("data/features.test")
R_train,C_train = features_train.shape
R_test,C_test = features_test.shape

def one_vs_all(digit, C, Q):
    X_in = features_train[:,1:3]
    Y_in = -1*np.ones(R_train)
    Y_in[features_train[:,0] == digit] = 1.0

    X_out = features_test[:,1:3]
    Y_out = -1*np.ones(R_test)
    Y_out[features_test[:,0] == digit] = 1.0    
    
    model_svm = svm.SVC(kernel='poly',coef0=1.0, gamma=1.0,degree=Q, C=C)
    model_svm.fit(X_in,Y_in)
    
    # predicting SVM
    Y_svm_in = model_svm.predict(X_in)
    p_in_svm  = np.mean((Y_svm_in != Y_in).astype(int))
    Y_svm_out = model_svm.predict(X_out)
    p_out_svm  = np.mean((Y_svm_out != Y_out).astype(int))    
    
    print("digit:",digit,"E_in:",p_in_svm,"E_out:",p_out_svm,"nof_sup_v:",len(model_svm.support_))

def one_vs_one(digit1, digit2, Q, C):
    #feature train
    X_in_d1 = features_train[features_train[:,0] == digit1]
    X_in_d2 = features_train[features_train[:,0] == digit2]
    X_in = np.vstack([X_in_d1,X_in_d2])
    
    R_d1_d2 = len(X_in_d1) + len(X_in_d2)
    
    Y_in = -1*np.ones(R_d1_d2)
    Y_in[X_in[:,0] == digit1] = 1.0

    X_in = X_in[:,1:3] # remove 1st col
    
    # feature test
    X_out_d1 = features_test[features_test[:,0] == digit1]
    X_out_d2 = features_test[features_test[:,0] == digit2]
    X_out = np.vstack([X_out_d1,X_out_d2])
    
    R_d1_d2 = len(X_out_d1) + len(X_out_d2)
    
    Y_out = -1*np.ones(R_d1_d2)
    Y_out[X_out[:,0] == digit1] = 1.0

    X_out = X_out[:,1:3] # remove 1st col
    
    model_svm = svm.SVC(kernel='poly',coef0=1.0, gamma=1.0,degree=Q, C=C)
    model_svm.fit(X_in,Y_in)
#    print(model_svm)
    
    # predicting SVM
    Y_svm_in = model_svm.predict(X_in)
    p_in_svm  = np.mean((Y_svm_in != Y_in).astype(int))
    Y_svm_out = model_svm.predict(X_out)
    p_out_svm  = np.mean((Y_svm_out != Y_out).astype(int))    
    
    print("=>",digit1,"vs",digit2," E_in:",p_in_svm,"E_out:",p_out_svm,"nof_sup_v:",len(model_svm.support_),"Q:",Q,"C:",C)


def get_data_one_vs_one(train, test, digit1, digit2):
    #train
    X_in_d1 = train[train[:,0] == digit1]
    X_in_d2 = train[train[:,0] == digit2]
    X_in = np.vstack([X_in_d1,X_in_d2])
    
    R_d1_d2 = len(X_in_d1) + len(X_in_d2)
    
    Y_in = -1*np.ones(R_d1_d2)
    Y_in[X_in[:,0] == digit1] = 1.0

    X_in = X_in[:,1:3] # remove 1st col
    
    # test
    X_out_d1 = test[test[:,0] == digit1]
    X_out_d2 = test[test[:,0] == digit2]
    X_out = np.vstack([X_out_d1,X_out_d2])
    
    R_d1_d2 = len(X_out_d1) + len(X_out_d2)
    
    Y_out = -1*np.ones(R_d1_d2)
    Y_out[X_out[:,0] == digit1] = 1.0

    X_out = X_out[:,1:3] # remove 1st col

    return   (X_in,Y_in,X_out,Y_out)
    
#print("==========================")
#print("problem 2,4")
#Q = 2
#C = 0.01
#digits = [0,2,4,6,8]
#for digit in digits:
#    one_vs_all(digit, C, Q)
#
#
#print("==========================")
#print("problem 3,4")
#Q = 2
#C = 0.01
#digits = [1,3,5,7,9]
#for digit in digits:
#    one_vs_all(digit, C, Q)


#print("==========================")
#print("problem 5")
#
#Q = 2
#Cs = [0.001,0.01,0.1,1]
#for C in Cs:
#        one_vs_one(1,5, Q, C)
#    
#print("==========================")
#print("problem 6")
#
#Qs = [2,5]
#Cs = [0.0001,0.001,0.01,1]
#for C in Cs:
#    for Q in Qs:
#        one_vs_one(1,5, Q, C)
        

print("==========================")
print("problem 7,8") # b(0.001),c(0.005)
Q = 2
Cs = {  0.0001:0, 0.001:0, 0.01:0, 0.1:0, 1:0}
#Cs = {  0.0002:0, 0.002:0, 0.02:0, 0.2:0, 2:0}
        
runs = 50

from sklearn.model_selection import KFold

Xd_train,Yd_train,Xd_test,Yd_test = get_data_one_vs_one(features_train, features_test, 1, 5)
kf = KFold(n_splits=10, shuffle=True)
    
for run in range(runs):

    # cv for C
    best_Ecv = np.inf
    best_C = 0
    E_cvs = []
    for C in Cs.keys():
        # n folds    
        for train_index, test_index in kf.split(Xd_train):
            X_in, Y_in = Xd_train[train_index], Yd_train[train_index]
            X_out, Y_out = Xd_train[test_index], Yd_train[test_index]
            
            model_svm = svm.SVC(kernel='poly',coef0=1.0, gamma=1.0,degree=Q, C=C)
            model_svm.fit(X_in,Y_in)
            
            # predicting SVM
            Y_svm_in = model_svm.predict(X_in)
            p_in_svm  = np.mean((Y_svm_in != Y_in).astype(int))
            Y_svm_out = model_svm.predict(X_out)
            p_val_svm  = np.mean((Y_svm_out != Y_out).astype(int))    
            
            # print(" E_in:",p_in_svm,"E_out:",p_val_svm,"nof_sup_v:",len(model_svm.support_))
        
            E_cvs.append(p_val_svm)
            
        avg_Ecv = np.mean(E_cvs)
        # print("Ecv",avg_Ecv,"C",C)
        
        if(avg_Ecv == best_Ecv):
            if(C < best_C):
                best_C = C
            best_Ecv = avg_Ecv
            
        elif(avg_Ecv < best_Ecv):
            best_Ecv = avg_Ecv
            best_C = C
        # print("==>best_Ecv",best_Ecv,"best_C",best_C)
        
    Cs[best_C] += 1 

print(Cs)

#print("==========================")
#print("problem 9, 10")
#
#Cs = [0.01,1,100,10000,1000000]
#for C in Cs:
#    model_svm = svm.SVC(kernel='rbf', gamma=1.0,C=C)
#    one_vs_one(1,5, model_svm)
#        
