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

def abort_string(string):
    if db.get(string) is None:
        abort(404, message="string {} doesn't exist".format(string))


class String(Resource):
    def get(self, name):
        abort_string(name)
        #force casting to be sure
        return(str(db.get(name)))

    def delete(self, name):
        abort_string(name)
        db.delete(name)
        return('', 204)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def abort_string(string):
    if db.get(string) is None:
        abort(404, message="string {} doesn't exist".format(string))


class String(Resource):
    def get(self, name):
        abort_string(name)
        #force casting to be sure
        return(jsonify({'string': str(db.get(name))}))

    def delete(self, name):
        abort_string(name)
        db.delete(name)
        return('', 204)

    def set(self, name, string):
        set = db.set(str(name), (string))
        return(set)






api.add_resource(String, '/string/<name>')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
