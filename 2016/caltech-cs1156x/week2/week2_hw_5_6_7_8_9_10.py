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
        A = np.vstack([tx, np.ones(len(tx))]).T
        k, b = np.linalg.lstsq(A, ty)[0]
        plt.plot(xrange, k*xrange + b, 'm')
    
        # plotting the points
        right_xs = X1[Y == -1]
        right_ys = X2[Y == -1]
        left_xs  = X1[Y == 1]
        left_ys  = X2[Y == 1]
        plt.plot(right_xs, right_ys, 'bs')
        plt.plot(left_xs, left_ys, 'rs')
        plt.axis([-1, 1, -1, 1])
        # plt.show()
    
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


# problem 6
print("==========================")
print("problem 6")
N = 1000
total_P = 0
for i in range(0,total_iteration):
    
    # generating the target function
    # comprising 2 (x,y) points
    f_x1 = np.repeat(x1[i], N)
    f_y1 = np.repeat(y1[i], N)
    f_x2 = np.repeat(x2[i], N)
    f_y2 = np.repeat(y2[i], N)
    
    # generate N random data points
    X1 = np.random.uniform(-1,1,N)
    X2 = np.random.uniform(-1,1,N)
    # generate valid left(+1) or right(-1) values
    Y = np.sign((f_x2 - f_x1)*X2 - (f_y2 - f_y1)*X1 + f_x1*f_y2 - f_x2*f_y1)

    # setting up X
    X = np.ones((N,3))
    X[:,1] = X1
    X[:,2] = X2
    Y.shape = (N,1)
    
    # measuring correct classification
    g_of_x = np.sign((w[i].T).dot(X.T))
    misclassified_pts  = np.sum((g_of_x != Y.T).astype(int))
    p = misclassified_pts / N
    total_P += p

print("P(incorrectly classified out of sample): ", total_P/total_iteration)  


#problem 7
print("==========================")
print("problem 7")
N = 10
runs = 100
P = 0
for run in range(runs):

    iterations_used_total = 0
    total_P = 0
    wi = w[i]
    wi.shape = (1,3)
    
    for i in range(0,total_iteration):
        iterations = i+1
        
        # generating the target function
        # comprising 2 (x,y) points
        f_x1 = np.repeat(x1[i], N)
        f_y1 = np.repeat(y1[i], N)
        f_x2 = np.repeat(x2[i], N)
        f_y2 = np.repeat(y2[i], N)
        
        # generate N random data points
        X1 = np.random.uniform(-1,1,N)
        X2 = np.random.uniform(-1,1,N)
        # generate valid left(+1) or right(-1) values
        Y = np.sign((f_x2 - f_x1)*X2 - (f_y2 - f_y1)*X1 + f_x1*f_y2 - f_x2*f_y1)
        
        missclassified_xjs = []
        for j in range(0,N):
            xj = np.array([ 1, X1[j],  X2[j] ])
            h = np.sign((wi).dot(xj))
                
            # misclassified
            if(Y[j] != h):
                missclassified_xjs += [(xj, Y[j])]
            
        if(len(missclassified_xjs) == 0):
            # print ("converged!")
            break
            
        rx, ry = random.choice(missclassified_xjs)
        wi += rx * ry
    
        p = len(missclassified_xjs)/N
        total_P += p
        
    if(plot_graph):
        # plotting the weights trained
        txo = np.array(range(-2,2))# extended line
        tyo = eval('(-( txo * w[1] + w[0])/w[2])')
        plt.plot(txo, tyo, 'k-')  
        plt.show()
            
    iterations_used_total += iterations
    P += (total_P/iterations)

print ("avg_iterations: "+str(iterations_used_total/runs))
print ("P[f!=g]: " + str(P/runs))

# problem 8
print("==========================")
print("problem 8")

noise_percentage = 10
total_P = 0.0
N = 1000
noise_sample_size = int(N*noise_percentage/100)
total_iteration = 1000
plot_graph = False
w = []
for i in range(0,total_iteration):
    
    # generate N random data points
    X = np.ones((N,3))
    X[:,1] = np.random.uniform(-1,1,N)
    X[:,2] = np.random.uniform(-1,1,N)

    # non linear target function
    Y = np.sign(np.square(X[:,1]) + np.square(X[:,2]) - 0.6)
    noise_indices = np.random.randint(N, size=noise_sample_size)
    Y[noise_indices] = -1 * Y[noise_indices]
    
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
        right_xs = X1[Y == -1]
        right_ys = X2[Y == -1]
        left_xs  = X1[Y == 1]
        left_ys  = X2[Y == 1]
        plt.plot(right_xs, right_ys, 'bs')
        plt.plot(left_xs, left_ys, 'rs')
        plt.axis([-1, 1, -1, 1])
        # plt.show()
    
    # Linear Regression
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

# problem 9
print("==========================")
print("problem 9")

total_P = 0.0
N = 1000
total_iteration = 10
plot_graph = False

w = []
X = np.ones((N,6))
Y = None
total_w = np.zeros(6)

for i in range(0,total_iteration):
    
    # generate N random data points
    X[:,1] = np.random.uniform(-1,1,N)
    X[:,2] = np.random.uniform(-1,1,N)
    X[:,3] = X[:,1] * X[:,2]
    X[:,4] = np.square(X[:,1])
    X[:,5] = np.square(X[:,2])

    # non linear target function
    Y = np.sign(np.square(X[:,1]) + np.square(X[:,2]) - 0.6)
    
    # Linear Regression
    # g function
    w.append((np.linalg.lstsq(X,Y))[0])

    # measuring correct classification
    g_of_x = np.sign((w[i].T).dot(X.T))
    misclassified_pts  = np.sum((g_of_x != Y.T).astype(int))
    p = misclassified_pts / N
    total_P += p
    total_w += w[i]

avg_w = total_w / total_iteration
print(avg_w.shape)
print("P(incorrectly classified in sample): ", total_P/total_iteration)
print("w: ", avg_w)
 
if(plot_graph):
    # plotting the points
    right_xs = X[:,1][Y == -1]
    right_ys = X[:,2][Y == -1]
    left_xs  = X[:,1][Y == 1]
    left_ys  = X[:,2][Y == 1]
    plt.plot(right_xs, right_ys, 'bs')
    plt.plot(left_xs, left_ys, 'rs')
    plt.axis([-1, 1, -1, 1])
    
    # delta = 0.001
    # xx, yy = np.meshgrid(np.arange(-1, 1, delta), np.arange(-1, 1, delta))
    # zz = w0 + w1 * xx + w2 * x2 + w3 * np.multiply(xx, yy)
    # plt.contour(xx, yy, zz, 0)
    
    M = 10
    X1 = np.ones((M,6))
    X1[:,1] = np.random.uniform(-1,1,M)
    X1[:,2] = np.random.uniform(-1,1,M)
    X1[:,3] = X1[:,1] * X1[:,2]
    X1[:,4] = np.square(X1[:,1])
    X1[:,5] = np.square(X1[:,2])
    Y1 = np.sign((avg_w.T).dot(X1.T))
    right_xs = X1[:,1][Y1 == -1]
    right_ys = X1[:,2][Y1 == -1]
    left_xs  = X1[:,1][Y1 == 1]
    left_ys  = X1[:,2][Y1 == 1]
    plt.plot(right_xs, right_ys, 'rs')
    plt.plot(left_xs, left_ys, 'ko')
    plt.show()
        

# problem 10
print("==========================")
print("problem 10")  
# estimating nearnest to eh provided choices
total_iteration = 1000
avg_w.shape = (1,6)
N = 1000
X = np.ones((N,6))
hchs = np.array([
                        [-1, -0.05, 0.08, 0.13, 1.5,  1.5],
                        [-1, -0.05, 0.08, 0.13, 1.5,  15],
                        [-1, -0.05, 0.08, 0.13, 15,  1.5],
                        [-1, -1.5,  0.08, 0.13, 0.05, 0.05],
                        [-1, -0.05, 0.08, 1.5,  0.15, 0.15],
                     ])
total_mismatch = np.zeros(5)
for i in range(0,total_iteration):
    # generate N random data points
    X[:,1] = np.random.uniform(-1,1,N)
    X[:,2] = np.random.uniform(-1,1,N)
    X[:,3] = X[:,1] * X[:,2]
    X[:,4] = np.square(X[:,1])
    X[:,5] = np.square(X[:,2])

    # applying hypothesis
    avg_w_gx = np.sign((avg_w).dot(X.T))
    noise_indices = np.random.randint(N, size=noise_sample_size)
    avg_w_gx[0,noise_indices] = -1 * avg_w_gx[0,noise_indices]
    
    hchs_gx = np.sign(hchs.dot(X.T))

    # measuring correct classification
    non_matching = np.sum((hchs_gx != avg_w_gx).astype(int), axis=1)
    total_mismatch += non_matching


print(total_mismatch/(N*total_iteration))
    
