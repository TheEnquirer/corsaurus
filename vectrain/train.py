# scratchpad for training custom word vectors
# originally based off of https://nbviewer.jupyter.org/github/jennselby/MachineLearningTutorials/blob/master/WordVectors.ipynb

from gensim.models import word2vec, Word2Vec
import os
import pickle

import logging

CORPUS_DIR = 'data/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled'
SPLIT_CORPUS_DIR = 'data/1-billion-word-language-modeling-benchmark-r13output/training_monolingual_split'

TRAIN_PARAMS = {
    'vector_size': 300,
    'window': 2,
    'min_count': 5,
        }

def serialize_config(cfg):
    return ','.join(f'{k}{v}' for k, v in cfg.items())

# # load vocab
# if __name__ == '__main__':
#     # takes ab 3 min on hotpotato
#     sentences = word2vec.PathLineSentences(CORPUS_DIR)
#     print('got sentences')
#     model = word2vec.Word2Vec(**TRAIN_PARAMS, workers=10)
#     print('got model')
#     model.build_vocab(sentences)
#     print('built vocab')
#     model.save(f'out/vocab_{serialize_config(TRAIN_PARAMS)}.model')
#     exit()

NUM_SPLIT = 4
DELTA_EPOCH = 20
# if __name__ == '__main__':
#     for i in range(NUM_SPLIT):
#         with open(f'temp_sentences_{i}', 'wb+') as wf:
#             print(SPLIT_CORPUS_DIR + f'/{i}')
#             sentences = word2vec.PathLineSentences(SPLIT_CORPUS_DIR + f'/{i}')
#             sentences_in_memory = list(sentences)
#             pickle.dump(sentences_in_memory, wf)
#             del sentences_in_memory

# train the model
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = Word2Vec.load(f'out/vocab_{serialize_config(TRAIN_PARAMS)}.model')
    sentences = word2vec.PathLineSentences(CORPUS_DIR)

    epochs = 0
    while True:
        for i in range(NUM_SPLIT):
            # sentences = word2vec.PathLineSentences(SPLIT_CORPUS_DIR + f'/{i}')
            # sentences_in_memory = list(sentences)
            with open(f'temp_sentences_{i}', 'rb') as rf:
                sentences_in_memory = pickle.load(rf)
                model.train(sentences_in_memory, total_examples=model.corpus_count/NUM_SPLIT, epochs=DELTA_EPOCH)
                model.save(f'out/trained_{epochs}_{serialize_config(TRAIN_PARAMS)}.model')
                del sentences_in_memory
                epochs += DELTA_EPOCH

