# pylint: disable=no-member
# * TO RUN THIS:
'''
First use this command:
$ export FLASK_APP=backend.py

Then, use this if you would like to enable dev mode (live reloading):
$ export FLASK_ENV=development

Finally, use this if you want a local server:
$ flask run

Or use this if you want other computers on the network to be able to access the backend server:
$ flask run --host=0.0.0.0

Oh, and if you want to go back to prod mode:
$ export FLASK_ENV=production
'''

import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gensim.models import word2vec

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

vecto = None

@app.route('/', methods=['GET'])
@cross_origin()
def root():
    app.logger.info('Hi :D')
    return 'Hi :D'

@app.route('/test', methods=['PUT'])
@cross_origin()
def test():
    content = json.loads(request.data)
    app.logger.info(content)
    return jsonify(content)

@app.route('/query', methods=['PUT'])
@cross_origin()
def query():
    global vecto
    app.logger.info('RECEIVED A QUERY.')
    try:
        #content = request.get_json()
        content = json.loads(request.data)
        '''
        content = request.data
        content = content.decode("utf-8")
        content = jsonify(content)
        '''
        app.logger.info(content)
        load_model()
        mode = content['mode'] # query mode

        # sum words together
        if mode == 'sum':
            num = content['num'] # natural number
            pos = content['pos'] # array of words
            neg = content['neg'] # array of words
            return jsonify(vecto.most_similar_cosmul(positive=pos, negative=neg, topn=num))
        # find words similar to given word
        elif mode == 'similar':
            word = content['word']
            return jsonify(vecto.most_similar(word))
        # find distance between two words
        elif mode == 'distance':
            words = content['words']
            return jsonify(vecto.distance(words[0], words[1]))
        # find distance between one word and group of words
        elif mode == 'distances':
            word = content['word']
            words = content['words']
            return jsonify(vecto.distances(word, words))
        # find outlier in group of words
        elif mode == 'outlier':
            words = content['words']
            return jsonify(vecto.doesnt_match(words))
        else:
          return {'message': 'You\'ve done goofed.'}
    except:
        app.logger.error(traceback.format_exc())
        return jsonify(traceback.format_exc())

def load_model():
  global vecto
  if vecto is None:
    wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')
    vecto = wv_model.wv
    del wv_model

app.logger.info('STARTING.')
load_model()
app.logger.info('STARTED.')

'''
EXAMPLE CODE FOR QUERYING:
fetch('BACKENDURL/query', {
  method: 'put',
  body: JSON.stringify(
  {
    'num': 10,
    'pos': ['king', 'woman'],
    'neg': ['man'],
    'mode': 'sum'
  }),
  headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
})
  .then((res) =>
  {
    let val = JSON.parse(res.text());
  })
  .catch((err) => console.error(err));
'''


'''
THIS IS MY NINJA WAY!
                                      ▓▓▓▓▓▓  ▓▓▓▓▓▓
                                      ▓▓  ░░▓▓▓▓  ▓▓▓▓▓▓
                                ▓▓▓▓▓▓▓▓░░  ░░▓▓░░░░▓▓▓▓  ▓▓
                              ▒▒▓▓░░  ▓▓░░░░░░░░░░░░▓▓░░░░▓▓
                                  ▒▒░░  ░░░░░░░░░░░░░░░░▓▓▓▓▒▒
                                  ▓▓░░░░░░░░░░░░░░░░░░░░▓▓░░▓▓
                ██████████    ▒▒▓▓░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░▓▓
            ██████      ██████    ▓▓▓▓▓▓▓▓▓▓▓▓▒▒    ▒▒▒▒▒▒▓▓▓▓
          ████              ████████▓▓▓▓▓▓▓▓▓▓▒▒    ▒▒  ▒▒▓▓
        ████                  ██████░░  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                          ██████████░░  ░░░░░░██░░░░░░████
                    ██████████    ██░░░░░░░░░░▒▒░░░░░░▒▒██
              ██████████          ██░░░░░░░░░░░░░░░░░░░░██
        ██████████                  ████░░░░░░░░░░░░░░░░██
      ██████                          ████░░░░░░▒▒▒▒░░██
    ████                              ██▓▓██░░░░░░░░██
  ████                          ████████▓▓▓▓████████
  ██                          ████▓▓▓▓▓▓████████▓▓██████
  ██                        ████▓▓▓▓▓▓▓▓▓▓██████▓▓██▓▓▓▓██
                          ▓▓████▓▓▓▓██▓▓▓▓▓▓▓▓██▓▓██▓▓██▓▓▓▓
                        ████████▓▓▓▓██▓▓▓▓▓▓▓▓██▓▓██▓▓██▓▓██
                      ██▓▓▓▓▓▓▓▓████████████████▓▓██████▓▓██
                      ██▓▓██▓▓▓▓████▒▒░░░░  ░░░░▓▓██▒▒██▓▓██
                    ██▓▓▓▓██████████▒▒  ░░░░    ▓▓██▒▒██▓▓████
                    ██▓▓▓▓▓▓████  ██▒▒░░    ░░░░▓▓██▒▒▒▒██████
                  ██▓▓▓▓▓▓▓▓██    ██▒▒░░░░      ▓▓██▒▒▒▒██▓▓██
                  ██▓▓▓▓▓▓▓▓██    ██▒▒░░░░░░░░░░░░▓▓██▒▒██▓▓██
                ██▓▓▓▓████▓▓██    ████▒▒░░    ░░░░▓▓██▒▒██▓▓▓▓██
                ██▓▓██░░░░██        ████████▓▓▓▓▓▓▓▓████████▓▓▓▓████
                  ██░░░░████        ████████████████████████▓▓████░░████
                ██░░░░░░░░██        ██▒▒░░░░░░░░░░░░░░░░████▓▓██░░░░░░░░██
                ██░░░░░░░░░░██      ██░░    ░░░░░░░░░░░░░░░░████░░░░░░░░██
                ██░░░░░░░░░░██      ██▒▒░░░░    ░░░░██░░░░░░████░░░░░░██
                ██░░░░░░░░██      ██▒▒  ▒▒▒▒▒▒░░░░░░██░░░░░░░░████████
                  ████████        ██████    ▒▒▒▒████░░████░░░░██
                                  ██    ████▒▒██  ████▒▒▒▒▒▒▒▒░░██
                                ██░░░░░░  ▒▒▒▒██    ██▒▒▒▒▒▒▒▒░░░░██
                                ██░░░░░░▒▒▒▒██        ██▒▒▒▒▒▒▒▒░░██
                              ██░░░░░░▒▒▒▒▒▒██        ██▒▒▒▒▒▒▒▒░░██
                            ██░░░░░░░░▒▒▒▒██            ██▒▒▒▒▒▒▒▒░░██
                            ██░░░░░░▒▒▒▒▒▒██            ██▒▒▒▒▒▒▒▒░░██
                          ██░░░░░░▒▒▒▒▒▒██              ██▒▒▒▒▒▒░░░░██
                        ██░░░░░░▒▒▒▒▒▒██                ██▒▒▒▒▒▒▒▒░░██
                        ██░░░░░░▒▒▒▒▒▒██                ██▒▒▒▒▒▒▒▒░░██
                          ██░░▒▒▒▒▒▒██                    ████████████
                        ████████████                        ████████
                        ██▓▓▓▓████                          ██▓▓▓▓██
                      ████████████                        ██▓▓██████████
                    ██▓▓▓▓▓▓▓▓██                          ██▓▓▓▓▓▓▓▓▓▓▓▓████
                  ██▓▓▓▓▓▓▓▓▓▓██                          ██████▓▓▓▓▓▓░░░░░░██
                ██▓▓░░░░░░░░████                                ██████████████
                ██████████████





 ▒ ▒ ▒ ▒ ▒ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ █ █ █ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ █ █ █ ▒ ▒
 ▒ ▒ █ █ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ █ ▒ ▒ █ ▒
 ▒ █ █ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ █ █ █ ▒ ▒ ▒ █ █ ▒ ▒ █ ▒
 ▒ ▒ ▒ ▒ █ █ █ █ █ ▒ ▒ █ ▒ ▒ █ ▒ ▒ █ █ █ ▒ █ █ ▒
 ▒ ▒ ▒ ▒ █ ▒ ▒ ▒ █ ▒ █ ▒ ▒ ▒ █ ▒ █ █ ▒ █ █ █ ▒ ▒
 ▒ ▒ ▒ █ ▒ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ █ █ █ ▒ █ █ █ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ █ ▒ ▒ ▒ ▒ █ █ █ █ █ ▒ █ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ █ █ ▒ █ █ ▒ █ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ ▒ █ ▒ ▒ ▒ █ █ █ ▒ ▒ ▒ ▒
 ▒ ▒ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ ▒ █ █ ▒ ▒ ▒ ▒ ▒ █ ▒ ▒ ▒ ▒
'''
