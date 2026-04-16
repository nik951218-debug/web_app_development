import os
from flask import Flask
from .models import init_app as init_db_app

def create_app(test_config=None):
    """Flask App Factory"""
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 如果有 config.py 則讀取
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 如果有傳入測試設定則載入
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫相關工具
    init_db_app(app)

    # 註冊 Blueprint
    from .routes import main, auth, draw, tarot, user
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(draw.bp)
    app.register_blueprint(tarot.bp)
    app.register_blueprint(user.bp)

    return app
