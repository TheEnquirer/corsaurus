import time
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/time', methods=['PUT'])
@cross_origin()
def get_current_time():
    app.logger.info('hereee')
    # content = json.loads(request.data)
    data = request.data
    data = data.decode("utf-8")
    data = jsonify(data)
    app.logger.info(data)
    # return {'time': time.time()}
    return data

@app.route('/query', methods=['PUT'])
@cross_origin()
def query():
    app.logger.info('sss')
    return {'payload': 'ahahhahaha'}

