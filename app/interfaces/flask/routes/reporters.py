from flask import Blueprint, jsonify

from .. import flask_api_message

bp = Blueprint('reporters', __name__)
prefix = '/reporters'

@bp.route('/register', methods=['POST'], endpoint='register_reporter')
@flask_api_message
def register_reporter(router, request, current_app, **kwargs):
    return jsonify(router.handle(request, current_app, **kwargs))