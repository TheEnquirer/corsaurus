# * TO RUN THIS:
'''
First use this command:
$ export FLASK_APP=backend.py

Then, use this if you would like to enable dev mode:
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

@app.route('/test', methods=['PUT'])
def test():
    content = json.loads(request.data)
    print(content)
    return jsonify(content)

@app.route('/query', methods=['PUT'])
def query():
    try:
        #content = request.get_json()
        content = json.loads(request.data)
        print(content)
        load_model()
        num = content['num'] # natural number
        pos = content['pos'] # array of words
        neg = content['neg'] # array of words
        return jsonify(wordvec.most_similar_cosmul(positive=pos, negative=neg, topn=num))
    except:
        traceback.print_exc()
        return traceback.format_exc()

def load_model():
    if wordvec is None:
        wv_model = word2vec.Word2Vec.load('./data/1billion_word_vectors/1billion_word_vectors')
        wordvec = wv_model.wv
        del wv_model
    return wordvec

   
if __name__ == '__main__':
    wordvec = load_model()
    #app.run(debug=True)
    # ^ commented out because we are using the commands at the top of this script



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