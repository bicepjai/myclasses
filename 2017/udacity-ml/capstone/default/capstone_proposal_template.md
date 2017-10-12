# Machine Learning Engineer Nanodegree
## Capstone Proposal
Jayaram Prabhu Durairaj  
August 20, 2017

## Proposal

### Domain Background

I have been taking NLP classes online to master NLP with deep learning along with MLND. I am following cs224n and oxford-cs-deepnlp-2017. This project will be a comprehensive study on important NLP classification methods. From the inception of word vectors concept, there has been a big change over from using count based models to word vector based models. Still there is not a significant difference in results because of algorithms in general [1]. There has not been a general model that could achieve state of the art results for all the tasks. In this project, I am planning to try many models learned over multiple Machine Learning and NLP courses, also models suggested in many research papers which will be cited in reference section and some new models created by myself.

Deep learning in medicine has been applied in a variety of applications such as image-based assessments of traumatic brain injuries, identify diseases from ordinary radiology image data, visualize and quantify heart flow in the body using any MRI machine, analyzes medical images to identify tumors, nearly invisible fractures, and other medical conditions.

A lot has been said during the past several years about how precision medicine and, more concretely, how genetic testing is going to disrupt the way diseases like cancer are treated. But this is only partially happening due to the huge amount of manual work still required. 



### Problem Statement

Kaggle along with Memorial Sloan Kettering Cancer Center (MSKCC) launched "Personalized Medicine: Redefining Cancer Treatment" competition, accepted by the NIPS 2017 Competition Track, because they need data scientists to help to take personalized medicine to its full potential. Once sequenced, a cancer tumor can have thousands of genetic mutations. But the challenge is distinguishing the mutations that contribute to tumor growth (drivers) from the neutral mutations (passengers). Currently this interpretation of genetic mutations is being done manually. This is a very time-consuming task where a clinical pathologist has to manually review and classify every single genetic mutation based on evidence from text-based clinical literature.

For this competition MSKCC is making available an expert-annotated knowledge base where world-class researchers and oncologists have manually annotated thousands of mutations. One needs to develop Machine Learning algorithms that, using this knowledge base as a baseline, automatically classifies genetic variations. 

### Datasets and Inputs

In this competition we have to develop algorithms to classify genetic mutations based on clinical evidence (text). There are nine different classes a genetic mutation can be classified on. This is not a trivial task since interpreting clinical evidence is very challenging even for human specialists. Therefore, modeling the clinical evidence (text) will be critical for the success of your approach.

Both, training and test, data sets are provided via two different files. One (training/test_variants) provides the information about the genetic mutations, whereas the other (training/test_text) provides the clinical evidence (text) that our human experts used to classify the genetic mutations. Both are linked via the ID field. Therefore the genetic mutation (row) with ID=15 in the file training_variants, was classified using the clinical evidence (text) from the row with ID=15 in the file training_text. Finally, to make it more exciting!! Some of the test data is machine-generated to prevent hand labeling. we have to submit all the results of the classification algorithm, and the machine-generated samples will be ignored. Following provides the file descriptions.

1. training_variants - a comma separated file containing the description of the genetic mutations used for training. Fields are ID (the id of the row used to link the mutation to the clinical evidence), Gene (the gene where this genetic mutation is located), Variation (the aminoacid change for this mutations), Class (1-9 the class this genetic mutation has been classified on)
2. training_text - a double pipe (||) delimited file that contains the clinical evidence (text) used to classify genetic mutations. Fields are ID (the id of the row used to link the clinical evidence to the genetic mutation), Text (the clinical evidence used to classify the genetic mutation)
3. test_variants - a comma separated file containing the description of the genetic mutations used for training. Fields are ID (the id of the row used to link the mutation to the clinical evidence), Gene (the gene where this genetic mutation is located), Variation (the aminoacid change for this mutations)
4. test_text - a double pipe (||) delimited file that contains the clinical evidence (text) used to classify genetic mutations. Fields are ID (the id of the row used to link the clinical evidence to the genetic mutation), Text (the clinical evidence used to classify the genetic mutation)
submissionSample - a sample submission file in the correct format

### Solution Statement
I have divided the solutions to try into 3 categories

	1. Count-based classification methods
	2. Count-based classification ensemble methods
	3. Deep Learning methods

Scikit-Learn has most of the classification algorithms in really good api format. After converting the documents to Term-Frequency-Inverse-Document-Frequency matrix, the following available algorithms are used to predict the multi class log loss.

	1. Multinomial Naive Bayes
	2. Support Vector Machine
	3. Softmax Regression
	4. K Nearest Neighbour
	5. Gaussian Process Classifier
	6. Passive Aggresive Classifier
	7. Quadratic Discriminant Analysis
	8. AdaBoost Classifier
	9. Random Forest Classifier
	10. Extreme Randomization Trees

Some ensemble packages that are going to be used and tuned are 

	1. catboost
	2. xgboost
	3. lightgbm

Word Vectors took the NLP community by storm with its ability to be used in deep learning models. Following are some of the Deep Learning methods that will be used for text classification

	1. A Convolutional Neural Network for Modelling Sentences, Kalchbrenner et al. ACL 2014 [2]
	2. Convolutional Neural Networks for Sentence Classification [3]
	3. Very Deep Convolutional Networks for Text Classification [4]
	4. Character-level Convolutional Networks for Text Classification [5]
	5. Distributed Representations of Sentences and Documents [6]
	6. Semantic Compositionality through Recursive Matrix-Vector Spaces [7]

Finally I am going to make some new models based on my experience and knowledge that i have accumulated over MLND and other courses.

### Benchmark Model

There are no benchmarks available other than kaggle leadership board ranking. I am going to use ensemble models as benchmark models for personal validation before competing on kaggle leader-board.

### Evaluation Metrics

Submissions are evaluated on Multi Class Log Loss between the predicted probability and the observed target. Multi Class Log Loss is the multi-class version of the Logarithmic Loss metric. Each observation is in one class and for each observation, you submit a predicted probability for each class. The metric is negative the log likelihood of the model that says each test observation is chosen independently from a distribution that places the submitted probability mass on the corresponding class, for each observation.

$log loss = -\frac{1}{N}\sum_{i=1}^N\sum_{j=1}^My_{i,j}\log(p_{i,j})$

where $N$ is the number of observations, $M$ is the number of class labels, $\log$ is the natural logarithm, $y_{i,j}$ is 1 if observation $i$ is in class $j$ and $0$ otherwise, and $p_{i,j}$ is the predicted probability that observation $i$ is in class $j$.

Both the solution file and the submission file are CSV's where each row corresponds to one observation, and each column corresponds to a class. The solution has 1's and 0's (exactly one "1" in each row), while the submission consists of predicted probabilities.

The submitted probabilities need not sum to 1, because they will be rescaled (each is divided by the sum) so that they do before evaluation.

### Project Design

Planning to use Jupyter notebook for all the necessary tasks so that it can be well documented for reference later. All the training and validation will be performed in from the training data-set. 

Custom text vectorizer will be used since it has to be generic with the task at hand. Medical data has lot of new scientific vocabulary that needs to be considered. After reviewing the textual data from training and testing data-set, they will be properly cleaned and all converted to lower case and cleaned to conform to "UTF-8" format. Custom regular expressions will be used to remove more frequent useless words such as urls, tables and figure information. All the stop-words will removed but lemmatization will not be performed since we might risk losing medical vocabulary. After applying the same prepossessing for all the text data available, we are ready to create the vocabulary for the corpus.

The count based models will be used to estimate the classification task using the TF-IDF matrix. Then using the same TF-IDF matrix the ensemble methods will be used to estimate the log loss. 

For deep learning models, its important to get meaningful word vectors which will form the base for how well models created will perform. After obtaining the corpus (train and test data-set) vocabulary, we need to obtain vectors already trained and available such as bioNLP [8] vectors and glove [9] vectors. These vectors have been tested on large corpus. More importance will be given to the bioNLP vectors since they were trained on medical corpus. All the remaining words in the corpus that are not in bioNLP vectors will be updated with glove vectors. The remaining words will be set randomly and we have to find words to train skip-gram model on them to make the word vectors able to capture semantic meaningful relations.

Kaggle allows external textual data to be used. We have to implement skip-gram [10] model algorithm to create/update corpus word vectors.  Any allowed external textual data will be preprocessed similar to training and testing data-sets. These text will be used to update the word vectors with the above created algorithm that will capture more domain related information. This process will make the downstream models more reliable and robust.

After word-vectors are are created , I will be able to implement all the above discussed models that will try and reduce log-loss to compete with other high precise models in the competition.

### Reference

[1] [Improving Distributional Similarity with Lessons Learned from Word Embeddings, Omer Levy, Yoav Goldberg, Ido Dagan](https://levyomer.files.wordpress.com/2015/03/improving-distributional-similarity-tacl-2015.pdf)
[2] [A Convolutional Neural Network for Modelling Sentences, Kalchbrenner et al. ACL 2014](http://www.aclweb.org/anthology/P14-1062)
[3] [Convolutional Neural Networks for Sentence Classification](http://www.aclweb.org/anthology/D14-1181)
[4] [Very Deep Convolutional Networks for Text Classification](https://arxiv.org/abs/1606.01781)
[5] [Character-level Convolutional Networks for Text Classification](https://arxiv.org/abs/1509.01626)
[6] [Distributed Representations of Sentences and Documents](https://cs.stanford.edu/~quocle/paragraph_vector.pdf)
[7] [Semantic Compositionality through Recursive Matrix-Vector Spaces](https://nlp.stanford.edu/pubs/SocherHuvalManningNg_EMNLP2012.pdf)
[8] [Word vectors trained on PubMed and PMC texts](http://bio.nlplab.org/)
[9] [glove vectors](https://nlp.stanford.edu/projects/glove/)
[10] [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/pdf/1301.3781.pdf)

