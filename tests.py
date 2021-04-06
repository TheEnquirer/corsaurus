from gensim.models import word2vec



# your path
wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')


wordvec = wv_model.wv
del wv_model

breakpoint()


# Cosmul seems to work better

# a = wordvec.most_similar(positive=['king', 'woman'], negative=['man'], topn=3)
# print(a)


# wordvec.most_similar_cosmul(positive=['sports', 'digital'], negative=['exercise'], topn=10)
# wordvec.most_similar(positive=['king', 'woman'], negative=['man'], topn=10)


