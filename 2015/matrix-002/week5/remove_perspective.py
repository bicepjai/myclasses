from imp import reload

import vec
reload(vec)
from vec import *

import mat
reload(mat)
from mat import *

import matutil
reload(matutil)
from matutil import *

import vecutil
reload(vecutil)
from vecutil import *

import perspective_lab
reload(perspective_lab)
from perspective_lab import *

import image_mat_util
reload(image_mat_util)
from image_mat_util import *

veclist = make_nine_equations([(358,36),(329,597),(592,157),(580,483)])
L = rowdict2mat(veclist)
hvec = solve(L,b)
H = Mat((R,C),hvec.f)
(X_pts, colors) = image_mat_util.file2mat('board.png', ('x1','x2','x3'))
Y_pts = H * X_pts
Y_board = mat_move2board(Y_pts)
image_mat_util.mat2display(Y_board, colors, ('y1', 'y2', 'y3'), scale=100, xmin=None, ymin=None)