# app/exceptions.py

from flask import jsonify, render_template


class InvalidUsage(Exception):
    """
    Exception for invalid usage or unauthorized access.

    Attributes:
        message (str): Explanation of the error.
        status_code (int): HTTP status code to return.
        payload (dict): Additional data to include in the response.
    """

    status_code = 400

    def __init__(self, message="Invalid usage", status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        Convert the exception details to a dictionary for JSON responses.
        """
        rv = dict(self.payload or ())
        rv["error"] = self.message
        return rv


def register_error_handlers(app):
    """
    Register global error handlers for the Flask app.
    """

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template("400.html"), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return render_template("405.html"), 405

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500
