# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 19:25:07 2016

@author: bicepjai
"""
import comp_prob_inference

prob_table = {('sunny', 'hot'): 3/10,
     ('sunny', 'cold'): 1/5,
     ('rainy', 'hot'): 1/30,
     ('rainy', 'cold'): 2/15,
     ('snowy', 'hot'): 0,
     ('snowy', 'cold'): 1/3}

prob_table[('rainy', 'cold')]

prob_W_T_dict = {}
for w in {'sunny', 'rainy', 'snowy'}:
    prob_W_T_dict[w] = {}
prob_W_T_dict['sunny']['hot'] = 3/10
prob_W_T_dict['sunny']['cold'] = 1/5
prob_W_T_dict['rainy']['hot'] = 1/30
prob_W_T_dict['rainy']['cold'] = 2/15
prob_W_T_dict['snowy']['hot'] = 0
prob_W_T_dict['snowy']['cold'] = 1/3

comp_prob_inference.print_joint_prob_table_dict(prob_W_T_dict)

prob_W_T_dict['rainy']['cold']

import numpy as np
prob_W_T_rows = ['sunny', 'rainy', 'snowy']
prob_W_T_cols = ['hot', 'cold']
prob_W_T_array = np.array([[3/10, 1/5], [1/30, 2/15], [0, 1/3]])
comp_prob_inference.print_joint_prob_table_array(prob_W_T_array, prob_W_T_rows, prob_W_T_cols)

prob_W_T_array[prob_W_T_rows.index('rainy'), prob_W_T_cols.index('cold')]
    
prob_W_T_rows = ['sunny', 'rainy', 'snowy']
prob_W_T_cols = ['hot', 'cold']
prob_W_T_row_mapping = {label: index for index, label in enumerate(prob_W_T_rows)}
prob_W_T_col_mapping = {label: index for index, label in enumerate(prob_W_T_cols)}
prob_W_T_array = np.array([[3/10, 1/5], [1/30, 2/15], [0, 1/3]])
#prob_W_T_array[prob_W_T_row_mapping[w], prob_W_T_col_mapping[t]]

prob_W_I_dict = {}
for w in {'sunny', 'rainy', 'snowy'}:
    prob_W_T_dict[w] = {}
prob_W_I_dict['sunny'][1] = 1/2
prob_W_I_dict['sunny'][0] = 0
prob_W_I_dict['rainy'][1] = 0
prob_W_I_dict['rainy'][0] = 1/6
prob_W_I_dict['snowy'][1] = 0
prob_W_I_dict['snowy'][0] = 1/3

print (prob_W_I_dict)

prob_X_Y_dict = {}
for w in {'sunny', 'rainy', 'snowy'}:
    prob_X_Y_dict[w] = {}
prob_X_Y_dict['sunny'][1] = 1/4
prob_X_Y_dict['sunny'][0] = 1/4
prob_X_Y_dict['rainy'][1] = 1/12
prob_X_Y_dict['rainy'][0] = 1/12
prob_X_Y_dict['snowy'][1] = 1/6
prob_X_Y_dict['snowy'][0] = 1/6

print (prob_X_Y_dict)
print ({k:sum(v.values()) for (k,v) in (prob_X_Y_dict.items())})

P_Y = {}
for (k,v) in (prob_X_Y_dict.items()):
    for (k1,v1) in (v.items()):
        if(k1 not in P_Y):
            P_Y[k1] = v1
        else:
            P_Y[k1] += v1

print(P_Y)

from simpsons_paradox_data import *
print(simpsons_paradox_data.prob_space)
print(simpsons_paradox_data.joint_prob_table[gender_mapping['female'], department_mapping['C'], admission_mapping['admitted']])

joint_prob_gender_admission = simpsons_paradox_data.joint_prob_table.sum(axis=1)
print(joint_prob_gender_admission)
print(joint_prob_gender_admission[gender_mapping['female'], admission_mapping['admitted']])

female_only = joint_prob_gender_admission[gender_mapping['female']]
prob_admission_given_female = female_only / np.sum(female_only)
prob_admission_given_female_dict = dict(zip(admission_labels, prob_admission_given_female))
print(prob_admission_given_female_dict)

male_only = joint_prob_gender_admission[gender_mapping['male']]
prob_admission_given_male = male_only / np.sum(male_only)
prob_admission_given_male_dict = dict(zip(admission_labels, prob_admission_given_male))
print(prob_admission_given_male_dict)

admitted_only = joint_prob_gender_admission[:, admission_mapping['admitted']]
prob_gender_given_admitted = admitted_only / np.sum(admitted_only)
prob_gender_given_admitted_dict = dict(zip(gender_labels, prob_gender_given_admitted))
print(prob_gender_given_admitted_dict)

#------------------------------------------
for d in department_mapping:
    print("Department: "+d)
    female_and_d_only = joint_prob_table[gender_mapping['female'], department_mapping[d]]
    prob_female_and_d = female_and_d_only / np.sum(female_and_d_only)
    prob_admitted_female_and_d_dict = dict(zip(admission_labels, prob_female_and_d))
    print("Gender: Female")
    print(prob_admitted_female_and_d_dict)
    
    male_and_d_only = joint_prob_table[gender_mapping['male'], department_mapping[d]]
    prob_male_and_d = male_and_d_only / np.sum(male_and_d_only)
    prob_admitted_male_and_d_dict = dict(zip(admission_labels, prob_male_and_d))
    print("Gender: Male")
    print(prob_admitted_male_and_d_dict)
    
