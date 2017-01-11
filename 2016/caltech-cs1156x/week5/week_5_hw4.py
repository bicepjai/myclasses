# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 21:30:05 2016

@author: bicepjai
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

# problem 8,9
print("==========================")
print("problem 8,9")

N = 100
runs = 100
epochs = 1000
plot_graph = False
eta = 0.01
threshold = 0.01

runs_epochs = []
runs_eouts = []
  
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

for run in range(0,runs):
   
    # generating the target function
    # comprising 2 (x,y) points
    a,b,c,d = np.random.uniform(-1,1,4)
    X1, X2, Yin, line_eqn = generate_2d_points(N, a, b, c, d)
   
    if(plot_graph):
        # plotting targer hypothesis line
        xrange = np.arange(-1.2,1.2,0.2)
        plt.plot(xrange, [ line_eqn(x) for x in xrange], color='k', linestyle='-', linewidth=2)
    
        # plotting the points
        right_xs = X1[Yin == -1]
        right_ys = X2[Yin == -1]
        left_xs  = X1[Yin == 1]
        left_ys  = X2[Yin == 1]
        plt.plot(right_xs, right_ys, 'bs')
        plt.plot(left_xs, left_ys, 'rs')
        plt.axis([-1, 1, -1, 1])
        # plt.show()

    # Logistic Regression
    w = np.zeros((1,3))
    w_prev = np.zeros((1,3))
    epoch = 0
    x_indices = np.arange(N)

    while(True):
        epoch = epoch + 1
        
        np.random.shuffle(x_indices)
        
        X = np.ones((N,3))
        X[:,1] = X1[x_indices]
        X[:,2] = X2[x_indices]
        Y = np.expand_dims(Yin[x_indices],0)
        
        # calculation of delta E_in
        Y_W_Xn = Y.T * np.dot(X,w.T)
        Y_Xn = Y.T * X
        Y_Xn_by_one_plus_exp_Y_W_Xn = -1 * Y_Xn / (1 + np.exp(Y_W_Xn))
        delta_Ein = np.sum(Y_Xn_by_one_plus_exp_Y_W_Xn, 0)
        # here we are considerign only one data point at a time

        # w update        
        w = w - eta * delta_Ein
        
        if(np.linalg.norm(w_prev - w) < threshold):
            # print("w_prev - w: ",np.linalg.norm(w_prev - w))
            break
        
        if(epochs > 0 and epoch > epochs):
            # print("exceeded epochs:",epochs,"w_prev - w: ",np.linalg.norm(w_prev - w))
            break
        
        w_prev = w

    if(plot_graph):
        # plotting trained line
        # extending the line    
        xrange = np.arange(-1.2,1.2,0.2)
        out_line_eqn = lambda x,w: (-w[0,0] - w[0,1] * x)/w[0,2]
        plt.plot(xrange, [ out_line_eqn(x,w) for x in xrange], color='r', linestyle='-', linewidth=2)
        plt.show()
        
    runs_epochs.append(epoch)
    
    # eout calculataion for out of sample
    # generate N random data points
    X_out = np.ones((N,3))
    X_out[:,1], X_out[:,2], Y_out, line_eqn = generate_2d_points(N, a, b, c, d)
        
    exp_term = -np.expand_dims(Y_out,0).T * np.dot(X_out,w.T)
    log_one_plus_exp = np.log(1 + np.exp(exp_term))
    E_out = np.mean(log_one_plus_exp)
    runs_eouts.append(E_out)
    
        
print("epochs: ",np.mean(runs_epochs))  
print("E_out: ",np.mean(runs_eouts))  

    
#    if(plot_graph):
        # plotting the weights trained
#        x1s = np.array(range(-2,2))# extended line
#        x2s = eval('(-( x1s * w[1] + w[0])/w[2])')
#        plt.plot(x1s, x2s, 'k-')  
#        plt.show()
