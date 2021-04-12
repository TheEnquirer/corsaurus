# scratchpad for training custom word vectors
# originally based off of https://nbviewer.jupyter.org/github/jennselby/MachineLearningTutorials/blob/master/WordVectors.ipynb

from gensim.models import word2vec
import os

CORPUS_DIR = 'data/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled'

TRAIN_PARAMS = {
    'vector_size': 300,
    'window': 5,
    'min_count': 5,
        }

if __name__ == '__main__':
    sentences = word2vec.PathLineSentences(CORPUS_DIR)
    print('got sentences')
    model = word2vec.Word2Vec(sentences, **TRAIN_PARAMS, workers=10)
    print('got model')
    model.save(f'vecs_{str(TRAIN_PARAMS)}')

