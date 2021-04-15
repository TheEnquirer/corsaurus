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

In total:
export FLASK_APP=backend.py
export FLASK_ENV=development
flask run
'''

from flask import Flask, request, jsonify, redirect
# from flask_cors import cross_origin
from gensim.models import word2vec
from datetime import datetime
import csv
import traceback
import json
import signal
import sys

GENERATED_MODELS_DIR = '/home/exr0n/vol/storage/model_snapshots/word2vec'
LOG_DIR = '/home/exr0n/vol/storage/logs/corsaurus'

WORDVEC_MODELS = {
        'default': './data/1billion_word_vectors/1billion_word_vectors',
        'window8': f'{GENERATED_MODELS_DIR}/trained_40_vector_size300,window8,min_count5.model',
        'window2': f'{GENERATED_MODELS_DIR}/trained_340_vector_size300,window2,min_count5.model',
    }

app = Flask(__name__, static_folder='../build', static_url_path='/')
app.config['CORS_HEADERS'] = 'Content-Type'

vecto = None # the word vector model

@app.before_request
def redirect_https():
  if app.env == "development":
    return
  if request.is_secure:
    return

  url = request.url.replace("http://", "https://", 1)
  code = 301
  return redirect(url, code=code)

if app.env == 'production':
  logfile = open(f'{LOG_DIR}/{datetime.now().isoformat()}.sumlog', 'a+')
  logwriter = csv.writer(logfile)
  LOG_SUMMARIZE_ROUTES = ['/', '/query']
  log_routes_map = { v: i+1 for i,v in enumerate(LOG_SUMMARIZE_ROUTES) }
  @app.after_request
  def logger(res):
    if request.path in log_routes_map:
      # https://stackoverflow.com/a/279597/10372825
      if not hasattr(logger, "counter") or logger.counter[0] > 10:
        if hasattr(logger, 'counter'):
          logwriter.writerow([datetime.now().isoformat(), logger.counter])
          logfile.flush()
        logger.counter = [0] * (len(LOG_SUMMARIZE_ROUTES) + 1)

      logger.counter[0] += 1
      if request.path in log_routes_map:
        logger.counter[log_routes_map[request.path]] += 1

      # logwriter.writerow([datetime.now().isoformat(), res.status_code, request.remote_addr, request.method, request.host, request.path])

    return res

@app.route('/', methods=['GET'])
def root():
  return app.send_static_file('index.html')

@app.route('/help', methods=['GET'])
def help():
  return "No help page yet, contact us at support@corsaur.us :D"

# @cross_origin()
@app.route('/query', methods=['PUT'])
def query():
  global vecto

  try:
    content = json.loads(request.data)

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
      res = vecto.most_similar(
        positive=[content['word']],
        negative=[],
        topn    =content['num']
      )
    elif mode == 'distance':                                                            # find distance between two words
      res = vecto.distance(content['words'][0], content['words'][1])
    elif mode == 'distances':                                                           # find distance between one word and group of words
      res = vecto.distances(content['word'], content['words'])
    elif mode == 'outlier':                                                             # find outlier in group of words
      res = vecto.doesnt_match(content['words'])
    elif mode == 'similar_vector':                                                      # find words similar to given vector
      res = vecto.similar_by_vector(content['vector'], content['num'])
    elif mode == 'get_vector':                                                          # get vector of a word
      res = vecto[content['word']]
    elif mode == 'relationships':                                                       # get words that represent the relationships between words similar to a sum and the sum
      res = relationship_determiner(content['pos'], content['neg'], content['num'], content['relationship_num'])
    elif mode == 'vocabcheck':
      if 'word' in content:
        res = content['word'] in vecto.key_to_index
      else:
        res = [(w in vecto.key_to_index) for w in content['words']]

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
  """
  Loads word vector model into memory if not already loaded.
  Must be called when initializing backend and should be called whenever using vecto.
  """
  global vecto
  if vecto is None:
    app.logger.info('loading wordvectors...')
    wv_model = word2vec.Word2Vec.load(WORDVEC_MODELS['default'])
    vecto = wv_model.wv
    # TODO: model.wv.save(path), KeyedVectors.load(path, mmap='r')
    del wv_model
    app.logger.info('loaded wordvectors...')

def manual_vector_sum(pos, neg=[]):
  """
  Sums vectors.

  Parameters:
    pos (array) -- *vectors* added in the sum
    neg (array) -- *vectors* subtracted in the sum
  Returns:
    sum (array) -- vector of the sum
  """
  vector_size = 100
  if (len(pos) > 0):
    vector_size = len(pos[0])
  else:
    vector_size = len(neg[0])
  sum = [0] * vector_size

  for i in pos:
    index = 0
    for j in i:
      sum[index] = sum[index] + j
      index += 1

  for x in neg:
    index = 0
    for y in x:
      sum[index] = sum[index] - y
      index += 1

  return sum

def relationship_determiner(pos, neg, n1=10, n2=1):
  """
  Get words that represent the relationships between words similar to a sum and the sum.

  Parameters:
    pos (array) -- words added in the sum
    neg (array) -- words subtracted in the sum
    n1 (int) -- num of words similar to sum (default 10)
    n2 (int) -- num of words for each relationship (default 1)
  Returns:
    relationships (array) -- 2D array of words that represent the relationships
  """
  load_model()
  # get similar words to sum
  similar_words = vecto.most_similar(
    positive=pos,
    negative=neg,
    topn    =n1
  )

  # convert words similar to sum to their vector representations
  index = 0
  for x in similar_words:
    similar_words[index] = vecto[x]
    index += 1

  # convert summed words to their vector representations
  index = 0
  for y in pos:
    pos[index] = vecto[y]
    index += 1
  index = 0
  for z in neg:
    neg[index] = vecto[z]
    index += 1

  sum = manual_vector_sum(pos, neg)

  relationship_vectors = [None] * len(similar_words)

  index = 0
  for i in similar_words:
    relationship_vectors[index] = manual_vector_sum([sum], [i])
    index += 1

  relationships = [None] * len(relationship_vectors)

  index = 0
  for j in relationship_vectors:
    relationships[index] = vecto.similar_by_vector(j, n2)
    index += 1

  return relationships

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
