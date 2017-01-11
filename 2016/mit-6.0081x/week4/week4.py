# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 20:07:55 2016

@author: bicepjai
"""

import numpy as np
import scipy as sci

# Mutual Information 
#https://courses.edx.org/courses/course-v1:MITx+6.008.1x+3T2016/courseware/1__Probability_and_Inference/info_measures/
joint_prob_XY = np.array([[0.10, 0.09, 0.11], [0.08, 0.07, 0.07], [0.18, 0.13, 0.17]])

prob_X = joint_prob_XY.sum(axis=1)
prob_Y = joint_prob_XY.sum(axis=0)

joint_prob_XY_indep = np.outer(prob_X, prob_Y)

nof_questions = np.log2(np.divide(joint_prob_XY, joint_prob_XY_indep))
entropy_matrix = np.multiply(joint_prob_XY,nof_questions)
mutual_info_XY = np.sum(entropy_matrix)

# solution given
def info_divergence(p, q):
    return np.sum(p * np.log2(p / q))
    
print(entropy_matrix)
print(mutual_info_XY)

# homework3
# Ainsley Works on Problem Sets 
print("Ainsley Works on Problem Sets ")
ss = [1,2,3,4]
cs = [0,1,2,3,4,5,6,7,8]
ds = [0,1,2,3,4]

P_D_given_S = lambda s,q,d: sci.misc.comb(s,d) * np.power(q, d) * np.power(1-q, s-d) if d in ds else 0
E_C_given_S = lambda s: sum([c/(2.0*s + 1) for c in range(0,2*s+1)])
P_S = 1.0/4.0

P_D = lambda d,q: sum([P_D_given_S(s,q,d) * P_S for s in ss ])

E_C_given_D = lambda q,d: sum([ E_C_given_S(s) * P_D_given_S(s,q,d) * P_S / P_D(d,q) for s in ss])

print("\n-----------verifications:")
print("E_C_given_S")
print([E_C_given_S(s) for s in ss])

print("\ntest1: ")
q_given = 0.2
d_given = 2
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

q_given = 0.2
d_given = 3
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

q_given = 0.5
d_given = 1
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

d_given = 3
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

q_given = 0.7
d_given = 1
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

d_given = 2
print("q: ",q_given,"d: ",d_given)
print("P_D: ", P_D(d_given,q_given))
print("E_C_given_D", E_C_given_D(q_given,d_given))

print("\n==========Answers")
print (E_C_given_D(0.2,1))
print (E_C_given_D(0.5,2))
print (E_C_given_D(0.7,3))
