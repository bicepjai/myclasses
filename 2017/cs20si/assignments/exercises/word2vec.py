import numpy as np
import pandas as pd

import os
import shutil
import time

from tqdm import tqdm
import functools

import matplotlib
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.client import device_lib
from tensorflow.contrib.tensorboard.plugins import projector

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']

print(tf.__version__)
get_available_gpus()

import glob, os, shutil
# for f in glob.glob("/tmp/tb/word2vec/*"):
#     shutil.rmtree(f)

VOCAB_SIZE = 50000
SKIP_WINDOW = 1 # the context window
BATCH_SIZE = 128
EMBED_SIZE = 128 # dimension of the word embedding vectors
N_NEG_SAMPLES = 32    # Number of negative examples to sample.
LEARNING_RATE = 1.0
EPOCHS = 100000
SKIP_STEP = 2000 #how many steps to skip before reporting the loss

# http://danijar.com/structuring-your-tensorflow-models/
def doublewrap(function):
    """
    A decorator decorator, allowing to use the decorator to be used without
    parentheses if not arguments are provided. All arguments must be optional.
    """
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return function(args[0])
        else:
            return lambda wrapee: function(wrapee, *args, **kwargs)
    return decorator


@doublewrap
def define_scope(function, scope=None, *args, **kwargs):
    """
    A decorator for functions that define TensorFlow operations. The wrapped
    function will only be executed once. Subsequent calls to it will directly
    return the result so that operations are added to the graph only once.
    The operations added by the function live within a tf.variable_scope(). If
    this decorator is used with arguments, they will be forwarded to the
    variable scope. The scope name defaults to the name of the wrapped
    function.
    """
    attribute = '_cache_' + function.__name__
    name = scope or function.__name__
    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self, attribute):
            with tf.variable_scope(name, *args, **kwargs):
                setattr(self, attribute, function(self))
        return getattr(self, attribute)
    return decorator

class SkipGramModel:
    """ Build the graph for word2vec model """
    def __init__(self, batch_generator, epochs, learning_rate):

        self.batch_generator = batch_generator
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.global_step = tf.Variable(0, trainable=False, dtype=tf.int32, name="global_step")

        self.Placeholders
        self.Embedding
        self.Loss
        self.Optimizer
        self.Summaries

    @define_scope
    def Placeholders(self):
        """ Step 1: define the placeholders for input and output """
        self.batch_inputs = tf.placeholder(tf.int32, shape=[BATCH_SIZE], name="center_words")
        self.batch_labels = tf.placeholder(tf.int32, shape=[BATCH_SIZE,1], name="target_words")

    @define_scope
    def Embedding(self):
        """ Step 2: define weights. In word2vec, it's actually the weights that we care about """
        self.embedding_matrix = tf.Variable(tf.random_uniform([BATCH_SIZE, EMBED_SIZE], -1.0, 1.0),
                                            name="embedding_matrix")
        self.batch_embeddings = tf.nn.embedding_lookup(self.embedding_matrix, self.batch_inputs)

        norm = tf.sqrt(tf.reduce_mean(tf.square(self.embedding_matrix), 1, keep_dims=True))
        self.normalized_embedding_matrix = self.embedding_matrix / norm


    @define_scope
    def Loss(self):
        """ Step 3 + 4: define the inference + the loss function """
        nce_weights = tf.Variable(tf.truncated_normal([VOCAB_SIZE, EMBED_SIZE], stddev=1.0/EMBED_SIZE ** 0.5))
        nce_biases   = tf.Variable(tf.zeros([VOCAB_SIZE]))
        self.loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights, biases=nce_biases,
                                             labels=tf.cast(self.batch_labels, tf.float32),
                                             inputs=self.batch_embeddings,
                                             num_sampled=N_NEG_SAMPLES, num_classes=VOCAB_SIZE))

    @define_scope
    def Optimizer(self):
        """ Step 5: define optimizer """
        self.optimizer = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss,
                                                                                        global_step=self.global_step)

    @define_scope
    def Summaries(self):
        tf.summary.scalar("loss", self.loss)
        tf.summary.histogram("histogram_loss", self.loss)
        # because you have several summaries, we should merge them all
        # into one op to make it easier to manage
        self.summary_op = tf.summary.merge_all()

    def Train(self):
        """ Training """

        # https://stackoverflow.com/questions/37337728/tensorflow-internalerror-blas-sgemm-launch-failed
        if 'session' in locals() and session is not None:
            print('Close interactive session')
            session.close()

        saver = tf.train.Saver() # defaults to saving all variables
        initial_step = 0
        with tf.device("/gpu:1"):
            config_sp = tf.ConfigProto(allow_soft_placement=True)
            with tf.Session(config=config_sp) as sess:                # initialize the necessary variables, in this case, w and b
                sess.run(tf.global_variables_initializer())

                ckpt = tf.train.get_checkpoint_state(os.path.dirname('/tmp/tb/word2vec/checkpoints/checkpoint'))
                # if that checkpoint exists, restore from checkpoint
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)

                writer = tf.summary.FileWriter("/tmp/tb/word2vec/improved_graph/lr"+str(self.learning_rate),
                                               sess.graph)

                total_loss = 0.0 # we use this to calculate late average loss in the last SKIP_STEP steps
                loss_batch = 0

                initial_step = self.global_step.eval()
                for epoch in tqdm(xrange(initial_step, self.epochs - initial_step)):

                    center_word_indices, target_word_indices = self.batch_generator.next()
                    feed_dict={self.batch_inputs: center_word_indices, self.batch_labels: target_word_indices}



                    # to deal with  summary_op issue
                    # https://stackoverflow.com/questions/38243194/tensorflow-feed-dict-error-you-must-feed-a-value-for-placeholder-tensor
                    # loss_batch, _, final_embedding_matrix, summary = sess.run([self.loss, self.optimizer,
                    #                                                            self.normalized_embedding_matrix,
                    #                                                            self.summary_op],
                    #                                                           feed_dict=feed_dict)
                    # writer.add_summary(summary, global_step=epoch)

                    loss_batch, _, final_embedding_matrix = sess.run([self.loss, self.optimizer,
                                                                               self.normalized_embedding_matrix],
                                                                              feed_dict=feed_dict)

                    total_loss += loss_batch
                    if (epoch + 1) % SKIP_STEP == 0:
                        tqdm.write('Average loss at step {}: {:5.1f}'.format(epoch, total_loss / SKIP_STEP))
                        total_loss = 0.0
                        saver.save(sess, "/tmp/tb/word2vec/checkpoints/skip-gram", epoch)

                # code to visualize the embeddings
                # it has to variable. constants don't work here.
                final_embedding_matrix = sess.run(self.normalized_embedding_matrix)
                embedding_var = tf.Variable(final_embedding_matrix[:1000], name='embedding')
                sess.run(embedding_var.initializer)

                config = projector.ProjectorConfig()
                summary_writer = tf.summary.FileWriter('/tmp/tb/word2vec/visualize')

                # add embedding to the config file
                embedding = config.embeddings.add()
                embedding.tensor_name = embedding_var.name

                # link this tensor to its metadata file, in this case the first 500 words of vocab
                embedding.metadata_path = '/home/bicepjai/Projects/myclasses/2017/cs20si/assignments/exercises/vocab_1000.tsv'

                # saves a configuration file that TensorBoard will read during startup.
                projector.visualize_embeddings(summary_writer, config)
                saver_embed = tf.train.Saver([embedding_var])
                saver_embed.save(sess, '/tmp/tb/word2vec/visualize/visual_embed.ckpt', 1)
                summary_writer.close()

            writer.close()

from process_data import process_data
batch_generator = process_data(VOCAB_SIZE, BATCH_SIZE, SKIP_WINDOW)

skipgram = SkipGramModel(batch_generator, EPOCHS, LEARNING_RATE)
skipgram.Train()
