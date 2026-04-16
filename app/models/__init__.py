import sqlite3
import os
from flask import g, current_app

def get_db():
    """取得資料庫連線，並存入 Flask 的 g 物件中以便在同一個 Request 中重複使用。"""
    if 'db' not in g:
        # 確保資料庫路徑存在於 instance 資料夾
        db_path = current_app.config.get('DATABASE', os.path.join(current_app.instance_path, 'database.db'))
        
        # 確保 instance 目錄存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # 設定回傳為 dict 格式以便操作
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """關閉資料庫連線。"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """根據 schema.sql 初始化資料庫。"""
    db = get_db()
    
    # 這裡假設 schema.sql 放在專案根目錄的 database/schema.sql
    schema_path = os.path.join(current_app.root_path, '..', 'database', 'schema.sql')
    
    with current_app.open_resource(schema_path) as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """在 Flask App 中註冊資料庫相關函式。"""
    app.teardown_appcontext(close_db)
    # 這裡可以視需求加入 cli 指令 init-db
