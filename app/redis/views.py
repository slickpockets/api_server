from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, jsonify)
from app import db

main = Blueprint('main', __name__)

@main.route('/string/<string>', methods=['GET', 'POST'])
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



@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
