# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 21:30:05 2016

@author: bicepjai
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random

x1,y1,x2,y2 =[],[],[],[]
w = [] 

# problem 5
print("==========================")
print("problem 5")

total_P = 0.0
N = 100
total_iteration = 1000
plot_graph = True

for i in range(0,total_iteration):
    
    # generating the target function
    # comprising 2 (x,y) points
    a,b,c,d = np.random.uniform(-1,1,4)

    x1.append(a)
    y1.append(b)
    x2.append(c)
    y2.append(d)
    
    f_x1 = np.repeat(x1[i], N)
    f_y1 = np.repeat(y1[i], N)
    f_x2 = np.repeat(x2[i], N)
    f_y2 = np.repeat(y2[i], N)
    
    # generate N random data points
    X1 = np.random.uniform(-1,1,N)
    X2 = np.random.uniform(-1,1,N)

    # RightOrLeft = lambda x,y: np.sign((x2 - x1)*y - (y2 - y1)*x + x1*y2 - x2*y1)
    # generate valid left(+1) or right(-1) values
    Y = np.sign((f_x2 - f_x1)*X2 - (f_y2 - f_y1)*X1 + f_x1*f_y2 - f_x2*f_y1)
    
   
    if(plot_graph):
        # plotting training line
        # pla.plot([x1,x2], [y1,y2])
        # extending the line    
        xrange = np.arange(-1.2,1.2,0.2)
        tx = [x1,x2]
        ty = [y1,y2]
        
#        A = np.vstack([tx, np.ones(len(tx))]).T
#        k, b = np.linalg.lstsq(A, ty)[0]
#        plt.plot(xrange, k*xrange + b, 'm')
    
        # plotting the points
        right_xs = X1[Y == -1]
        right_ys = X2[Y == -1]
        left_xs  = X1[Y == 1]
        left_ys  = X2[Y == 1]
        plt.plot(right_xs, right_ys, 'bs')
        plt.plot(left_xs, left_ys, 'rs')
        plt.axis([-1, 1, -1, 1])
        plt.show()
    
    # Linear Regression
    X = np.ones((N,3))
    X[:,1] = X1
    X[:,2] = X2
    Y.shape = (N,1)

    # g function
    w.append((np.linalg.lstsq(X,Y))[0])

    # measuring correct classification
    g_of_x = np.sign((w[i].T).dot(X.T))
    misclassified_pts  = np.sum((g_of_x != Y.T).astype(int))
    p = misclassified_pts / N
    total_P += p

    
    if(plot_graph):
        # plotting the weights trained
        x1s = np.array(range(-2,2))# extended line
        x2s = eval('(-( x1s * w[1] + w[0])/w[2])')
        plt.plot(x1s, x2s, 'k-')  
        plt.show()

print("P(incorrectly classified in sample): ", total_P/total_iteration)

