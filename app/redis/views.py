from flask import Blueprint, abort, request, jsonify, url_for, redirect
import json
from app import db

main = Blueprint('main', __name__)

endpoints = {
	"endpoints": {
		"strings": {
			"get": {
				"url": "/string/<key>"
			},
			"post": {
				"url": "/string/<key>",
				"paramaters": {
					"key": "key location",
					"value": "value of what to store"
				}
			}
		},
        "delete": {
            "url": "/_delete",
            "paramaters": {
                "key": "key you want to delete"
            }
        },
        "key access": {
            "url": "/<key>",
            "paramaters": {
                "none": "key has to exist, should route access to correct endpoint"
            }
        },
        "multi key access": {
            "url": "/keys?",
            "paramaters": {
                "query string": "expects the ?keys=[1,2,3] with 1,2,3 being keys to access"
            }
        }
	}
}

def key_check(key):
    if db.exists(key) == 1:
        return(True)
    else:
        return(False)

def key_type_check(*args):
    print("args:", args, flush=True)
    empty = {}
    for i in args.pop():

        empty.update({i:  db.type(i)})

    return(empty)



@main.route('/')
def index():
    return(jsonify(endpoints))

@main.route('/keys')
def keys():
    a = request.args.get('keys')
    # print(a.split(","), flush=True)
    new = a.split(",")
    new = list(new)
    print(new, flush=True)
    keys = key_type_check(a)
    # print(keys, flush=True)

    return(jsonify({"keys" : keys}))

@main.route('/check/<key>')
def check(key):
    if key_check(key) is False:
        return(jsonify({"Error string Not found": key}))
    return(jsonify({"type": key_type_check(key)}))

@main.route('/<key>', methods=['GET', 'POST'])
def key_access(key):
    if request.method == "GET":
        if key_check(key) is False:
            return(jsonify({"Error key Not found": key}))

    type = key_type_check(key)
    if type == 'string':
        return(redirect(url_for('main.string_access', key=key)))
    elif type == 'list':
        return(redirect(url_for('main.list_access', key=key)))
    elif type == 'set':
        return(redirect(url_for('main.set_access', key=key)))
    elif type == 'hash':
        return(redirect(url_for('main.hash_access', name=key, key=None)))
    elif type == 'zset':
        return(redirect(url_for('main.sorted_set_access', name=key)))
    else:
        return(jsonify({"error": "not found"}))

    return(jsonify({"error": "shouldnt be hitting this"}))




@main.route('/_delete')
def delete():
    return(jsonify({"todo": "not done yet buddy"}))


@main.route('/string/<key>', methods=['GET', 'POST'])
def string_access(key):
    if request.method == "GET":
        if db.get(key) is None:
            return(jsonify({"Error string Not found": key}))
        results = db.get(key)
        return jsonify({'string': results})
    elif request.method == 'POST':
        if request.is_json is True:
            content = request.get_json()
            value = content["value"]
            key = content["key"]
            getset = db.getset(key, arg)
            return jsonify({"updated": {"key": key, "value": value, "previously": getset}})
        else:
            return(jsonify({"pass json please"}))

@main.route('/list/<key>', methods=['GET', 'POST'])
def list_access(key):
    if request.method == "GET":
        return(jsonify({"GET": "list"}))
    elif request.method == "POST":
        return(jsonify({"POST": "list"}))

@main.route("/set/<key>", methods=['GET', 'POST'])
def set_access(key):
    if request.method == "GET":
        return(jsonify({"GET": "set"}))
    elif request.method == "POST":
        return(jsonify({"POST": "set"}))


@main.route("/hash/<name>/", methods=['GET', 'POST'])
@main.route("/hash/<name>/<key>", methods=['GET', 'POST'])
def hash_access(name, key=None):
    if request.method == "GET":
        return(jsonify({"GET": "hash"}))
    elif request.method == "POST":
        return(jsonify({"POST": "hash"}))


@main.route("/sorted-set/<name>/", methods=['GET', 'POST'])
@main.route("/sorted-set/<name>/<key>", methods=['GET', 'POST'])
def sorted_set_access(name, key=None):
    if request.method == "GET":
        return(jsonify({"GET": "zset"}))
    elif request.method == "POST":
        return(jsonify({"POST": "zset"}))

@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
