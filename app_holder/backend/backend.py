import json
from flask import Flask, request, jsonify
from gensim.models import word2vec

app = Flask(__name__)
wordvec = None

@app.route('/query', methods=['PUT'])
def index():
    query = json.loads(request.data)
    print(query)
    return jsonify(query)

'''def load():
    wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')
    wordvec = wv_model.wv
    del wv_model
    #breakpoint()'''

app.run(debug=True)