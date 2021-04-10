import time
from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/time')
@cross_origin()
def get_current_time():
    app.logger.info('hereee')
    return {'time': time.time()}

@app.route('/time')
@cross_origin()
def get_current_time():
    app.logger.info('hereee')
    return {'time': time.time()}





app.logger.info('sss')
