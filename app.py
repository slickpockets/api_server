#!/usr/bin/env python
from flask import Flask, jsonify, make_response, request
from flask_restful import reqparse, abort, Api, Resource
import redis
import os

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

for line in open('.env'):
    var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]

redis_pass= os.environ['REDISPASS']
redis_server = os.environ['REDISURL']
redis_port = os.environ['REDISPORT']
redis_db = os.environ['REDISDB']


db = redis.StrictRedis(
    host=redis_server,
    port=redis_port,
    password=redis_pass,
    decode_responses=True
)





@app.route('/string/<string>', methods=['GET', 'POST'])
def access(string):
    if request.method == "GET":
        results = db.get(string)
        return jsonify({'string': results})
    elif request.method == 'POST':
        if request.is_json is True:
            content = request.get_json()
            value = content["value"]
            string = content["string"]
            getset = db.getset(string, arg)
            return jsonify({"updated": {"string": string, "value": arg, "previously": getset}})
        else:
            return(jsonify({"pass json please"}))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
