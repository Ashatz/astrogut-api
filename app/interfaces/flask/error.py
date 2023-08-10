def register_error_handlers(app):
    from flask import make_response, jsonify
    from ...core.error import AppError

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return make_response(jsonify(error.to_dict()), error.status_code)