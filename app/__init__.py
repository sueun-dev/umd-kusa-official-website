# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .exceptions import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # Determine the project root (one level up from this file)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Create the Flask app with explicit template and static folder paths
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (use relative import for 'routes.main')
    from .routes.main import bp as main_bp

    app.register_blueprint(main_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
