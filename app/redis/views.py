from flask import Blueprint, abort, request, jsonify

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
        }
	}
}

def key_check(key):
    if db.exists(key) == 1:
        return(True)
    else:
        return(False)

def key_type_check(key):
    #assume key exists
    return(db.type(key))



@main.route('/')
def index():
    return(jsonify(endpoints))

@main.route('/check/<key>')
def check(key):
    if key_check(key) is False:
        return(jsonify({"Error string Not found": key}))
    return(jsonify({"type": key_type_check(key)}))

@main.route('/<key>', methods=['GET', 'POST'])

def key_access(key):
    if request.method == "GET":
        if key_check(key) is False:
            return(jsonify({"Error string Not found": key}))
        type = key_type_check(key)
        return(jsonify({"type": type}))


@main.route('/_delete')
def delete():
    return(jsonify({"todo": "not done yet buddy"}))


@main.route('/string/<key>', methods=['GET', 'POST'])
def access(key):
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




@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
