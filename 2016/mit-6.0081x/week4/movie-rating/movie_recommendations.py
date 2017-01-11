#!/usr/bin/env python
"""
movie_recommendations.py
Original author: Felix Sun (6.008 TA, Fall 2015)
Modified by:
- Danielle Pace (6.008 TA, Fall 2016),
- George H. Chen (6.008/6.008.1x instructor, Fall 2016)

Please read the project instructions beforehand! Your code should go in the
blocks denoted by "YOUR CODE GOES HERE" -- you should not need to modify any
other code!
"""

import matplotlib.pyplot as plt
import movie_data_helper
import numpy as np
import scipy
import scipy.misc
from sys import exit


def compute_posterior(prior, likelihood, y):
    """
    Use Bayes' rule for random variables to compute the posterior distribution
    of a hidden variable X, given N i.i.d. observations Y_0, Y_1, ..., Y_{N-1}.

    Hidden random variable X is assumed to take on a value in {0, 1, ..., M-1}.

    Each random variable Y_i takes on a value in {0, 1, ..., K-1}.

    Inputs
    ------
    - prior: a length M vector stored as a 1D NumPy array; prior[m] gives the
        (unconditional) probability that X = m
    - likelihood: a K row by M column matrix stored as a 2D NumPy array;
        likelihood[k, m] gives the probability that Y = k given X = m
    - y: a length-N vector stored as a 1D NumPy array; y[n] gives the observed
        value for random variable Y_n

    Output
    ------
    - posterior: a length M vector stored as a 1D NumPy array: posterior[m]
        gives the probability that X = m given
        Y_0 = y_0, ..., Y_{N-1} = y_{n-1}
    """

    # -------------------------------------------------------------------------
    # ERROR CHECKS -- DO NOT MODIFY
    #

    # check that prior probabilities sum to 1
    if np.abs(1 - np.sum(prior)) > 1e-06:
        exit('In compute_posterior: The prior probabilities need to sum to 1')

    # check that likelihood is specified as a 2D array
    if len(likelihood.shape) != 2:
        exit('In compute_posterior: The likelihood needs to be specified as ' +
             'a 2D array')

    K, M = likelihood.shape

    # make sure likelihood and prior agree on number of hidden states
    if len(prior) != M:
        exit('In compute_posterior: Mismatch in number of hidden states ' +
             'according to the prior and the likelihood.')

    # make sure the conditional distribution given each hidden state value sums
    # to 1
    for m in range(M):
        if np.abs(1 - np.sum(likelihood[:, m])) > 1e-06:
            exit('In compute_posterior: P(Y | X = %d) does not sum to 1' % m)

    #
    # END OF ERROR CHECKS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (b)
    #
    # Place your code to compute the log of the posterior here: store it in a
    # NumPy array called `log_answer`. If you exponentiate really small
    # numbers, the result is likely to underflow (i.e., it will be so small
    # that the computer will just make it 0 rather than storing the right
    # value). You need to go to log-domain. Hint: this next line is a good
    # first step.
    log_prior = np.log(prior)
    
    # likelihood just contains each user rating
    # hence indexing using y for observed users
    y_likelihood = likelihood[y]
    log_y_given_x = np.log(y_likelihood)
    
    # index into the sum_log_y_given_x to get the products of log_y_given_x
    sum_log_y_given_x = np.apply_along_axis(sum, 0, log_y_given_x)

    # use x as index in log_p_x_y to get P(Y|X=x)*P(X=x)
    log_p_x_y = log_prior + sum_log_y_given_x

    # using the trick to normalize 
    # i.e, divide by sum of all x in P(Y|X=x)*P(X=x)
    log_answer = log_p_x_y - scipy.misc.logsumexp(log_p_x_y)
    
    #
    # END OF YOUR CODE FOR PART (b)
    # -------------------------------------------------------------------------

    # do not exponentiate before this step
    posterior = np.exp(log_answer)
    return posterior


def compute_movie_rating_likelihood(M):
    """
    Compute the rating likelihood probability distribution of Y given X where
    Y is an individual rating (takes on a value in {0, 1, ..., M-1}), and X
    is the hidden true/innherent rating of a movie (also takes on a value in
    {0, 1, ..., M-1}).

    Please refer to the instructions of the project to see what the
    likelihood for ratings should be.

    Output
    ------
    - likelihood: an M row by M column matrix stored as a 2D NumPy array;
        likelihood[k, m] gives the probability that Y = k given X = m
    """

    # define the size to begin with
    likelihood = np.zeros((M, M))

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (c)
    #
    # Remember to normalize the likelihood, so that each column is a
    # probability distribution.
    #
    
    #generating x and y indices
    xs = np.tile(np.arange(0,M),(M,1))
    ys = np.tile(np.vstack(np.arange(0,M)),(1,M))
    
    # base case when x!=y
    ones = np.ones((M,M))
    xs_sub_ys_abs = np.abs(xs - ys)
    p_y_given_x = ones/xs_sub_ys_abs
    
    # handling x=y case
    np.fill_diagonal(p_y_given_x, 2)
    
    # for each x value the prob sum to 1
    col_sum = np.sum(p_y_given_x, axis=1)
    
    likelihood = p_y_given_x/col_sum

    #
    # END OF YOUR CODE FOR PART (c)
    # -------------------------------------------------------------------------

    return likelihood

## global variables to make plotting faster
#M = 11
#prior = np.array([1.0 / M] * M)  # uniform distribution
#likelihood = compute_movie_rating_likelihood(M)
#
## get the list of all movie IDs to process
#movie_id_list = movie_data_helper.get_movie_id_list()
#num_movies = len(movie_id_list)
#movie_ratings = [movie_data_helper.get_ratings(i) for i in movie_id_list]


def infer_true_movie_ratings(num_observations=-1):
    """
    For every movie, computes the posterior distribution and MAP estimate of
    the movie's true/inherent rating given the movie's observed ratings.

    Input
    -----
    - num_observations: integer that specifies how many available ratings to
        use per movie (the default value of -1 indicates that all available
        ratings will be used).

    Output
    ------
    - posteriors: a 2D array consisting of the posterior distributions where
        the number of rows is the number of movies, and the number of columns
        is M, i.e., the number of possible ratings (remember ratings are
        0, 1, ..., M-1); posteriors[i] gives a length M vector that is the
        posterior distribution of the true/inherent rating of the i-th movie
        given ratings for the i-th movie (where for each movie, the number of
        observations used is precisely what is specified by the input variable
        `num_observations`)
    - MAP_ratings: a 1D array with length given by the number of movies;
        MAP_ratings[i] gives the true/inherent rating with the highest
        posterior probability in the distribution `posteriors[i]`
    """

    M = 11  # all of our ratings are between 0 and 10
    prior = np.array([1.0 / M] * M)  # uniform distribution
    likelihood = compute_movie_rating_likelihood(M)

    # get the list of all movie IDs to process
    movie_id_list = movie_data_helper.get_movie_id_list()
    num_movies = len(movie_id_list)

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (d)
    #
    # Your code should iterate through the movies. For each movie, your code
    # should:
    #   1. Get all the observed ratings for the movie. You can artificially
    #      limit the number of available ratings used by truncating the ratings
    #      vector according to num_observations.
    #   2. Use the ratings you retrieved and the function compute_posterior to
    #      obtain the posterior of the true/inherent rating of the movie
    #      given the observed ratings
    #   3. Find the rating for each movie that maximizes the posterior

    # These are the output variables - it's your job to fill them.
    posteriors = np.zeros((num_movies, M))
    MAP_ratings = np.zeros(num_movies)
    
    for movie_id in movie_id_list:
        if(num_observations == -1):
            ratings = movie_data_helper.get_ratings(movie_id)
#            ratings = movie_ratings[movie_id]
        else:
            ratings = movie_data_helper.get_ratings(movie_id)[:num_observations]
#            ratings = movie_ratings[movie_id][:num_observations]
            
        posterior = compute_posterior(prior, likelihood, ratings)
        rating_with_high_posterior = np.argmax(posterior)
        posteriors[movie_id,:] = posterior
        MAP_ratings[movie_id] = rating_with_high_posterior
        
    #
    # END OF YOUR CODE FOR PART (d)
    # -------------------------------------------------------------------------

    return posteriors, MAP_ratings


def compute_entropy(distribution):
    """
    Given a distribution, computes the Shannon entropy of the distribution in
    bits.

    Input
    -----
    - distribution: a 1D array of probabilities that sum to 1

    Output:
    - entropy: the Shannon entropy of the input distribution in bits
    """

    # -------------------------------------------------------------------------
    # ERROR CHECK -- DO NOT MODIFY
    #
    if np.abs(1 - np.sum(distribution)) > 1e-6:
        exit('In compute_entropy: distribution should sum to 1.')
    #
    # END OF ERROR CHECK
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (f)
    #
    # Be sure to:
    # - use log base 2
    # - enforce 0log0 = 0

    sinfo = distribution * np.log2(1/distribution)
    sinfo[distribution < 10e-8] = 0.0
    entropy = np.sum(sinfo)    
    
    #
    # END OF YOUR CODE FOR PART (f)
    # -------------------------------------------------------------------------

    return entropy


def compute_true_movie_rating_posterior_entropies(num_observations):
    """
    For every movie, computes the Shannon entropy (in bits) of the posterior
    distribution of the true/inherent rating of the movie given observed
    ratings.

    Input
    -----
    - num_observations: integer that specifies how many available ratings to
        use per movie (the default value of -1 indicates that all available
        ratings will be used)

    Output
    ------
    - posterior_entropies: a 1D array; posterior_entropies[i] gives the Shannon
        entropy (in bits) of the posterior distribution of the true/inherent
        rating of the i-th movie given observed ratings (with number of
        observed ratings given by the input `num_observations`)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR PART (g)
    #
    # Make use of the compute_entropy function you coded in part (f).
    
    posteriors, MAP_estimates = infer_true_movie_ratings(num_observations)
    posterior_entropies = np.apply_along_axis(compute_entropy, 1, posteriors)
        
    #
    # END OF YOUR CODE FOR PART (g)
    # -------------------------------------------------------------------------

    return posterior_entropies


def main():

    # -------------------------------------------------------------------------
    # ERROR CHECKS
    #
    # Here are some error checks that you can use to test your code.

    print("\nproblem c compute_movie_rating_likelihood\n")
    print("\n M=2\n",compute_movie_rating_likelihood(2))
    print("\n M=3\n", compute_movie_rating_likelihood(3))
    print("\n M=5\n", compute_movie_rating_likelihood(5))
    print("\n------------------------------------------------\n")    
    
    print("\nproblem b compute_posterior")
    print("\nPosterior calculation (few observations)")
    prior = np.array([0.6, 0.4])
    likelihood = np.array([
        [0.7, 0.98],
        [0.3, 0.02],
    ])
    y = [0]*2 + [1]*1
    print("My answer:")
    print(compute_posterior(prior, likelihood, y))
    print("Expected answer:")
    print(np.array([[0.91986917, 0.08013083]]))
    print("\n------------------------------------------------\n")    


    print("\nproblem d infer_true_movie_ratings\n")
    num_observations = -1
    posteriors, MAP_ratings = infer_true_movie_ratings(num_observations)

    print("\ncorrect movie id 0 posterior\n")
    movie_id0 = np.array([  0.00000000e+000,   0.00000000e+000,   0.00000000e+000,   0.00000000e+000,
    0.00000000e+000,   0.00000000e+000,   2.08691952e-217,   7.41913971e-104,
    1.00000000e+000,   3.12235460e-048,   2.56768318e-058])
    
    print(movie_id0)
    
    print("\nmovie id 0 posterior\n")
    print(posteriors[0,:])
    print("\nmovie id 368 posterior\n")
    print(posteriors[368,:])
    
    print("\nbincounts of estimates")
    # print(MAP_ratings)
    bincounts = np.bincount(MAP_ratings.astype(int))
    print("bincounts",bincounts)
    print("\n------------------------------------------------\n")    

    print("\n problem top 10 movies\n")
    movie_indices_max_MAP = np.argsort(MAP_ratings, kind='mergesort')
    print("\ntop 10 movies with max MAP estimate")
    top_movies = movie_indices_max_MAP.flatten()[:10]
    movies_max_MAP = [movie_data_helper.get_movie_name(mid) for mid in top_movies]
    print( movies_max_MAP )
    print("\n------------------------------------------------\n")    

    print("\n problem f compute_entropy\n")
    print("Entropy of fair coin flip")
    distribution = np.array([0.5, 0.5])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(1.0)

    print("\nEntropy of coin flip where P(heads) = 0.25 and P(tails) = 0.75")
    distribution = np.array([0.25, 0.75])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(0.811278124459)

    print("\nEntropy of coin flip where P(heads) = 0.75 and P(tails) = 0.25")
    distribution = np.array([0.75, 0.25])
    print("My answer:")
    print(compute_entropy(distribution))
    print("Expected answer:")
    print(0.811278124459)

    print("\nEntropy with zeros")
    distribution = np.array([0.0, 0.000000001, 0.0000001, 0.999999899])
    print("My answer:")
    print(compute_entropy(distribution))
    print("\n------------------------------------------------\n")    

    
    print("\nproblem g compute_true_movie_rating_posterior_entropies\n")
    
    print("\n------------------------------------------------\n")    
    print("\nproblem h plot entropies\n")
    N = 200
    y_total_entropies = []
    for n in range(1,N+1):
#        print(n," ",end='')
        entropies = compute_true_movie_rating_posterior_entropies(n)
        y_total_entropies.append(np.sum(entropies)/len(entropies))
        
    plt.plot(range(1,N+1), y_total_entropies, 'b-')
    plt.show()
    print("\n------------------------------------------------\n")    


    #
    # END OF ERROR CHECKS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE FOR TESTING THE FUNCTIONS YOU HAVE WRITTEN,
    # for example, to answer the questions in part (e) and part (h)
    #
    # Place your code that calls the relevant functions here.  Make sure it's
    # easy for us graders to run your code. You may want to define multiple
    # functions for each of the parts of this problem, and call them here.

    #
    # END OF YOUR CODE FOR TESTING
    # -------------------------------------------------------------------------


if __name__ == '__main__':
    main()
