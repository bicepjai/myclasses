# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:25:58 2016

@author: bicepjai
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import svm
import random

# problem 8,9
print("==========================")
print("problem 8,9,10")

plot_graph = False

def generate_2d_points(N, a, b, c, d):
    line_eqn = lambda x : ((d-b)/(c-a)) * (x - a) + b
    
    # generate N random data points
    X1 = np.random.uniform(-1,1,N)
    X2 = np.random.uniform(-1,1,N)

    # following manipulation to make the calculation of Y easy
    f_x1 = np.repeat(a, N)
    f_y1 = np.repeat(b, N)
    f_x2 = np.repeat(c, N)
    f_y2 = np.repeat(d, N)
    
    # for plotting
    # generate valid left(+1) or right(-1) values
    Y = np.sign((f_x2 - f_x1)*X2 - (f_y2 - f_y1)*X1 + f_x1*f_y2 - f_x2*f_y1)
    
    return (X1, X2, Y, line_eqn)

def compare_SVM_PLA(runs,N):
    
    support_vectors = []
    nof_support_vectors = [];
    svm_wins = 0

    for run in range(0,runs):
       
        # generating the target function
        # comprising 2 (x,y) points
        a,b,c,d = np.random.uniform(-1,1,4)
        X1, X2, Y_in, line_eqn_in = generate_2d_points(N, a, b, c, d)
        while(np.all(Y_in==1) or np.all(Y_in==-1)):
            X1, X2, Y_in, line_eqn_in = generate_2d_points(N, a, b, c, d)
        X_in = np.ones((N,3))
        X_in[:,1] = X1
        X_in[:,2] = X2
    
        if(plot_graph):
            # plotting targer hypothesis line
            xrange = np.arange(-1.2,1.2,0.2)
            plt.plot(xrange, [ line_eqn_in(x) for x in xrange], color='k', linestyle='-', linewidth=2)
        
            # plotting the points
            right_xs = X1[Y_in == -1]
            right_ys = X2[Y_in == -1]
            left_xs  = X1[Y_in == 1]
            left_ys  = X2[Y_in == 1]
            plt.plot(right_xs, right_ys, 'bs')
            plt.plot(left_xs, left_ys, 'rs')
            plt.axis([-1, 1, -1, 1])
            #plt.show()
        
        a,b,c,d = np.random.uniform(-1,1,4)
        X1, X2, Y_out, line_eqn_out = generate_2d_points(N, a, b, c, d)
        while(np.all(Y_out==1) or np.all(Y_out==-1)):
            X1, X2, Y_out, line_eqn_out = generate_2d_points(N, a, b, c, d)
        X_out = np.ones((N,3))
        X_out[:,1] = X1
        X_out[:,2] = X2
        
        # w vectors
        w_pla = np.zeros(3)
    
        # ----------------------- PLA
        while(True):                
            misclassified_xjs = []
        
            for j in range(0,N):
                h = np.sign((w_pla.T).dot(X_in[j]))
                
                # misclassified
                if(Y_in[j] != h):
                    misclassified_xjs += [(X_in[j], Y_in[j])]
            
            if(len(misclassified_xjs) == 0):
                # print ("converged!")
                break
            rx, ry = random.choice(misclassified_xjs)
            w_pla += rx * ry
        
        # predicting PLA
        Y_pla = np.sign(np.expand_dims(w_pla,0).dot(X_out.T))
        p_out_pla  = np.mean((Y_pla != Y_out).astype(int))
    
        if(plot_graph):
            # plotting trained line
            # extending the line    
            xrange = np.arange(-1.2,1.2,0.2)
            out_line_eqn = lambda x,w: (-w[0] - w[1] * x)/w[2]
            yrange = [ out_line_eqn(x,w_pla) for x in xrange]
            plt.plot(xrange, yrange, color='r', linestyle='-', linewidth=2)
            # plt.show()
    
        # ----------------------- SVM

        model_svm = svm.SVC(kernel='linear')
        model_svm.fit(X_in,Y_in)
        w_svm = model_svm.coef_[0] + model_svm.intercept_

        # predicting SVM
        Y_svm = model_svm.predict(X_out)
        p_out_svm  = np.mean((Y_svm != Y_out).astype(int))

        if(plot_graph):
            # plotting trained line
            # extending the line    
            xrange = np.arange(-1.2,1.2,0.2)
            out_line_eqn = lambda x,w: (-w[0] - w[1] * x)/w[2]
            yrange = [ out_line_eqn(x,w_svm) for x in xrange]
            plt.plot(xrange, yrange, color='m', linestyle='-', linewidth=2)
            plt.show()
            
        # ----------------------- winner
        if p_out_svm < p_out_pla:
            svm_wins += 1
            nof_support_vectors.append(len(model_svm.n_support_))
            support_vectors += [np.sum(model_svm.n_support_)]
    
    
    print("N",N,"runs",runs,"svm_win_%",svm_wins/float(runs),"nof_support_vectors",np.mean(nof_support_vectors))

plot_graph = True
compare_SVM_PLA(runs=1,N=100)

#plot_graph = False
#compare_SVM_PLA(runs=1000,N=10)
#compare_SVM_PLA(runs=1000,N=100)
    