# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import comp_prob_inference
comp_prob_inference.flip_fair_coin()
flips = comp_prob_inference.flip_fair_coins(100)
comp_prob_inference.plot_discrete_histogram(flips)
comp_prob_inference.plot_discrete_histogram(flips, frequency=True)

n = 100000
heads_so_far = 0
fraction_of_heads = []
for i in range(n):
    if comp_prob_inference.flip_fair_coin() == 'heads':
        heads_so_far += 1
    fraction_of_heads.append(heads_so_far / (i+1))
    

import matplotlib.pyplot as plt
plt.figure(figsize=(8, 4))
plt.plot(range(1, n+1), fraction_of_heads)
plt.xlabel('Number of flips')
plt.ylabel('Fraction of heads')

prob_space = {'sunny': 1/2, 'rainy': 1/6, 'snowy': 1/3}
W_mapping = {'sunny': 'sunny', 'rainy': 'rainy', 'snowy': 'snowy'}
I_mapping = {'sunny': 1, 'rainy': 0, 'snowy': 0}
random_outcome = comp_prob_inference.sample_from_finite_probability_space(prob_space)
W = W_mapping[random_outcome]
I = I_mapping[random_outcome]
print(W,I)

W_table = {'sunny': 1/2, 'rainy': 1/6, 'snowy': 1/3}
I_table = {0: 1/2, 1: 1/2}
W = comp_prob_inference.sample_from_finite_probability_space(W_table)
I = comp_prob_inference.sample_from_finite_probability_space(I_table)
print(W,I)

pmf = {}
for d1 in range(1,7):
    for d2 in range(1,7):
        if d1+d2 in pmf:
            pmf[d1+d2] += 1/36
        else:
            pmf[d1+d2] = 1/36
print(pmf)
