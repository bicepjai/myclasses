import sys
import os.path
import numpy as np
from collections import Counter, defaultdict
import util

USAGE = "%s <test data folder> <spam folder> <ham folder>"

def get_counts(file_list):
    """
    Computes counts for each word that occurs in the files in file_list.

    Inputs
    ------
    file_list : a list of filenames, suitable for use with open() or 
                util.get_words_in_file()

    Output
    ------
    A dict whose keys are words, and whose values are the number of files the
    key occurred in.
    """
    words_in_files = Counter()
    for file_name in file_list:
        words = set(util.get_words_in_file(file_name))
        words_in_files.update(words)

    return words_in_files

def get_log_probabilities(file_list):
    """
    Computes log-frequencies for each word that occurs in the files in 
    file_list.

    Input
    -----
    file_list : a list of filenames, suitable for use with open() or 
                util.get_words_in_file()

    Output
    ------
    A dict whose keys are words, and whose values are the log of the smoothed
    estimate of the fraction of files the key occurred in.

    Hint
    ----
    The data structure util.DefaultDict will be useful to you here, as will the
    get_counts() helper above.
    """
    words_in_files = get_counts(file_list)
    files_n = len(file_list)
#    print("word_counts",word_counts)
#    print("files_n",files_n)
    prob_dict = {}
    for key in words_in_files.keys():
        prob_dict[key] = np.log((words_in_files[key]+1) / (files_n+2))

    return prob_dict


def learn_distributions(file_lists_by_category):
    """
    Input
    -----
    A two-element list. The first element is a list of spam files, 
    and the second element is a list of ham (non-spam) files.

    Output
    ------
    (log_probabilities_by_category, log_prior)

    log_probabilities_by_category : A list whose first element is a smoothed
                                    estimate for log P(y=w_j|c=spam) (as a dict,
                                    just as in get_log_probabilities above), and
                                    whose second element is the same for c=ham.

    log_prior_by_category : A list of estimates for the log-probabilities for
                            each class:
                            [est. for log P(c=spam), est. for log P(c=ham)]
    """
    spam_files, ham_files = file_lists_by_category
    spam_n = len(spam_files)
    ham_n = len(ham_files)
    
    p_spam = (spam_n) / (spam_n + ham_n)
    p_ham = (ham_n) / (spam_n + ham_n)
    log_prior_by_category = [np.log(p_spam), np.log(p_ham)]

    log_probabilities_by_category = []

    spam_prob_dict = defaultdict(lambda: np.log(1 / (spam_n + 2)), get_log_probabilities(spam_files))
    ham_prob_dict = defaultdict(lambda: np.log(1 / (ham_n + 2)), get_log_probabilities(ham_files))
    
#    print("spam default", 1 / (spam_n + 2), np.log(1 / (spam_n + 2)))
#    print("ham default", 1 / (ham_n + 2), np.log(1 / (ham_n + 2)))
    
    log_probabilities_by_category = [spam_prob_dict, ham_prob_dict]

    return [log_probabilities_by_category, log_prior_by_category]

def classify_email(email_filename,
                   log_probabilities_by_category,
                   log_prior_by_category):
    """
    Uses Naive Bayes classification to classify the email in the given file.

    Inputs
    ------
    email_filename : name of the file containing the email to be classified

    log_probabilities_by_category : See output of learn_distributions

    log_prior_by_category : See output of learn_distributions

    Output
    ------
    One of the labels in names.
    """

    spam_i = 0
    ham_i = 1
    log_spam_prob_dict = log_probabilities_by_category[spam_i]
    log_ham_prob_dict = log_probabilities_by_category[ham_i]
    vocabulary = list(set(list(log_spam_prob_dict.keys()) + list(log_ham_prob_dict.keys())))
    email_words = (get_counts([email_filename])).keys()

#    print(len(vocabulary),len(log_spam_prob_dict.keys()),len(log_ham_prob_dict.keys()))
#    print(vocabulary)
#    print(log_spam_prob_dict.keys())
#    print(log_ham_prob_dict.keys())
#    print(len(email_words))

    log_p_c_spam_yj = log_prior_by_category[spam_i]
    log_p_c_ham_yj = log_prior_by_category[ham_i]
    
    
    for word in vocabulary:
#        print("=====================",word)
#        print("before",log_p_c_spam_yj, log_p_c_ham_yj,)
#        if(word in log_ham_prob_dict.keys()): print("in ham",log_ham_prob_dict[word])
#        if(word in log_spam_prob_dict.keys()): print("in spam",log_spam_prob_dict[word])
        if(word in email_words):
            log_p_c_spam_yj += log_spam_prob_dict[word]
            log_p_c_ham_yj += log_ham_prob_dict[word]
#            print("++>",log_p_c_spam_yj, log_p_c_ham_yj,)
        else:
            log_p_c_spam_yj += np.log(1 - np.exp(log_spam_prob_dict[word]))
            log_p_c_ham_yj += np.log(1 - np.exp(log_ham_prob_dict[word]))
#            print("??>",np.log(1 - np.exp(log_spam_prob_dict[word])), np.log(1 - np.exp(log_ham_prob_dict[word])))
#            print("-->",log_p_c_spam_yj, log_p_c_ham_yj,)
#        print("after",log_p_c_spam_yj, log_p_c_ham_yj,)


    label = 'ham'
    if(log_p_c_spam_yj - log_p_c_ham_yj >= 0):
        label = 'spam'
        
    return label

def classify_emails(spam_files, ham_files, test_files):
    # DO NOT MODIFY -- used by the autograder
    log_probabilities_by_category, log_prior = \
        learn_distributions([spam_files, ham_files])
    estimated_labels = []
    for test_file in test_files:
        estimated_label = \
            classify_email(test_file, log_probabilities_by_category, log_prior)
        estimated_labels.append(estimated_label)
    return estimated_labels

def main():
    ### Read arguments
    if len(sys.argv) != 4:
        print(USAGE % sys.argv[0])
    testing_folder = sys.argv[1]
    (spam_folder, ham_folder) = sys.argv[2:4]

    ### Learn the distributions
    file_lists = []
    for folder in (spam_folder, ham_folder):
        file_lists.append(util.get_files_in_folder(folder))
    (log_probabilities_by_category, log_priors_by_category) = \
            learn_distributions(file_lists)

    # Here, columns and rows are indexed by 0 = 'spam' and 1 = 'ham'
    # rows correspond to true label, columns correspond to guessed label
    performance_measures = np.zeros([2,2])

    ### Classify and measure performance
    for filename in (util.get_files_in_folder(testing_folder)):
        ## Classify
        label = classify_email(filename,
                               log_probabilities_by_category,
                               log_priors_by_category)
#        break
        ## Measure performance
        # Use the filename to determine the true label
        base = os.path.basename(filename)
        true_index = ('ham' in base)
        guessed_index = (label == 'ham')
        performance_measures[true_index, guessed_index] += 1


        # Uncomment this line to see which files your classifier
        # gets right/wrong:
        print("%s : %s" %(label, filename))

    template="You correctly classified %d out of %d spam emails, and %d out of %d ham emails."
    # Correct counts are on the diagonal
    correct = np.diag(performance_measures)
    # totals are obtained by summing across guessed labels
    totals = np.sum(performance_measures, 1)
    print(template % (correct[0],
                      totals[0],
                      correct[1],
                      totals[1]))

if __name__ == '__main__':
    main()
