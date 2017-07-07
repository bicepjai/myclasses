#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_gradcheck import gradcheck_naive
from q2_sigmoid import sigmoid, sigmoid_grad

def normalizeRows(x):
    """ Row normalization function

    Implement a function that normalizes each row of a matrix to have
    unit length.
    """

    ### YOUR CODE HERE
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    ### END YOUR CODE

    return x


def test_normalize_rows():
    print "Testing normalizeRows..."
    x = normalizeRows(np.array([[3.0,4.0],[1, 2]]))
    print x
    ans = np.array([[0.6,0.8],[0.4472136,0.89442719]])
    assert np.allclose(x, ans, rtol=1e-05, atol=1e-06)
    print ""


def softmaxCostAndGradient(predicted, target, outputVectors, dataset):
    """ Softmax cost function for word2vec models

    Implement the cost and gradients for one predicted word vector
    and one target word vector as a building block for word2vec
    models, assuming the softmax prediction function and cross
    entropy loss.

    Arguments:
    predicted -- numpy ndarray, predicted word vector (\hat{v} in
                 the written component)
    target -- integer, the index of the target word
    outputVectors -- "output" vectors (as rows) for all tokens
    dataset -- needed for negative sampling, unused here.

    Return:
    cost -- cross entropy cost for the softmax word prediction
    gradPred -- the gradient with respect to the predicted word
           vector
    grad -- the gradient with respect to all the other word
           vectors

    We will not provide starter code for this function, but feel
    free to reference the code you previously wrote for this
    assignment!
    """

    ### YOUR CODE HERE
    vc = predicted
    uo_idx = target
    uw_vc = np.dot(outputVectors, vc) # v_w
    y_hat = softmax(uw_vc).reshape(-1, 1)

    # gradient for softmax
    y_hat_minus_y = y_hat # w != o
    y_hat_minus_y[uo_idx] -= 1. # w = o

    # cost
    cost = -np.log(y_hat[uo_idx])

    # gradient w.r.t to uw
    grad = np.dot(y_hat_minus_y, vc.reshape(1, -1))

    # gradient w.r.t to vc
    gradPred = np.dot(outputVectors.T, y_hat_minus_y)
    ### END YOUR CODE

    return cost, gradPred, grad


def getNegativeSamples(target, dataset, K):
    """ Samples K indexes which are not the target """

    indices = [None] * K
    for k in xrange(K):
        newidx = dataset.sampleTokenIdx()
        while newidx == target:
            newidx = dataset.sampleTokenIdx()
        indices[k] = newidx
    return indices


def negSamplingCostAndGradient(predicted, target, outputVectors, dataset,
                               K=10):
    """ Negative sampling cost function for word2vec models

    Implement the cost and gradients for one predicted word vector
    and one target word vector as a building block for word2vec
    models, using the negative sampling technique. K is the sample
    size.

    Note: See test_word2vec below for dataset's initialization.

    Arguments/Return Specifications: same as softmaxCostAndGradient
    """

    # Sampling of indices is done for you. Do not modify this if you
    # wish to match the autograder and receive points!
    indices = [target]
    indices.extend(getNegativeSamples(target, dataset, K))

    ### YOUR CODE HERE
    # dont know why they have target index in indices
    neg_sample_indices = indices[1:]

    # matching derivated equations
    uo_idx = target
    vc = predicted
    uk = outputVectors[neg_sample_indices]
    uo = outputVectors[uo_idx]
    uw_vc = outputVectors.dot(vc)
    neg_uk_vc = -uw_vc[neg_sample_indices]
    uo_vc = uw_vc[uo_idx]

    sigmoid_uo_vc = sigmoid(uo_vc)
    sigmoid_neg_uk_vc = [sigmoid(scalar) for scalar in neg_uk_vc]

    # cost that is contributed by the target word
    cost = 0
    cost -= np.log(sigmoid_uo_vc)
    # cost that is contributed by the negative sampled word
    cost -= sum([np.log(scalar) for scalar in sigmoid_neg_uk_vc])

    # gradPred = dJ_dvc
    gradPred = uo * (sigmoid_uo_vc - 1.)
    # sigmoid_neg_uk_vc and uk has matching indices
    # we use for loop caz its just K elements
    gradPred -= sum([(sigmoid_neg_uk_vc[idx] - 1) * uk[idx] for idx in range(K)])

    # grad =  dJ_duo + dJ_duk
    grad = np.zeros(outputVectors.shape)
    # dJ_duo
    grad[uo_idx] += vc * (sigmoid_uo_vc - 1.)
    # gradient dJ_duk contributed by negative samples
    for idx, neg_sample_idx in enumerate(neg_sample_indices):
        grad[neg_sample_idx] -= (sigmoid_neg_uk_vc[idx] - 1) * vc
    ### END YOUR CODE


def skipgram(currentWord, C, contextWords, tokens, inputVectors, outputVectors,
             dataset, word2vecCostAndGradient=softmaxCostAndGradient):
    """ Skip-gram model in word2vec

    Implement the skip-gram model in this function.

    Arguments:
    currrentWord -- a string of the current center word
    C -- integer, context size
    contextWords -- list of no more than 2*C strings, the context words
    tokens -- a dictionary that maps words to their indices in
              the word vector list
    inputVectors -- "input" word vectors (as rows) for all tokens
    outputVectors -- "output" word vectors (as rows) for all tokens
    word2vecCostAndGradient -- the cost and gradient function for
                               a prediction vector given the target
                               word vectors, could be one of the two
                               cost functions you implemented above.

    Return:
    cost -- the cost function value for the skip-gram model
    grad -- the gradient with respect to the word vectors
    """

    cost = 0.0
    gradIn = np.zeros(inputVectors.shape)
    gradOut = np.zeros(outputVectors.shape)

    ### YOUR CODE HERE
    predicted = inputVectors[tokens[currentWord]]
    for contextWord in contextWords:
        target = tokens[contextWord]
        current_cost, gradPred, grad = word2vecCostAndGradient(predicted, target,
                                                        outputVectors, dataset)
        gradIn[tokens[currentWord]] += gradPred.reshape(-1)
        gradOut += grad
        cost += current_cost
    ### END YOUR CODE

    return cost, gradIn, gradOut


def cbow(currentWord, C, contextWords, tokens, inputVectors, outputVectors,
         dataset, word2vecCostAndGradient=softmaxCostAndGradient):
    """CBOW model in word2vec

    Implement the continuous bag-of-words model in this function.

    Arguments/Return specifications: same as the skip-gram model

    Extra credit: Implementing CBOW is optional, but the gradient
    derivations are not. If you decide not to implement CBOW, remove
    the NotImplementedError.
    """

    cost = 0.0
    gradIn = np.zeros(inputVectors.shape)
    gradOut = np.zeros(outputVectors.shape)

    ### YOUR CODE HERE
    contextWord_tokens = [tokens[contextWord] for contextWord in contextWords]
    predicted = np.sum(inputVectors[contextWord_tokens], axis=0)

    target = tokens[currentWord]
    cost, gradPred, gradOut = word2vecCostAndGradient(predicted, target, outputVectors, dataset)
    for t in contextWord_tokens:
        gradIn[t] += gradPred.reshape(-1)
    ### END YOUR CODE

    return cost, gradIn, gradOut


#############################################
# Testing functions below. DO NOT MODIFY!   #
#############################################

def word2vec_sgd_wrapper(word2vecModel, tokens, wordVectors, dataset, C,
                         word2vecCostAndGradient=softmaxCostAndGradient):
    batchsize = 50
    cost = 0.0
    grad = np.zeros(wordVectors.shape)
    N = wordVectors.shape[0]
    inputVectors = wordVectors[:N/2,:]
    outputVectors = wordVectors[N/2:,:]
    for i in xrange(batchsize):
        C1 = random.randint(1,C)
        centerword, context = dataset.getRandomContext(C1)

        if word2vecModel == skipgram:
            denom = 1
        else:
            denom = 1

        c, gin, gout = word2vecModel(
            centerword, C1, context, tokens, inputVectors, outputVectors,
            dataset, word2vecCostAndGradient)
        cost += c / batchsize / denom
        grad[:N/2, :] += gin / batchsize / denom
        grad[N/2:, :] += gout / batchsize / denom

    return cost, grad


def test_word2vec():
    """ Interface to the dataset for negative sampling """
    dataset = type('dummy', (), {})()
    def dummySampleTokenIdx():
        return random.randint(0, 4)

    def getRandomContext(C):
        tokens = ["a", "b", "c", "d", "e"]
        return tokens[random.randint(0,4)], \
            [tokens[random.randint(0,4)] for i in xrange(2*C)]
    dataset.sampleTokenIdx = dummySampleTokenIdx
    dataset.getRandomContext = getRandomContext

    random.seed(31415)
    np.random.seed(9265)
    dummy_vectors = normalizeRows(np.random.randn(10,3))
    dummy_tokens = dict([("a",0), ("b",1), ("c",2),("d",3),("e",4)])
    print "==== Gradient check for skip-gram ===="
    print "--- skip-gram with softmaxCostAndGradient ----"
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(
        skipgram, dummy_tokens, vec, dataset, 5, softmaxCostAndGradient),
        dummy_vectors)
    print "--- skip-gram with negSamplingCostAndGradient ----"
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(
        skipgram, dummy_tokens, vec, dataset, 5, negSamplingCostAndGradient),
        dummy_vectors)
    print "\n==== Gradient check for CBOW      ===="
    print "--- CBOW with softmaxCostAndGradient ----"
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(
        cbow, dummy_tokens, vec, dataset, 5, softmaxCostAndGradient),
        dummy_vectors)
    print "--- CBOW with negSamplingCostAndGradient ----"
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(
        cbow, dummy_tokens, vec, dataset, 5, negSamplingCostAndGradient),
        dummy_vectors)
    #
    # print "\n=== Results ==="
    # print skipgram("c", 3, ["a", "b", "e", "d", "b", "c"],
    #     dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset)
    # print skipgram("c", 1, ["a", "b"],
    #     dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset,
    #     negSamplingCostAndGradient)
    # print cbow("a", 2, ["a", "b", "c", "a"],
    #     dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset)
    # print cbow("a", 2, ["a", "b", "a", "c"],
    #     dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset,
    #     negSamplingCostAndGradient)


if __name__ == "__main__":
    test_normalize_rows()
    test_word2vec()
