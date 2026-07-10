"""Pylearn 应用工厂"""

import os
from flask import Flask
from app.path_utils import get_app_root


def create_app():
    root = get_app_root()

    app = Flask(__name__,
                instance_relative_config=True,
                template_folder=os.path.join(root, 'templates'),
                static_folder=os.path.join(root, 'static'),
                static_url_path='/static')

    # 确保 instance 目录存在（用于 SQLite）
    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY='pylearn-dev-key',
        DATABASE=os.path.join(app.instance_path, 'pylearn.db'),
    )

    # 初始化数据库
    from app import db
    db.init_app(app)

    # 注册路由
    from app.routes import main, lessons, playground, api, challenges, turtle, update_page
    app.register_blueprint(main.bp)
    app.register_blueprint(lessons.bp, url_prefix='/lessons')
    app.register_blueprint(playground.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(challenges.bp)
    app.register_blueprint(turtle.bp)
    app.register_blueprint(update_page.bp)

    return app
