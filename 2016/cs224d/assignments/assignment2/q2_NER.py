import os
import getpass
import sys
import time

import numpy as np
import tensorflow as tf
from q2_initialization import xavier_weight_init
import data_utils.utils as du
import data_utils.ner as ner
from utils import data_iterator
from model import LanguageModel

import copy

# import pdb
# pdb.set_trace()

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('summaries_dir', '/tmp/q2_ner', 'Summaries directory')

def variable_summaries(var, name):
  with tf.name_scope("summaries"):
    mean = tf.reduce_mean(var)
    tf.scalar_summary('mean/' + name, mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_sum(tf.square(var - mean)))
    tf.scalar_summary('stddev/' + name, stddev)
    tf.scalar_summary('max/' + name, tf.reduce_max(var))
    tf.scalar_summary('min/' + name, tf.reduce_min(var))
    tf.histogram_summary(name, var)

class Config(object):
  """Holds model hyperparams and data information.

  The config class is used to store various hyperparameters and dataset
  information parameters. Model objects are passed a Config() object at
  instantiation.
  """
  embed_size = 50
  batch_size = 64
  label_size = 5
  hidden_size = 100
  max_epochs = 50
  early_stopping = 2
  dropout = 0.9
  lr = 0.001
  l2 = 0.001
  window_size = 3

class NERModel(LanguageModel):
  """Implements a NER (Named Entity Recognition) model.

  This class implements a deep network for named entity recognition. It
  inherits from LanguageModel, which has an add_embedding method in addition to
  the standard Model method.
  """

  def load_data(self, debug=False):
    """Loads starter word-vectors and train/dev/test data."""
    # Load the starter word vectors
    self.wv, word_to_num, num_to_word = ner.load_wv(
      'data/ner/vocab.txt', 'data/ner/wordVectors.txt')
    tagnames = ['O', 'LOC', 'MISC', 'ORG', 'PER']
    self.num_to_tag = dict(enumerate(tagnames))
    tag_to_num = {v:k for k,v in self.num_to_tag.iteritems()}

    # Load the training set
    docs = du.load_dataset('data/ner/train')
    self.X_train, self.y_train = du.docs_to_windows(
        docs, word_to_num, tag_to_num, wsize=self.config.window_size)
    if debug:
      self.X_train = self.X_train[:1024]
      self.y_train = self.y_train[:1024]

    # Load the dev set (for tuning hyperparameters)
    docs = du.load_dataset('data/ner/dev')
    self.X_dev, self.y_dev = du.docs_to_windows(
        docs, word_to_num, tag_to_num, wsize=self.config.window_size)
    if debug:
      self.X_dev = self.X_dev[:1024]
      self.y_dev = self.y_dev[:1024]

    # Load the test set (dummy labels only)
    docs = du.load_dataset('data/ner/test.masked')
    self.X_test, self.y_test = du.docs_to_windows(
        docs, word_to_num, tag_to_num, wsize=self.config.window_size)

    # print details of data
    print "X_train: " + str(self.X_train.shape) + " " + "y_train:" + str(self.y_train.shape)
    print "X_dev: " + str(self.X_dev.shape) + " " + "y_dev:" + str(self.y_dev.shape)
    print "X_test: " + str(self.X_test.shape) + " " + "y_train:" + str(self.y_test.shape)
    print ""

  def add_placeholders(self):
    """Generate placeholder variables to represent the input tensors

    These placeholders are used as inputs by the rest of the model building
    code and will be fed data during training.  Note that when "None" is in a
    placeholder's shape, it's flexible

    Adds following nodes to the computational graph

    input_placeholder: Input placeholder tensor of shape
                       (None, window_size), type tf.int32
    labels_placeholder: Labels placeholder tensor of shape
                        (None, label_size), type tf.float32
    dropout_placeholder: Dropout value placeholder (scalar),
                         type tf.float32

    Add these placeholders to self as the instance variables
  
      self.input_placeholder
      self.labels_placeholder
      self.dropout_placeholder

    (Don't change the variable names)
    """
    ### YOUR CODE HERE

    self.input_placeholder = tf.placeholder(tf.int32, 
                              # shape=(self.config.batch_size, self.config.window_size),
                              shape=None,
                              name="input")
    self.labels_placeholder = tf.placeholder(tf.float32, 
                              # shape=(self.config.batch_size, self.config.label_size),
                              shape=None,
                              name="labels")
    self.dropout_placeholder = tf.placeholder(tf.float32, name="dropout")

    ### END YOUR CODE

  def create_feed_dict(self, input_batch, dropout, label_batch=None):
    """Creates the feed_dict for softmax classifier.

    A feed_dict takes the form of:

    feed_dict = {
        <placeholder>: <tensor of values to be passed for placeholder>,
        ....
    }

    Hint: The keys for the feed_dict should be a subset of the placeholder
          tensors created in add_placeholders.
    Hint: When label_batch is None, don't add a labels entry to the feed_dict.
    
    Args:
      input_batch: A batch of input data.
      label_batch: A batch of label data.
    Returns:
      feed_dict: The feed dictionary mapping from placeholders to values.
    """
    ### YOUR CODE HERE

    feed_dict = {
        self.input_placeholder: input_batch,
        self.dropout_placeholder: dropout
    }
    if np.any(label_batch):
        feed_dict[self.labels_placeholder] = label_batch

    ### END YOUR CODE
    return feed_dict

  def add_embedding(self):
    """Add embedding layer that maps from vocabulary to vectors.

    Creates an embedding tensor (of shape (len(self.wv), embed_size). Use the
    input_placeholder to retrieve the embeddings for words in the current batch.

    (Words are discrete entities. They need to be transformed into vectors for use
    in deep-learning. Although we won't do so in this problem, in practice it's
    useful to initialize the embedding with pre-trained word-vectors. For this
    problem, using the default initializer is sufficient.)

    Hint: This layer should use the input_placeholder to index into the
          embedding.
    Hint: You might find tf.nn.embedding_lookup useful.
    Hint: See following link to understand what -1 in a shape means.
      https://www.tensorflow.org/versions/r0.8/api_docs/python/array_ops.html#reshape
    Hint: Check the last slide from the TensorFlow lecture.
    Hint: Here are the dimensions of the variables you will need to create:

      L: (len(self.wv), embed_size)

    Returns:
      window: tf.Tensor of shape (-1, window_size*embed_size)
    """
    # The embedding lookup is currently only implemented for the CPU
    with tf.device('/cpu:0'):
      ### YOUR CODE HERE

      # using these namescopes for better looking graphs in tensorboard
      with tf.name_scope('Embedding'):
        embeddings = tf.Variable(
          tf.random_uniform([len(self.wv), self.config.embed_size], -1.0, 1.0))
        embed = tf.nn.embedding_lookup(embeddings, self.input_placeholder)
        window = tf.reshape(embed, [-1, self.config.window_size*self.config.embed_size])

      ### END YOUR CODE
      return window

  def add_model(self, window):
    """Adds the 1-hidden-layer NN.

    Hint: Use a variable_scope (e.g. "Layer") for the first hidden layer, and
          another variable_scope (e.g. "Softmax") for the linear transformation
          preceding the softmax. Make sure to use the xavier_weight_init you
          defined in the previous part to initialize weights.
    Hint: Make sure to add in regularization and dropout to this network.
          Regularization should be an addition to the cost function, while
          dropout should be added after both variable scopes.
    Hint: You might consider using a tensorflow Graph Collection (e.g
          "total_loss") to collect the regularization and loss terms (which you
          will add in add_loss_op below).
    Hint: Here are the dimensions of the various variables you will need to
          create

          W:  (window_size*embed_size, hidden_size)
          b1: (hidden_size,)
          U:  (hidden_size, label_size)
          b2: (label_size)

    https://www.tensorflow.org/versions/r0.7/api_docs/python/framework.html#graph-collections
    Args:
      window: tf.Tensor of shape (-1, window_size*embed_size)
    Returns:
      output: tf.Tensor of shape (batch_size, label_size)
    """
    ### YOUR CODE HERE

    with tf.name_scope('Layer1'):
      
      with tf.name_scope('weights'):
        W = tf.get_variable("W_weights", 
                          (self.config.window_size*self.config.embed_size, self.config.hidden_size),
                          initializer=xavier_weight_init())
        variable_summaries(W, 'Layer1/weights')

      with tf.name_scope('biases'):
        b1 = tf.get_variable("bias1", (self.config.hidden_size,),
                          initializer=tf.constant_initializer(0.0))
        variable_summaries(b1, 'Layer1/biases')

      with tf.name_scope('tanh_Wx_plus_b'):
        h1 = tf.tanh(tf.matmul(window, W) + b1)

    dropped1 = tf.nn.dropout(h1, self.config.dropout)

    with tf.name_scope('Layer2'):
      
      with tf.name_scope('weights'):
        U = tf.get_variable("U_weights", 
                          (self.config.hidden_size, self.config.label_size),
                          initializer=xavier_weight_init())
        variable_summaries(W, 'Layer2/weights')

      with tf.name_scope('biases'):
        b2 = tf.get_variable("bias2", (self.config.label_size,),
                          initializer=tf.constant_initializer(0.0))
        variable_summaries(b1, 'Layer2/biases')

      with tf.name_scope('Uh_plus_b'):
        # this layer is before softmax as we are calculating it in loss op
        h2 = tf.matmul(dropped1, U) + b2

    # add dropout
    dropped2 = tf.nn.dropout(h2, self.config.dropout)
    output = dropped2

    with tf.name_scope('Regularization'):
      regW = tf.reduce_sum(tf.pow(W, 2))
      regU = tf.reduce_sum(tf.pow(U, 2))
      reg = self.config.l2 * 0.5 * (regW + regU)
      tf.add_to_collection("reg_term", reg)
      variable_summaries(reg, 'reg_term')

    ### END YOUR CODE
    return output 

  def add_loss_op(self, pred):
    """Adds cross_entropy_loss ops to the computational graph.

    Hint: You can use tf.nn.softmax_cross_entropy_with_logits to simplify your
          implementation. You might find tf.reduce_mean useful.
    Args:
      pred: A tensor of shape (batch_size, n_classes)
    Returns:
      loss: A 0-d tensor (scalar)
    """
    ### YOUR CODE HERE
    
    with tf.name_scope('CE_Loss'):
      loss_tensor = tf.nn.softmax_cross_entropy_with_logits(pred, self.labels_placeholder)
      loss = tf.reduce_mean(loss_tensor)

    with tf.name_scope('Total_Loss'):
      reg_term = tf.get_collection("reg_term", scope=None)[0]
      loss = loss + reg_term
      variable_summaries(loss, 'total_loss')

    ### END YOUR CODE
    return loss

  def add_training_op(self, loss):
    """Sets up the training Ops.

    Creates an optimizer and applies the gradients to all trainable variables.
    The Op returned by this function is what must be passed to the
    `sess.run()` call to cause the model to train. See 

    https://www.tensorflow.org/versions/r0.7/api_docs/python/train.html#Optimizer

    for more information.

    Hint: Use tf.train.AdamOptimizer for this model.
          Calling optimizer.minimize() will return a train_op object.

    Args:
      loss: Loss tensor, from cross_entropy_loss.
    Returns:
      train_op: The Op for training.
    """
    ### YOUR CODE HERE
    
    with tf.name_scope('train'):
      train_op = tf.train.GradientDescentOptimizer(learning_rate=self.config.lr)
      train_op = train_op.minimize(loss)

    ### END YOUR CODE
    return train_op

  def __init__(self, config):
    """Constructs the network using the helper functions defined above."""
    self.config = config
    
    self.load_data(debug=False)
    
    self.add_placeholders()
    
    window = self.add_embedding()

    y = self.add_model(window)

    self.loss = self.add_loss_op(y)

    self.predictions = tf.nn.softmax(y)
    
    one_hot_prediction = tf.argmax(self.predictions, 1)
    correct_prediction = tf.equal(
        tf.argmax(self.labels_placeholder, 1), one_hot_prediction)
    self.correct_predictions = tf.reduce_sum(tf.cast(correct_prediction, 'int32'))
    
    self.train_op = self.add_training_op(self.loss)

  # modified run to include summaries and summary writer
  def run_epoch(self, epoch, session, input_data, input_labels, 
                merged_summaries, summary_writer,
                shuffle=True, verbose=True):
    orig_X, orig_y = input_data, input_labels
    dp = self.config.dropout
    # We're interested in keeping track of the loss and accuracy during training
    total_loss = []
    total_correct_examples = 0
    total_processed_examples = 0
    total_steps = len(orig_X) / self.config.batch_size
    for step, (x, y) in enumerate(
      data_iterator(orig_X, orig_y, batch_size=self.config.batch_size,
                   label_size=self.config.label_size, shuffle=shuffle)):
      feed = self.create_feed_dict(input_batch=x, dropout=dp, label_batch=y)

      # modified run to include summaries that were created
      summary, loss, total_correct, _ = session.run(
          [merged_summaries, self.loss, self.correct_predictions, self.train_op],
          feed_dict=feed)
      summary_writer.add_summary(summary, epoch)

      total_processed_examples += len(x)
      total_correct_examples += total_correct
      total_loss.append(loss)
      ##
      if verbose and step % verbose == 0:
        sys.stdout.write('\r{} / {} : loss = {}'.format(
            step, total_steps, np.mean(total_loss)))
        sys.stdout.flush()
    if verbose:
        sys.stdout.write('\r')
        sys.stdout.flush()

    return np.mean(total_loss), total_correct_examples / float(total_processed_examples)

  def predict(self, session, X, y=None):
    """Make predictions from the provided model."""
    # If y is given, the loss is also calculated
    # We deactivate dropout by setting it to 1
    dp = 1
    losses = []
    results = []
    if np.any(y):
        data = data_iterator(X, y, batch_size=self.config.batch_size,
                             label_size=self.config.label_size, shuffle=False)
    else:
        data = data_iterator(X, batch_size=self.config.batch_size,
                             label_size=self.config.label_size, shuffle=False)
    for step, (x, y) in enumerate(data):
      feed = self.create_feed_dict(input_batch=x, dropout=dp)
      if np.any(y):
        feed[self.labels_placeholder] = y
        loss, preds = session.run(
            [self.loss, self.predictions], feed_dict=feed)
        losses.append(loss)
      else:
        preds = session.run(self.predictions, feed_dict=feed)

      predicted_indices = preds.argmax(axis=1)
      results.extend(predicted_indices)
    return np.mean(losses), results

def print_confusion(confusion, num_to_tag):
    """Helper method that prints confusion matrix."""
    # Summing top to bottom gets the total number of tags guessed as T
    total_guessed_tags = confusion.sum(axis=0)
    # Summing left to right gets the total number of true tags
    total_true_tags = confusion.sum(axis=1)
    print
    print confusion
    for i, tag in sorted(num_to_tag.items()):
        prec = confusion[i, i] / float(total_guessed_tags[i])
        recall = confusion[i, i] / float(total_true_tags[i])
        print 'Tag: {} - P {:2.4f} / R {:2.4f}'.format(tag, prec, recall)

def calculate_confusion(config, predicted_indices, y_indices):
    """Helper method that calculates confusion matrix."""
    confusion = np.zeros((config.label_size, config.label_size), dtype=np.int32)
    for i in xrange(len(y_indices)):
        correct_label = y_indices[i]
        guessed_label = predicted_indices[i]
        confusion[correct_label, guessed_label] += 1
    return confusion

def save_predictions(predictions, filename):
  """Saves predictions to provided file."""
  with open(filename, "wb") as f:
    for prediction in predictions:
      f.write(str(prediction) + "\n")


#modified to add config
def test_NER(config):
  """Test NER model implementation.

  You can use this function to test your implementation of the Named Entity
  Recognition network. When debugging, set max_epochs in the Config object to 1
  so you can rapidly iterate.
  """

  with tf.Graph().as_default():
    model = NERModel(config)

    init = tf.initialize_all_variables()
    saver = tf.train.Saver()

    with tf.Session() as session:
      best_val_loss = float('inf')
      best_val_epoch = 0

      # tensor board summaries
      merged_summaries = tf.merge_all_summaries()
      summary_writer = tf.train.SummaryWriter(FLAGS.summaries_dir, session.graph)

      session.run(init)

      for epoch in xrange(config.max_epochs):
        print 'Epoch {}'.format(epoch)
        start = time.time()
        ###

        train_loss, train_acc = model.run_epoch(epoch, session, 
                                                model.X_train, model.y_train, 
                                                merged_summaries, summary_writer, 
                                                verbose=True)
        val_loss, predictions = model.predict(session, model.X_dev, model.y_dev)
        print 'Training loss: {}'.format(train_loss)
        print 'Training acc: {}'.format(train_acc)
        print 'Validation loss: {}'.format(val_loss)
        if val_loss < best_val_loss:
          best_val_loss = val_loss
          best_val_epoch = epoch
          if not os.path.exists("./weights"):
            os.makedirs("./weights")
        
          saver.save(session, './weights/ner.weights')
        if epoch - best_val_epoch > config.early_stopping:
          break
        ###
        confusion = calculate_confusion(config, predictions, model.y_dev)
        print_confusion(confusion, model.num_to_tag)
        print 'Total time: {}'.format(time.time() - start)
      
      saver.restore(session, './weights/ner.weights')
      print 'Test'
      print '======-------======-------======'
      print 'Writing predictions to q2_test.predicted'
      _, predictions = model.predict(session, model.X_test, model.y_test)
      save_predictions(predictions, "q2_test.predicted")

  # returning val loss to fit hyper parameters
  return best_val_loss

def hyperParameterSearch(hyper_runs = 10):
  if tf.gfile.Exists(FLAGS.summaries_dir):
    tf.gfile.DeleteRecursively(FLAGS.summaries_dir)
  tf.gfile.MakeDirs(FLAGS.summaries_dir)

  config = Config()
  
  best_loss = float('inf')
  best_config = None

  for hyper_run in xrange(hyper_runs):
    # setting hyper parameters
    config.l2 = 10**np.random.uniform(-5,-1)
    config.lr = 10**np.random.uniform(-3,-1)
    
    print "=======================hyperparameters search "+ str(hyper_run) +"==============="
    print "lr: "+ str(config.lr)
    print "l2: "+ str(config.l2)

    loss = test_NER(config)
    if(loss < best_loss):
      best_loss = loss
      best_config = copy.copy(config)
  
  return best_config

if __name__ == "__main__":
  best_config =  hyperParameterSearch(hyper_runs = 20)
  #best run
  print "===================BEST Model Run================="
  print "lr: "+ str(best_config.lr)
  print "l2: "+ str(best_config.l2)
  test_NER( best_config )
