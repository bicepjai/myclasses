from imp import reload
from GF2 import *
from vec import *
from mat import *
from matutil import *
from orthogonalization import *
from vecutil import *
from Orthogonalization_problems import *
from python_lab import *
from read_data import *
from machine_learning_lab import *
from cancer_data import *
from solver import *

A,b = read_training_data('train.data')
w1 = Vec(A.D[1], {key: 1 for key in A.D[1]})
w0 = Vec(A.D[1], {})
sigma1 = 2e-9
sigma2 = 1e-9
T1 = 100
T2 = 1000
T3 = 10000
w = QR_solve(A,b)

>>> w = solve(A,b)
>>> loss(A, b, w)
77.5005109640753
>>> fraction_wrong(A, b, w)
0.04666666666666667

>>> w = QR_solve(A,b)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bicepjai/Projects/coursera/matrix/Orthogonalization_problems.py", line 175, in QR_solve
    return (triangular_solve(Rlist, RCollabels, Q.transpose() * b))
  File "/Users/bicepjai/Projects/coursera/matrix/triangular.py", line 59, in triangular_solve
    x[c] = (b[j] - x*row)/row[c]
ZeroDivisionError: float division by zero

loss(A, b, w)
fraction_wrong(A, b, w)

>>> w = gradient_descent(A, b, w0, sigma1, T1)
>>> loss(A, b, w)
229.04464980482433
>>> fraction_wrong(A, b, w)
0.36666666666666664
>>>
>>> w = gradient_descent(A, b, w0, sigma1, T2)
>>> loss(A, b, w)
188.5259689795305
>>> fraction_wrong(A, b, w)
0.11333333333333333
>>>
>>> w = gradient_descent(A, b, w0, sigma1, T3)
>>> loss(A, b, w)
174.13216628243913
>>> fraction_wrong(A, b, w)
0.16
>>>
>>> w = gradient_descent(A, b, w1, sigma1, T1)
>>> loss(A, b, w)
1200437.5831500404
>>> fraction_wrong(A, b, w)
0.71
>>>
>>> w = gradient_descent(A, b, w1, sigma1, T2)
>>> loss(A, b, w)
366204.22045221634
>>> fraction_wrong(A, b, w)
0.6633333333333333
>>>
>>> w = gradient_descent(A, b, w1, sigma1, T3)
>>> loss(A, b, w)
5758.507214036355
>>> fraction_wrong(A, b, w)
0.48333333333333334

>>> w = gradient_descent(A, b, w0, sigma2, T1)
>>> loss(A, b, w)
229.04464980482427
>>> fraction_wrong(A, b, w)
0.36666666666666664
>>>
>>> w = gradient_descent(A, b, w0, sigma2, T2)
>>> loss(A, b, w)
188.52596897953043
>>> fraction_wrong(A, b, w)
0.11333333333333333
>>>
>>> w = gradient_descent(A, b, w0, sigma2, T3)
>>> loss(A, b, w)
174.13216628243913
>>> fraction_wrong(A, b, w)
0.16
>>>
>>> w = gradient_descent(A, b, w1, sigma2, T1)
>>> loss(A, b, w)
1200437.5831500406
>>> fraction_wrong(A, b, w)
0.71
>>>
>>> w = gradient_descent(A, b, w1, sigma2, T2)
>>> loss(A, b, w)
366204.22045221616
>>> fraction_wrong(A, b, w)
0.6633333333333333
>>>
>>> w = gradient_descent(A, b, w1, sigma2, T3)
>>> loss(A, b, w)
5758.507214036362
>>> fraction_wrong(A, b, w)
0.48333333333333334
>>>


