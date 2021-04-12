from train import OUT_DIR, NUM_SPLIT, PICKLED_CORPUS_PATH, TRAIN_PARAMS, MODEL_OUT_PATH, cfg_str

# good ones for window2
EPOCH_TO_LOAD = 340
EPOCH_TO_LOAD = 260

# good ones for window8
EPOCH_TO_LOAD = 40

from gensim.models import Word2Vec
model = Word2Vec.load(MODEL_OUT_PATH.format(**locals(), epochs=EPOCH_TO_LOAD))
wv = model.wv
del model

# NOTE: this would be cleaner
# from gensim.models import KeyedVectors
# wv = KeyedVectors.load(MODEL_OUT_PATH.format(**locals(), epochs=EPOCH_TO_LOAD))

result = wv.most_similar(positive=['woman', 'king'], negative=['man'])
most_similar_key, similarity = result[0]  # look at the first match
print(f"{most_similar_key}: {similarity:.4f}")
