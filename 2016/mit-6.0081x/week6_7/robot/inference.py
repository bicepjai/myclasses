#!/usr/bin/env python
# inference.py
# Base code by George H. Chen (georgehc@mit.edu) -- updated 10/18/2016
import collections
import sys

import graphics
import numpy as np
import robot


# Throughout the code, we use these variables.
# Do NOT change these (but you'll need to use them!):
# - all_possible_hidden_states: a list of possible hidden states
# - all_possible_observed_states: a list of possible observed states
# - prior_distribution: a distribution over states
# - transition_model: a function that takes a hidden state and returns a
#     Distribution for the next state
# - observation_model: a function that takes a hidden state and returns a
#     Distribution for the observation from that hidden state
all_possible_hidden_states = robot.get_all_hidden_states()
all_possible_observed_states = robot.get_all_observed_states()
prior_distribution = robot.initial_distribution()
transition_model = robot.transition_model
observation_model = robot.observation_model


# You may find this function helpful for computing logs without yielding a
# NumPy warning when taking the log of 0.
def careful_log(x):
    # computes the log of a non-negative real number
    if x == 0:
        return -np.inf
    else:
        return np.log(x)


# -----------------------------------------------------------------------------
# Functions for you to implement
#

def forward_backward(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of marginal distributions at each time step; each distribution
    should be encoded as a Distribution (see the Distribution class in
    robot.py and see how it is used in both robot.py and the function
    generate_data() above, and the i-th Distribution should correspond to time
    step i
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #

    # form inverse_index hidden state dic
    hidden_state_to_i = {p: i for i, p in enumerate(all_possible_hidden_states)}
    num_all_hidden_states = len(all_possible_hidden_states)

    # transition_matrix =========================================
    transition_matrix = np.zeros((440, 440))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        transition_model_dict = transition_model(hidden_state)
        for next_hidden_state in transition_model_dict.keys():
            transition_matrix[i, hidden_state_to_i[next_hidden_state]] = transition_model_dict[next_hidden_state]

    # form inverse_index hidden state dic
    observed_state_to_i = {p: i for i, p in enumerate(all_possible_observed_states)}

    # emission_matrix =========================================================
    emission_matrix = np.zeros((440, 96))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        observed_model_dict = observation_model(hidden_state)
        for observed_state in observed_model_dict.keys():
            emission_matrix[i, observed_state_to_i[observed_state]] = observed_model_dict[observed_state]

    # initial_state ==========================================================
    initial_state_matrix = np.zeros((1, 440))
    for initial_state in prior_distribution.keys():
        initial_state_matrix[0, hidden_state_to_i[initial_state]] = prior_distribution[initial_state]

    num_time_steps = len(observations)

    # TODO: Compute the forward messages =========================================
    forward_messages = [initial_state_matrix for _ in range(num_time_steps)]
    forward_messages[0] = initial_state_matrix
    fm_i = 0
    for i, observed_state in enumerate(observations):
        fm_i = fm_i + 1

        # tracking from first timestep
        if(i >= num_time_steps - 1):
            break

        if(observed_state is None):
            phi = np.ones((1, 440))
        else:
            phi = emission_matrix[:, observed_state_to_i[observed_state]]

        prev_fw_msg = forward_messages[fm_i - 1]
        alpha_matrix = (prev_fw_msg * phi) * transition_matrix.T
        forward_messages[fm_i] = np.sum(alpha_matrix, 1)

    # TODO: Compute the backward messages =========================================
    backward_messages = [np.ones((1, 440)) / num_all_hidden_states for _ in range(num_time_steps)]
    backward_messages[num_time_steps - 1] = np.ones((1, 440)) / num_all_hidden_states
    bw_i = num_time_steps - 1
    for i, observed_state in enumerate(observations[::-1]):
        bw_i = bw_i - 1

        # tracking from last timestep
        if(num_time_steps - i - 1 <= 0):
            break

        if(observed_state is None):
            phi = np.ones((1, 440))
        else:
            phi = emission_matrix[:, observed_state_to_i[observed_state]]

        prev_bw_msg = backward_messages[bw_i + 1]
        alpha_matrix = (prev_bw_msg * phi) * transition_matrix
        backward_messages[bw_i] = np.sum(alpha_matrix, 1)

    # TODO: Compute the marginals =========================================
    marginals = [robot.Distribution() for _ in range(num_time_steps)]

    for i, observed_state in enumerate(observations):

        if(observed_state is None):
            phi = np.ones((1, 440))
        else:
            phi = np.expand_dims(emission_matrix[:, observed_state_to_i[observed_state]], 0)

        fw_msg = forward_messages[i]
        bw_msg = backward_messages[i]

        marginal = fw_msg * bw_msg * phi

        for j in range(num_all_hidden_states):
            if marginal[0, j] != 0:
                marginals[i][all_possible_hidden_states[j]] = marginal[0, j]

        marginals[i].renormalize()

    return marginals


def Viterbi(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of esimated hidden states, each encoded as a tuple
    (<x>, <y>, <action>)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #

    hidden_state_to_i = {p: i for i, p in enumerate(all_possible_hidden_states)}
    num_all_hidden_states = len(all_possible_hidden_states)
    num_all_observed_states = len(all_possible_observed_states)

    # transition_matrix =========================================
    transition_matrix = np.zeros((num_all_hidden_states, num_all_hidden_states))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        transition_model_dict = transition_model(hidden_state)
        for next_hidden_state in transition_model_dict.keys():
            transition_matrix[i, hidden_state_to_i[next_hidden_state]] = transition_model_dict[next_hidden_state]

    log_transition_matrix = -np.log2(transition_matrix)

    # form inverse_index hidden state dic
    observed_state_to_i = {p: i for i, p in enumerate(all_possible_observed_states)}

    # emission_matrix =========================================================
    emission_matrix = np.zeros((num_all_hidden_states, num_all_observed_states))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        observed_model_dict = observation_model(hidden_state)
        for observed_state in observed_model_dict.keys():
            emission_matrix[i, observed_state_to_i[observed_state]] = observed_model_dict[observed_state]
    log_emission_matrix = -np.log2(emission_matrix)

    # initial_state ==========================================================
    initial_state_matrix = np.zeros((1, num_all_hidden_states))
    for initial_state in prior_distribution.keys():
        initial_state_matrix[0, hidden_state_to_i[initial_state]] = prior_distribution[initial_state]
    log_initial_state_matrix = -np.log2(initial_state_matrix)

    num_time_steps = len(observations)

    # forward messages and trace back values =================================
    trace_back_messages = [np.empty((1, num_all_hidden_states)) for _ in range(num_time_steps - 1)]
    log_forward_messages = [np.zeros((1, num_all_hidden_states)) for _ in range(num_time_steps - 1)]

    for fm_i, observed_state in enumerate(observations):

        #  no forward message and trace back for the last timestep
        if(fm_i >= num_time_steps - 1):
            break

        if fm_i == 0:
            phi = log_emission_matrix[:, observed_state_to_i[observed_state]] + log_initial_state_matrix
            log_alpha_matrix = phi + log_transition_matrix.T

        else:
            if(observed_state is None):
                phi = np.zeros((1, num_all_hidden_states)) # since dealing with log
            else:
                phi = log_emission_matrix[:, observed_state_to_i[observed_state]]
            log_alpha_matrix = log_forward_messages[fm_i - 1] + phi + log_transition_matrix.T

        log_forward_messages[fm_i] = np.amin(log_alpha_matrix, 1)
        trace_back_messages[fm_i] = np.argmin(log_alpha_matrix, 1)

    # MAP estimated states ===================================================
    estimated_hidden_states = [None] * num_time_steps

    # at last observed state
    bw_i = num_time_steps - 1
    phi_n = log_emission_matrix[:, observed_state_to_i[observations[bw_i]]]
    log_beta_vector = log_forward_messages[bw_i - 1] + phi_n
    estimated_hidden_states[bw_i] = all_possible_hidden_states[np.argmin(log_beta_vector)]

    # tracing back
    for bw_i in range(num_time_steps - 2, -1, -1):
        prev_best_hidden_state_i = hidden_state_to_i[estimated_hidden_states[bw_i + 1]]
        current_best_hidden_state_i = trace_back_messages[bw_i][prev_best_hidden_state_i]
        estimated_hidden_states[bw_i] = all_possible_hidden_states[current_best_hidden_state_i]

    return estimated_hidden_states


def second_best(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of esimated hidden states, each encoded as a tuple
    (<x>, <y>, <action>)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #

    hidden_state_to_i = {p: i for i, p in enumerate(all_possible_hidden_states)}
    num_all_hidden_states = len(all_possible_hidden_states)
    num_all_observed_states = len(all_possible_observed_states)

    # transition_matrix =========================================
    transition_matrix = np.zeros((num_all_hidden_states, num_all_hidden_states))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        transition_model_dict = transition_model(hidden_state)
        for next_hidden_state in transition_model_dict.keys():
            transition_matrix[i, hidden_state_to_i[next_hidden_state]] = transition_model_dict[next_hidden_state]

    log_transition_matrix = -np.log2(transition_matrix)

    # form inverse_index hidden state dic
    observed_state_to_i = {p: i for i, p in enumerate(all_possible_observed_states)}

    # emission_matrix =========================================================
    emission_matrix = np.zeros((num_all_hidden_states, num_all_observed_states))
    for i, hidden_state in enumerate(all_possible_hidden_states):
        observed_model_dict = observation_model(hidden_state)
        for observed_state in observed_model_dict.keys():
            emission_matrix[i, observed_state_to_i[observed_state]] = observed_model_dict[observed_state]
    log_emission_matrix = -np.log2(emission_matrix)

    # initial_state ==========================================================
    initial_state_matrix = np.zeros((1, num_all_hidden_states))
    for initial_state in prior_distribution.keys():
        initial_state_matrix[0, hidden_state_to_i[initial_state]] = prior_distribution[initial_state]
    log_initial_state_matrix = -np.log2(initial_state_matrix)

    num_time_steps = len(observations)

    # forward messages and trace back values =================================
    trace_back_messages1 = [np.empty((2, num_all_hidden_states)) for _ in range(num_time_steps - 1)]
    trace_back_messages2 = [np.empty((2, num_all_hidden_states)) for _ in range(num_time_steps - 1)]
    log_forward_messages = [np.zeros((1, num_all_hidden_states)) for _ in range(num_time_steps - 1)]
    
    argmin2 = lambda arr: arr.argsort()[1::-1][::-1][1]
    
    for fm_i, observed_state in enumerate(observations):

        #  no forward message and trace back for the last timestep
        if(fm_i >= num_time_steps - 1):
            break

        if fm_i == 0:
            phi = log_emission_matrix[:, observed_state_to_i[observed_state]] + log_initial_state_matrix
            log_alpha_matrix = phi + log_transition_matrix.T

        else:
            if(observed_state is None):
                phi = np.zeros((1, num_all_hidden_states)) # since dealing with log
            else:
                phi = log_emission_matrix[:, observed_state_to_i[observed_state]]
            log_alpha_matrix = log_forward_messages[fm_i - 1] + phi + log_transition_matrix.T

        log_forward_messages[fm_i] = np.amin(log_alpha_matrix, 1)
        trace_back_messages1[fm_i] = np.argmin(log_alpha_matrix, 1)
        trace_back_messages2[fm_i] = np.apply_along_axis(argmin2, 1, log_alpha_matrix) 

    # MAP estimated states ===================================================
    estimated_hidden_states = [None] * num_time_steps

    # at last observed state
    bw_i = num_time_steps - 1
    phi_n = log_emission_matrix[:, observed_state_to_i[observations[bw_i]]]
    log_beta_vector = log_forward_messages[bw_i - 1] + phi_n
    estimated_hidden_states[bw_i] = all_possible_hidden_states[argmin2(log_beta_vector)]

    # tracing back
    current_trace_back_message = trace_back_messages2
    for bw_i in range(num_time_steps - 2, -1, -1):
        
        prev_2best_hidden_state_i = hidden_state_to_i[estimated_hidden_states[bw_i + 1]]

        current_2best_hidden_state_i = current_trace_back_message[bw_i][prev_2best_hidden_state_i]
        current_best_hidden_state_i = trace_back_messages1[bw_i][prev_2best_hidden_state_i]

        if(current_best_hidden_state_i == current_2best_hidden_state_i):
            current_trace_back_message = trace_back_messages1
            
        estimated_hidden_states[bw_i] = all_possible_hidden_states[current_best_hidden_state_i]

    return estimated_hidden_states



# -----------------------------------------------------------------------------
# Generating data from the hidden Markov model
#

def generate_data(num_time_steps, make_some_observations_missing=False,
                  random_seed=None):
    # generate samples from this project's hidden Markov model
    hidden_states = []
    observations = []

    # if the random seed is not None, then this makes the randomness
    # deterministic, which may be helpful for debug purposes
    np.random.seed(random_seed)

    # draw initial state and emit an observation
    initial_state = prior_distribution.sample()
    initial_observation = observation_model(initial_state).sample()

    hidden_states.append(initial_state)
    observations.append(initial_observation)

    for time_step in range(1, num_time_steps):
        # move the robot
        prev_state = hidden_states[-1]
        new_state = transition_model(prev_state).sample()

        # maybe emit an observation
        if not make_some_observations_missing:
            new_observation = observation_model(new_state).sample()
        else:
            if np.random.rand() < .1:  # 0.1 prob. of observation being missing
                new_observation = None
            else:
                new_observation = observation_model(new_state).sample()

        hidden_states.append(new_state)
        observations.append(new_observation)

    return hidden_states, observations


# -----------------------------------------------------------------------------
# Main
#

def main():
    # flags
    make_some_observations_missing = False
    use_graphics = True
    need_to_generate_data = True

    # parse command line arguments
    for arg in sys.argv[1:]:
        if arg == '--missing':
            make_some_observations_missing = True
        elif arg == '--nographics':
            use_graphics = False
        elif arg.startswith('--load='):
            filename = arg[7:]
            hidden_states, observations = robot.load_data(filename)
            need_to_generate_data = False
            num_time_steps = len(hidden_states)

    # if no data is loaded, then generate new data
    if need_to_generate_data:
        num_time_steps = 100
        hidden_states, observations = \
            generate_data(num_time_steps,
                          make_some_observations_missing)

    print('Running forward-backward...')
    marginals = forward_backward(observations)
    print("\n")

    timestep = 2
    print("Most likely parts of marginal at time %d:" % (timestep))
    if marginals[timestep] is not None:
        print(sorted(marginals[timestep].items(),
                     key=lambda x: x[1],
                     reverse=True)[:10])
    else:
        print('*No marginal computed*')
    print("\n")

    print('Running Viterbi...')
    estimated_states = Viterbi(observations)
    print("\n")

    print("Last 10 hidden states in the MAP estimate:")
    for time_step in range(num_time_steps - 10 - 1, num_time_steps):
        if estimated_states[time_step] is None:
            print('Missing')
        else:
            print(estimated_states[time_step])
    print("\n")

    print('Finding second-best MAP estimate...')
    estimated_states2 = second_best(observations)
    print("\n")

    print("Last 10 hidden states in the second-best MAP estimate:")
    for time_step in range(num_time_steps - 10 - 1, num_time_steps):
        if estimated_states2[time_step] is None:
            print('Missing')
        else:
            print(estimated_states2[time_step])
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states[time_step] != hidden_states[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between MAP estimate and true hidden " +
          "states:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states2[time_step] != hidden_states[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between second-best MAP estimate and " +
          "true hidden states:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states[time_step] != estimated_states2[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between MAP and second-best MAP " +
          "estimates:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    # display
    if use_graphics:
        app = graphics.playback_positions(hidden_states,
                                          observations,
                                          estimated_states,
                                          marginals)
        app.mainloop()


if __name__ == '__main__':
    main()
