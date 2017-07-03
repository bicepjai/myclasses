import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive

def forward_backward_prop(data, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    ### YOUR CODE HERE: forward propagation

    N,_ = data.shape

    #layer1
    h1 = data
    a1 = data

    #layer2
    h2 = a1.dot(W1) + b1
    a2 = sigmoid(h2)

    #layer3
    out = a2.dot(W2) + b2
    scores = softmax(out)

    #cost selecting just the elements that are predicted
    y_indices = np.where( labels == 1 )
    cost = -np.sum(np.log(scores[y_indices]))

    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation

    gradW1 = np.zeros(W1.shape)
    gradb1 = np.zeros(b1.shape)
    gradW2 = np.zeros(W2.shape)
    gradb2 = np.zeros(b2.shape)

    #layer3 gradient
    dout = scores
    dout[y_indices] = dout[y_indices] - 1 #softmax gradient
    gradW2 += a2.T.dot(dout)
    da2 = W2.dot(dout.T)
    gradb2 += np.sum(dout,axis=0)

    #layer2 gradient
    dh2 = da2.T * (a2 * (1 - a2)) #sigmoid gradient
    gradW1 += a1.T.dot(dh2)
    gradb1 += np.sum(dh2,axis=0)

    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    return cost, grad

def rel_diff(a1, a2):
    return abs(a1 - a2) / max(1, abs(a1), abs(a2))

def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i,random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params: forward_backward_prop(data, labels, params,
        dimensions), params)

def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    # raise NotImplementedError
    ### END YOUR CODE

if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
