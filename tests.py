from gensim.models import word2vec



# your path
wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')


wordvec = wv_model.wv
del wv_model


a = wordvec.most_similar(positive=['king', 'woman'], negative=['man'])
print(a)


