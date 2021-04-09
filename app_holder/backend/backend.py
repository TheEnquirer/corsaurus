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
from gensim.models import word2vec

app = Flask(__name__)
wordvec = None

@app.route('/', methods=['GET'])
def root():
    app.logger.info('Hi :D')
    return 'Hi :D'

@app.route('/test', methods=['PUT'])
def test():
    content = json.loads(request.data)
    app.logger.info(content)
    return jsonify(content)

@app.route('/query', methods=['PUT'])
def query():
    app.logger.info('RECEIVED A QUERY.')
    try:
        #content = request.get_json()
        content = json.loads(request.data)
        app.logger.info(content)
        load_model()
        mode = content['mode'] # query mode
        to_return = None

        # sum words together
        if mode == 'sum':
            num = content['num'] # natural number
            pos = content['pos'] # array of words
            neg = content['neg'] # array of words
            to_return = jsonify(wordvec.most_similar_cosmul(positive=pos, negative=neg, topn=num))
        # find words similar to given word 
        elif mode == 'similar':
            word = content['word'] 
            to_return = jsonify(wordvec.most_similar(word))
        # find distance between two words
        elif mode == 'distance':
            words = content['words']
            to_return = jsonify(wordvec.distance(words[0], words[1]))
        # find distance between one word and group of words
        elif mode == 'distances':
            word = content['word']
            words = content['words']
            to_return = jsonify(wordvec.distances(word, words))
        # find outlier in group of words
        elif mode == 'outlier':
            words = content['words']
            to_return = jsonify(wordvec.doesnt_match(words))

        resp = app.Response(to_return)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        app.logger.error(traceback.format_exc())
        resp = app.Response(traceback.format_exc())
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

def load_model():
    if wordvec is None:
        wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')
        wordvec = wv_model.wv
        del wv_model
    return wordvec

app.logger.info('STARTING.')
wordvec = load_model()
app.logger.info('STARTED.')

'''
EXAMPLE CODE FOR QUERYING:
fetch('BACKENDURL', { 
  method: 'put', 
  body: JSON.stringify(
  {
    'num': 10,
    'pos': ['king', 'woman'],
    'neg': ['man']
  }),
  headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
})
  .then(res =>
  {
    let val = JSON.parse(res.text());
  })
  .catch(err => err)
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
'''