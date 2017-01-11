# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 12:06:01 2016

@author: bicepjai
"""

import numpy as np
import matplotlib.pyplot as plt
import random


# fair coin
mu = 0.5

M = 1000 # nof coins
iterations = 100000
N = 10 #training samples

v_1_tot = 0
v_min_tot = 0
v_rand_tot = 0

mu_sub_nu_v_1s = np.zeros((1,iterations))
mu_sub_nu_v_rands = np.zeros((1,iterations))
mu_sub_nu_v_mins = np.zeros((1,iterations))

# experiment run
for i in range(0,iterations):
    virtual_coins = np.zeros((1,M))
    # independant F flips
    for flip in range(N):
        virtual_flips = np.random.uniform(0,1,M)
        virtual_coins = virtual_coins + (virtual_flips > 0.5).astype(int)
    
    c_1 = 1
    c_rand = random.randint(0,N-1)
    c_min = np.argmin(virtual_coins, axis=1)
    
    v_1 = virtual_coins[(0,c_1)] / N
    v_rand = virtual_coins[(0,c_rand)] / N
    v_min = virtual_coins[(0,c_min)] / N

    mu_sub_nu_v_1s[(0,i)]    = abs(mu - v_1)
    mu_sub_nu_v_rands[(0,i)] = abs(mu - v_rand)
    mu_sub_nu_v_mins[(0,i)]  = abs(mu - v_min)
    
    v_1_tot = v_1_tot + v_1
    v_rand_tot = v_rand_tot + v_rand
    v_min_tot = v_min_tot + v_min
    
#    print("-------------")
#    print("v_1: ", v_1)
#    print("v_rand: ", v_rand)
#    print("v_min: ", v_min)

    
print("==================")
print("v_1: ", v_1_tot / iterations)
print("v_rand: ", v_rand_tot / iterations)
print("v_min: ", v_min_tot / iterations)

# checking hoeffding on v_1
inequality_held_v_1 = 0
inequality_held_v_rand = 0
inequality_held_v_min = 0

for ep in np.arange(0, 1, 0.01):
    #hoeffding inequality RHS
    hoefd = 2 * np.exp(-2 * np.square(ep) * N)
    
    # v_1
    mu_sub_nu_lt_ep = np.sum((mu_sub_nu_v_1s > ep).astype(int))
    p_mu_sub_nu_lt_ep = mu_sub_nu_lt_ep / iterations
    if (p_mu_sub_nu_lt_ep <= hoefd):
        inequality_held_v_1 += 1

    # v_rand
    mu_sub_nu_lt_ep = np.sum((mu_sub_nu_v_rands > ep).astype(int))
    p_mu_sub_nu_lt_ep = mu_sub_nu_lt_ep / iterations
    if (p_mu_sub_nu_lt_ep <= hoefd):
        inequality_held_v_rand += 1

    # v_rand
    mu_sub_nu_lt_ep = np.sum((mu_sub_nu_v_mins > ep).astype(int))
    p_mu_sub_nu_lt_ep = mu_sub_nu_lt_ep / iterations
    if (p_mu_sub_nu_lt_ep <= hoefd):
        inequality_held_v_min += 1        
        

print("inequality_held_v_1: ", inequality_held_v_1)
print("inequality_held_v_rand: ", inequality_held_v_rand)
print("inequality_held_v_min: ", inequality_held_v_min)


#hoef_v_1s    = 2 * np.exp(-2 * np.square(ep_v_1s) * N)
#hoef_v_rands = 2 * np.exp(-2 * np.square(ep_v_rands) * N)
#hoef_v_mins  = 2 * np.exp(-2 * np.square(ep_v_mins) * N)

#plt.plot(ep_v_1s, hoef_v_1s, 'bo')
#plt.show()


    