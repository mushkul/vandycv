from flask import Blueprint, request, jsonify

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/home/', methods=['GET'])
def return_home():
    return jsonify({
        'message': 'Hello world!',
        'people': ['Luka', 'Adam', 'Stanley']
    })
