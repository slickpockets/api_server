from flask import Blueprint, abort, request, jsonify

from app import db

default = Blueprint('default', __name__)



@default.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
