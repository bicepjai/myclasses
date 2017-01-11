# version code f4bde2e5d0a5+
coursera = 1
# Please fill out this stencil and submit using the provided submission script.

from matutil import *
from vecutil import *
from solver import *
from echelon import *
from GF2 import one



## 1: (Problem 1) Recognizing Echelon Form
# Write each matrix as a list of row lists

echelon_form_1 = [[  1,2,0,2,0  ],
                  [  0,1,0,3,4  ],
                  [  0,0,2,3,4  ],
                  [  0,0,0,2,0  ],
                  [  0,0,0,0,4  ]]

echelon_form_2 = [[   0,4,3,4,4   ],
                  [   0,0,4,2,0   ],
                  [   0,0,0,0,1   ],
                  [   0,0,0,0,0   ]]

echelon_form_3 = [[   1,0,0,1   ],
                  [   0,0,0,1   ],
                  [   0,0,0,0   ]]

echelon_form_4 = [[   1,0,0,0   ],
                  [   0,1,0,0   ],
                  [   0,0,0,0   ],
                  [   0,0,0,0   ]]



## 2: (Problem 2) Is it echelon?
def is_echelon(A):
    '''
    Input:
        - A: a list of row lists
    Output:
        - True if A is in echelon form
        - False otherwise
    Examples:
        >>> is_echelon([[9,-1,2],[0,4,5],[0,0,2]])
        True
        >>> is_echelon([[0,4,5],[0,3,0],[0,0,2]])
        False
        >>> is_echelon([[9,10]])
        True
        >>> is_echelon([[5]])
        True
        >>> is_echelon([[1],[1]])
        False
        >>> is_echelon([[0]])
        True
        >>> is_echelon([[0],[1]])
        False
        >>> is_echelon([[  1,2,0,2,0  ],[  0,1,0,3,4  ], [  0,0,2,3,4  ],[  0,0,0,2,0  ], [  0,0,0,0,4  ]])
        True
        >>> is_echelon([[   0,4,3,4,4   ],[   0,0,4,2,0   ],[   0,0,0,0,1   ],[   0,0,0,0,0   ]])
        True
        >>> is_echelon([[   1,0,0,1   ],[   0,0,0,1   ],[   0,0,0,0   ]])
        True
        >>> is_echelon([[   1,0,0,0   ],[   0,1,0,0   ],[   0,0,0,0   ],[   0,0,0,0   ]])
        True
        >>> is_echelon([])
        True
        >>> is_echelon([[],[]])
        True
        >>> is_echelon([[0,1,1],[0,1,0],[0,0,1]])
        False
        >>> is_echelon([[2,1,0],[0,-4,0],[0,0,1]])
        True
        >>> is_echelon([[2,1,0],[-4,0,0],[0,0,1]])
        False
        >>> is_echelon([[2,1,0],[0,3,0],[1,0,1]])
        False
        >>> is_echelon([[1,1,1,1,1],[0,2,0,1,3],[0,0,0,5,3]])
        True
        >>> is_echelon([[1,1,1],[0,1,0],[0,0,0],[0,0,0]])
        True
        >>> is_echelon([[1,1,1],[0,0,0],[0,0,1]])
        False
        >>> is_echelon([[0,1,0],[0,0,0],[0,0,1]])
        False
        >>> is_echelon([[1,0],[0,2]])
        True
        >>> is_echelon([[0,0,0],[0,0,0],[0,0,0]])
        True
    '''
    nonZeroPos = []
    for row in A:
        pos = None
        for i,ele in enumerate(row):
            if ele != 0:
                pos = i
                break
        nonZeroPos.append(pos)
    if all(pos == None for pos in nonZeroPos):
        return True

    gotNone = False
    for pos in nonZeroPos:
        if gotNone and pos != None:
            return False
        if pos == None:
            gotNone = True

    return all([earlier < later for earlier, later in zip(nonZeroPos, nonZeroPos[1:]) if earlier != None and later != None])


## 3: (Problem 3) Solving with Echelon Form: No Zero Rows
# Give each answer as a list

echelon_form_vec_a = [1,0,3,0]
echelon_form_vec_b = [-3,0,-2,3]
echelon_form_vec_c = [-5,0,2,0,2]



## 4: (Problem 4) Solving with Echelon Form
# If a solution exists, give it as a list vector.
# If no solution exists, provide "None" (without the quotes).

solving_with_echelon_form_a = None
solving_with_echelon_form_b = [21,0,2,0,0]



## 5: (Problem 5) Echelon Solver
def echelon_solve(row_list, label_list, b):
    '''
    Input:
        - row_list: a list of Vecs
        - label_list: a list of labels establishing an order on the domain of
                      Vecs in row_list
        - b: a vector (represented as a list)
    Output:
        - Vec x such that row_list * x is b
    >>> D = {'A','B','C','D','E'}
    >>> U_rows = [Vec(D, {'A':one, 'E':one}), Vec(D, {'B':one, 'E':one}), Vec(D,{'C':one})]
    >>> b_list = [one,0,one]
    >>> cols = ['A', 'B', 'C', 'D', 'E']
    >>> echelon_solve(U_rows, cols, b_list) == Vec({'B', 'C', 'A', 'D', 'E'},{'B': 0, 'C': one, 'A': one})
    True
    '''

    nonZeroPos = []
    for r,rowV in enumerate(row_list):
        for c in label_list:
            if rowV[c] != 0:
                nonZeroPos.append((r,c))
                break

    x = zero_vec(set(label_list))
    for r,c in reversed(nonZeroPos):
        rowV = row_list[r]
        x[c] = (b[r] - x*rowV)/rowV[c]
    return x


## 6: (Problem 6) Solving General Matrices via Echelon

def solve(A, b):
    M = transformation(A)
    U = M*A
    col_label_list = sorted(A.D[1])
    U_rows_dict = mat2rowdict(U)
    row_list = [U_rows_dict[i] for i in sorted(U_rows_dict)]
    return echelon_solve(row_list,col_label_list, M*b)

Ai = listlist2mat([ [one,one,0,one],
                    [one,0,0,one],                    
                    [one,one,one,one],                    
                    [0,0,one,one] ])

R = ['a','b','c','d']
C = ['A','B','C','D']
D = (set(R),set(C))
A = Mat(D, {(R[k[0]],C[k[1]]):v for k,v in Ai.f.items()})
M = transformation(A)
U = M*A
t_col_label_list = sorted(A.D[1])
U_rows_dict = mat2rowdict(U)
t_row_list = [U_rows_dict[i] for i in sorted(U_rows_dict)]
biv = Vec(set(R),{R[i]:e for i,e in enumerate([ one,0,one,0 ])})
bv  = M * biv

# Provide as a list of Vec instances
row_list = t_row_list 
# Provide as a list
label_list = t_col_label_list 
# Provide as a list of GF(2) values
b = [bv[r] for r in range(len(R))]

echelon_solve(row_list, label_list, b)

## 7: (Problem 7) Nullspace A
null_space_rows_a = {3,4} # Put the row numbers of M from the PDF



## 8: (Problem 8) Nullspace B
null_space_rows_b = {4} # Put the row numbers of M from the PDF

