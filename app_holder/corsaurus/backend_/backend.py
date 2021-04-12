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

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gensim.models import word2vec
import traceback
import json

app = Flask(__name__, static_folder='../build', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

vecto = None # the word vector model

@app.route('/', methods=['GET'])
def root():
  return app.send_static_file('index.html')

@cross_origin()
@app.route('/query', methods=['PUT'])
def query():
  global vecto
  #app.logger.info('RECEIVED A QUERY.')
  try:
    #content = request.get_json()
    content = json.loads(request.data)
    '''
    content = request.data
    content = content.decode("utf-8")
    content = jsonify(content)
    '''
    #app.logger.info(content)
    load_model()
    mode = content['mode'] # query mode

    res = None

    # sum words together
    if mode == 'sum':                                                                   # find correlations
      res = vecto.most_similar(
        positive=content['pos'],
        negative=content['neg'],
        topn    =content['num']
      )
    elif mode == 'similar':                                                             # find words similar to given word
      res = vecto.most_similar(content['word'])
    elif mode == 'distance':                                                            # find distance between two words
      res = vecto.distance(content['words'][0], content['words'][1])
    elif mode == 'distances':                                                           # find distance between one word and group of words
      res = vecto.distances(content['word'], content['words'])
    elif mode == 'outlier':                                                             # find outlier in group of words
      res = vecto.doesnt_match(content['words'])
    elif mode == 'similar_vector':                                                      # find words similar to given vector
      res = vecto.similar_by_vector(content['vector'])

    if res is None:
      return jsonify({ 'error': 'invalid_mode' })
    else:
      return jsonify({ 'success': res })

  except KeyError:
    return jsonify({ 'error': 'out_of_vocab' })
  except:
    app.logger.error(traceback.format_exc())
    return jsonify({ 'error': traceback.format_exc() })

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
