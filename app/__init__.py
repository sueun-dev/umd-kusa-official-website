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
        static_folder=os.path.join(project_root, "static")
    )
    app.config.from_object(Config)

    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트 등록
    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .routes.new import bp as news_bp
    app.register_blueprint(news_bp)  # /news 경로 등록

    # 글로벌 에러 핸들러 등록
    register_error_handlers(app)

    # (선택 사항) 템플릿 폴더 경로 출력
    print("Template folder:", app.template_folder)

    return app
