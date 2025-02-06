import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .exceptions import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import bp as main_bp

    app.register_blueprint(main_bp)

    from .routes.new import bp as news_bp

    app.register_blueprint(news_bp)  # Registers /news endpoints

    register_error_handlers(app)

    print("Template folder:", app.template_folder)
    return app
