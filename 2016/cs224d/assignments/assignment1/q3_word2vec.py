import numpy as np
import random

from q1_softmax import softmax
from q2_gradcheck import gradcheck_naive
from q2_sigmoid import sigmoid, sigmoid_grad

def normalizeRows(x):
    """ Row normalization function """
    # Implement a function that normalizes each row of a matrix to have unit length

    ### YOUR CODE HERE

    axis = x.ndim - 1
    row_sums = x.sum(axis=axis).astype(np.float64)
    if(row_sums.ndim == 0):
        x = x/row_sums
    else:
        x = x / row_sums[:, np.newaxis]

    ### END YOUR CODE

    return x

def test_normalize_rows():
    print "Testing normalizeRows..."
    x = normalizeRows(np.array([[3.0,4.0],[1, 2]]))
    # the result should be [[0.6, 0.8], [0.4472, 0.8944]]
    print x
    assert (x.all() == np.array([[0.6, 0.8], [0.4472, 0.8944]]).all())
    print ""

def softmaxCostAndGradient(predicted, target, outputVectors, dataset):
    """ Softmax cost function for word2vec models """

    # Implement the cost and gradients for one predicted word vector
    # and one target word vector as a building block for word2vec
    # models, assuming the softmax prediction function and cross
    # entropy loss.

    # Inputs:
    # - predicted: numpy ndarray, predicted word vector (\hat{v} in
    #   the written component or \hat{r} in an earlier version)
    # - target: integer, the index of the target word
    # - outputVectors: "output" vectors (as rows) for all tokens
    # - dataset: needed for negative sampling, unused here.

    # Outputs:
    # - cost: cross entropy cost for the softmax word prediction
    # - gradPred: the gradient with respect to the predicted word
    #        vector
    # - grad: the gradient with respect to all the other word
    #        vectors

    # We will not provide starter code for this function, but feel
    # free to reference the code you previously wrote for this
    # assignment!

    ### YOUR CODE HERE

    # print "==softmax======================"
    # print "target: " + str(target)
    # print "predicted: " + str(predicted.shape)
    # print "outputVectors: " + str(outputVectors.shape)

    # dot product of the predicted word vector with all of the
    # output vector
    output_predicted_dots = np.dot(outputVectors, predicted)
    predictions = softmax(output_predicted_dots)
    cost = -np.log(predictions[target])

    # derivative of cost w.r.t to input, here target
    y = predictions.copy()
    y[target] -= 1.
    # during back-prop, gradient with respect to the predicted word vector
    gradPred = np.dot(outputVectors.T, y)

    # during back-prop, gradient with respect to the other word vector
    # so that we can pick the gradient of any word we want
    grad = np.outer(y, predicted)

    ### END YOUR CODE

    return cost, gradPred, grad

def negSamplingCostAndGradient(predicted, target, outputVectors, dataset,
    K=10):
    """ Negative sampling cost function for word2vec models """

    # Implement the cost and gradients for one predicted word vector
    # and one target word vector as a building block for word2vec
    # models, using the negative sampling technique. K is the sample
    # size. You might want to use dataset.sampleTokenIdx() to sample
    # a random word index.
    #
    # Note: See test_word2vec below for dataset's initialization.
    #
    # Input/Output Specifications: same as softmaxCostAndGradient
    # We will not provide starter code for this function, but feel
    # free to reference the code you previously wrote for this
    # assignment!

    ### YOUR CODE HERE

    # print "==neg-sampling======================"
    # print "target: " + str(target)
    # print "predicted: " + str(predicted.shape)
    # print "outputVectors: " + str(outputVectors.shape)

    gradPred = np.zeros(predicted.shape)
    grad = np.zeros(outputVectors.shape)
    cost = 0

    # dot product of the predicted word vector with all of the
    # output vector, forward propagated with sigmoid output layer
    z = sigmoid(outputVectors.dot(predicted))

    # cost that is contributed by the target word
    cost -= np.log(z[target])

    gradPred += outputVectors[target] * (z[target]-1.)
    grad[target] += predicted * (z[target]-1.)

    # iterating thru K negative samples
    # adding gradient and cost contributed by negative sampling
    for k in range(K):
        neg_sampled_idx = dataset.sampleTokenIdx()
        cost -= np.log(1. - z[neg_sampled_idx])
        gradPred += z[neg_sampled_idx] * outputVectors[neg_sampled_idx]
        grad[neg_sampled_idx] += z[neg_sampled_idx] * predicted

    ### END YOUR CODE

    return cost, gradPred, grad


def skipgram(currentWord, C, contextWords, tokens, inputVectors, outputVectors,
    dataset, word2vecCostAndGradient = softmaxCostAndGradient):
    """ Skip-gram model in word2vec """

    # Implement the skip-gram model in this function.

    # Inputs:
    # - currrentWord: a string of the current center word
    # - C: integer, context size
    # - contextWords: list of no more than 2*C strings, the context words
    # - tokens: a dictionary that maps words to their indices in
    #      the word vector list
    # - inputVectors: "input" word vectors (as rows) for all tokens
    # - outputVectors: "output" word vectors (as rows) for all tokens
    # - word2vecCostAndGradient: the cost and gradient function for
    #      a prediction vector given the target word vectors,
    #      could be one of the two cost functions you
    #      implemented above

    # Outputs:
    # - cost: the cost function value for the skip-gram model
    # - grad: the gradient with respect to the word vectors
    # We will not provide starter code for this function, but feel
    # free to reference the code you previously wrote for this
    # assignment!

    ### YOUR CODE HERE

    # print "==skipgram======================"
    # print "currentWord: "+ str(currentWord)
    # print "target: " + str(currentWord)
    # print "contextWords: "+ str(contextWords)
    # print "vocab: tokens: " + str(tokens)
    # print "inputVectors: " + str(inputVectors.shape)
    # print "outputVectors: " + str(outputVectors.shape)

    cost = 0.
    gradIn = np.zeros(inputVectors.shape)
    gradOut = np.zeros(outputVectors.shape)

    # we are gathering input_word, its index in vocabulary and its feature vector
    current_word_index = tokens[currentWord]
    current_word_vector = inputVectors[current_word_index]

    # iterating thru each of the context words that are predicted
    for contextWord in contextWords:
        # get target word index from vocabulary
        context_word_index = tokens[contextWord]
        c_cost, c_grad_in, c_grad_out = word2vecCostAndGradient(current_word_vector, context_word_index, outputVectors, dataset)
        cost += c_cost
        gradIn[context_word_index] += c_grad_in
        gradOut += c_grad_out

    ### END YOUR CODE

    return cost, gradIn, gradOut

def cbow(currentWord, C, contextWords, tokens, inputVectors, outputVectors,
    dataset, word2vecCostAndGradient = softmaxCostAndGradient):
    """ CBOW model in word2vec """

    # Implement the continuous bag-of-words model in this function.
    # Input/Output specifications: same as the skip-gram model
    # We will not provide starter code for this function, but feel
    # free to reference the code you previously wrote for this
    # assignment!

    #################################################################
    # IMPLEMENTING CBOW IS EXTRA CREDIT, DERIVATIONS IN THE WRIITEN #
    # ASSIGNMENT ARE NOT!                                           #
    #################################################################

    cost = 0
    gradIn = np.zeros(inputVectors.shape)
    gradOut = np.zeros(outputVectors.shape)

    ### YOUR CODE HERE

    # print "==cbow======================"
    # print "currentWord: "+ str(currentWord)
    # print "target: " + str(currentWord)
    # print "contextWords: "+ str(contextWords)
    # print "vocab: tokens: " + str(tokens)
    # print "inputVectors: " + str(inputVectors.shape)
    # print "outputVectors: " + str(outputVectors.shape)
    # print "dataset: " + str(dataset)

    current_word_index = tokens[currentWord]

    for contextWord in contextWords:
        # we are gathering input_word, its index in vocabulary and its feature vector
        context_word_index = tokens[contextWord]
        context_word_vector = inputVectors[context_word_index]
        c_cost, c_grad_in, c_grad_out = word2vecCostAndGradient(context_word_vector, current_word_index, outputVectors, dataset)
        cost += c_cost
        gradIn[current_word_index] += c_grad_in
        gradOut += c_grad_out

    ### END YOUR CODE

    return cost, gradIn, gradOut

#############################################
# Testing functions below. DO NOT MODIFY!   #
#############################################

def word2vec_sgd_wrapper(word2vecModel, tokens, wordVectors, dataset, C, word2vecCostAndGradient = softmaxCostAndGradient):
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

        c, gin, gout = word2vecModel(centerword, C1, context, tokens, inputVectors, outputVectors, dataset, word2vecCostAndGradient)
        cost += c / batchsize / denom
        grad[:N/2, :] += gin / batchsize / denom
        grad[N/2:, :] += gout / batchsize / denom

    return cost, grad

def test_word2vec():
    # Interface to the dataset for negative sampling
    dataset = type('dummy', (), {})()
    def dummySampleTokenIdx():
        return random.randint(0, 4)

    def getRandomContext(C):
        tokens = ["a", "b", "c", "d", "e"]
        return tokens[random.randint(0,4)], [tokens[random.randint(0,4)] \
           for i in xrange(2*C)]
    dataset.sampleTokenIdx = dummySampleTokenIdx
    dataset.getRandomContext = getRandomContext

    random.seed(31415)
    np.random.seed(9265)
    dummy_vectors = normalizeRows(np.random.randn(10,3))
    dummy_tokens = dict([("a",0), ("b",1), ("c",2),("d",3),("e",4)])

    print "==== Gradient check for skip-gram ===="
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(skipgram, dummy_tokens, vec, dataset, 5), dummy_vectors)
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(skipgram, dummy_tokens, vec, dataset, 5, negSamplingCostAndGradient), dummy_vectors)

    print "\n==== Gradient check for CBOW      ===="
    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(cbow, dummy_tokens, vec, dataset, 5), dummy_vectors)

    gradcheck_naive(lambda vec: word2vec_sgd_wrapper(cbow, dummy_tokens, vec, dataset, 5, negSamplingCostAndGradient), dummy_vectors)

    print "\n=== Results ==="
    cost, gradIn, gradOut = skipgram("c", 3, ["a", "b", "e", "d", "b", "c"], dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset)
    print "skipgram-softmax: cost=%s \ngradIn=\n%s \ngradOut=\n%s" % (cost, gradIn, gradOut)
    cost, gradIn, gradOut = skipgram("c", 1, ["a", "b"], dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset, negSamplingCostAndGradient)
    print "skipgram-negsam: cost=%s \ngradIn=\n%s \ngradOut=\n%s" % (cost, gradIn, gradOut)

    cost, gradIn, gradOut = cbow("a", 2, ["a", "b", "c", "a"], dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset)
    print "cbow-softmax: cost=%s \ngradIn=\n%s \ngradOut=\n%s" % (cost, gradIn, gradOut)
    cost, gradIn, gradOut = cbow("a", 2, ["a", "b", "a", "c"], dummy_tokens, dummy_vectors[:5,:], dummy_vectors[5:,:], dataset, negSamplingCostAndGradient)
    print "cbow-negsam: cost=%s \ngradIn=\n%s \ngradOut=\n%s" % (cost, gradIn, gradOut)

if __name__ == "__main__":
    test_normalize_rows()
    test_word2vec()
