"""SQLite 数据库管理"""

import sqlite3
from flask import g, current_app


def get_db():
    """获取当前请求的数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """初始化数据库表"""
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            lesson_id TEXT PRIMARY KEY,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS challenge_progress (
            challenge_id TEXT PRIMARY KEY,
            passed INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_result TEXT,
            completed_at TIMESTAMP
        );
    """)
    db.commit()


def init_app(app):
    """在 Flask 应用上注册数据库管理"""
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
