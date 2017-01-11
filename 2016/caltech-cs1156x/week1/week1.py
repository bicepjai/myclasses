# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 21:30:05 2016

@author: bicepjai
"""

import numpy as np
import matplotlib.pyplot as plt
import random

runs = 100
avg_iterations = 0
avg_P = 0.0
N = 100
total_iteration = 1000
plot_graph = False
run_percent = 0.1

for run in range(0,runs):
    
    # generating the target function
    # comprising 2 (x,y) points
    x1,y1,x2,y2 = np.random.uniform(-1,1,4)
    RightOrLeft = lambda x,y: np.sign((x2 - x1)*y - (y2 - y1)*x + x1*y2 - x2*y1)
    
    # generate N random data points
    xn = []
    yn = np.zeros(0)
    
    # generate valid left(+1) or right(-1) values
    for i in range(0,N):
        x,y = np.random.uniform(-1,1,2)
        xn += [(x,y)]
        yn = np.append(yn, RightOrLeft(x,y))
   
    if(plot_graph):
        # plotting training line
        # pla.plot([x1,x2], [y1,y2])
        # extending the line    
        xrange = np.arange(-1.2,1.2,0.2)
        tx = [x1,x2]
        ty = [y1,y2]
        A = np.vstack([tx, np.ones(len(tx))]).T
        k, b = np.linalg.lstsq(A, ty)[0]
        plt.plot(xrange, k*xrange + b, 'm')
    
        # plotting the points
        right_xs = [x for i,(x,y) in enumerate(xn) if(yn[i] == -1)]
        right_ys = [y for i,(x,y) in enumerate(xn) if(yn[i] == -1)]
        left_xs  = [x for i,(x,y) in enumerate(xn) if(yn[i] == 1)]
        left_ys  = [y for i,(x,y) in enumerate(xn) if(yn[i] == 1)]
        plt.plot(right_xs, right_ys, 'bs')
        plt.plot(left_xs, left_ys, 'rs')
        plt.axis([-1, 1, -1, 1])
        # plt.show()
    
    # w vectors
    w = np.zeros(3)
    
    # PLA
    P = 0
    iterations = 0
    for i in range(0,total_iteration):
        iterations = i
        # print("\n--- Iteration "+ str(i) +"---")
        missclassified_xjs = []
        hn = np.zeros(0)

        for j in range(0,N):
            xj = np.array([ 1, xn[j][0],  xn[j][1] ])
            h = np.sign((w.transpose()).dot(xj))
            hn = np.append(hn, h)
            
            # misclassified
            if(yn[j] != h):
                missclassified_xjs += [(xj, yn[j])]
        
        if(len(missclassified_xjs) == 0):
            # print ("converged!")
            break
        
        rx, ry = random.choice(missclassified_xjs)
        w += rx * ry

        p = len(missclassified_xjs)/N
        P += p
        # print ("P[f!=g]: " + str(p))
    
    if(plot_graph):
        # plotting the weights trained
        txo = np.array(range(-2,2))# extended line
        tyo = eval('(-( txo * w[1] + w[0])/w[2])')
        plt.plot(txo, tyo, 'k-')  
        plt.show()
        
    avg_iterations += iterations
    avg_P += (P/iterations)
    # print ("\nResults for " + str(run) + ": ")
    # print ("Total test points: "+ str(N))
    # print ("total_iteration: " + str(iterations))
    # print ("P[f!=g]: " + str(P/total_iteration))

print ("avg_iterations: "+str(avg_iterations/runs))
print ("P[f!=g]: " + str(avg_P/runs))