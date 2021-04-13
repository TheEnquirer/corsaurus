# scratchpad for training custom word vectors
# originally based off of https://nbviewer.jupyter.org/github/jennselby/MachineLearningTutorials/blob/master/WordVectors.ipynb

from gensim.models import word2vec, Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models.callbacks import CallbackAny2Vec
import os
import pickle

import logging

CORPUS_DIR = '/home/exr0n/vol/storage/datasets/word2vec_news_corpus/training-monolingual.tokenized.shuffled'
SPLIT_CORPUS_DIR = 'data/1-billion-word-language-modeling-benchmark-r13output/training_monolingual_split'
OUT_DIR = '/home/exr0n/vol/storage/model_snapshots/word2vec'

TRAIN_PARAMS = {
    'vector_size': 300,
    'window': 8,
    'min_count': 5,
        }

all_params = [
        # { 'vector_size':  64, 'window':  2, 'min_count': 5, },
        # { 'vector_size':  64, 'window':  5, 'min_count': 5, },
        # { 'vector_size':  64, 'window':  8, 'min_count': 5, },
        # { 'vector_size':  64, 'window': 12, 'min_count': 5, }, # NOTE: this one only trained for 17 epochs

        # { 'vector_size': 300, 'window':  2, 'min_count': 5, },
        # { 'vector_size': 300, 'window':  5, 'min_count': 5, },
        # { 'vector_size': 300, 'window':  8, 'min_count': 5, },
        # { 'vector_size': 300, 'window': 12, 'min_count': 5, },

        { 'vector_size': 500, 'window':  2, 'min_count': 5, },
        { 'vector_size': 500, 'window':  5, 'min_count': 5, },
        { 'vector_size': 500, 'window':  8, 'min_count': 5, },
        { 'vector_size': 500, 'window': 12, 'min_count': 5, },
    ]

def serialize_config(cfg):
    return ','.join(f'{k}{v}' for k, v in cfg.items())
cfg_str = serialize_config(TRAIN_PARAMS)

# actually save epochs correctly
# based on https://radimrehurek.com/gensim/models/callbacks.html#usage-examples

class EpochSaver(CallbackAny2Vec):
    '''Callback to save model after each epoch.'''

    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 0

    def on_epoch_end(self, model):
        output_path = get_tmpfile('{}_epoch{}.model'.format(self.path_prefix, self.epoch))
        model.save(output_path)
        self.epoch += 1

# modified from commit 4bd4af46c9089b48eed36428ef067574bdd17f32

# train the model
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.PathLineSentences(CORPUS_DIR)
    for cfg in all_params:
        callbacks = [ EpochSaver(f'{OUT_DIR}/trained_{serialize_config(cfg)}') ]
        model = Word2Vec(sentences, **TRAIN_PARAMS, workers=10, callbacks=callbacks, epochs=30)

# end modified from commit 4bd4af46c9089b48eed36428ef067574bdd17f32

# NUM_SPLIT = 4
# PICKLED_CORPUS_PATH = 'data/pickles_{}.pickle'
# # # compress the corpus
# # if __name__ == '__main__':
# #     # takes 5 min on hotpotato
# #     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# #     for i in range(NUM_SPLIT):
# #         with open(PICKLED_CORPUS_PATH.format(i), 'wb+') as wf:
# #             print(SPLIT_CORPUS_DIR + f'/{i}')
# #             sentences = word2vec.PathLineSentences(SPLIT_CORPUS_DIR + f'/{i}')
# #             sentences_in_memory = list(sentences)
# #             pickle.dump(sentences_in_memory, wf, protocol=-1) # TODO: re-run with higher pickle number, cur is 4 (default for 3.9)
# #             del sentences_in_memory
#
# # build vocab
# if __name__ == '__main__':
#     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#     model = word2vec.Word2Vec(**TRAIN_PARAMS, workers=10)
#     model.build_vocab([['hello', 'world']]*TRAIN_PARAMS['min_count'])
#     for i in range(NUM_SPLIT):
#         with open(PICKLED_CORPUS_PATH.format(i), 'rb') as rf:
#             sentences_in_memory = pickle.load(rf)
#             model.build_vocab(sentences_in_memory, update=True, progress_per=int(1e5))
#             model.save(f'{OUT_DIR}/vocab_{cfg_str}.model')
#             del sentences_in_memory
#
# DELTA_EPOCH = 20
# MODEL_OUT_PATH = '{OUT_DIR}/trained_{epochs}_{cfg_str}.model' # NOTE: don't let the user touch this string, else RCE
# # train the model
# if __name__ == '__main__':
#     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#     model = Word2Vec.load(f'{OUT_DIR}/vocab_{cfg_str}.model')
#
#     epochs = 0
#     while True:
#         for i in range(NUM_SPLIT):
#             with open(PICKLED_CORPUS_PATH.format(i), 'rb') as rf:
#                 sentences_in_memory = pickle.load(rf)
#                 model.train(sentences_in_memory, total_examples=model.corpus_count, epochs=DELTA_EPOCH)
#                 epochs += DELTA_EPOCH
#                 model.save(MODEL_OUT_PATH.format(**locals()))
#                 del sentences_in_memory
#
