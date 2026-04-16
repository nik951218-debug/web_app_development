from flask import Blueprint

# 這裡先定義 Blueprint 物件，方便 App Factory 註冊
# 實作邏輯將在後續步驟中填充

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
draw_bp = Blueprint('draw', __name__)
tarot_bp = Blueprint('tarot', __name__)
user_bp = Blueprint('user', __name__)

# 為了方便從 app/__init__.py 匯入，我們可以導出它們
# 或者在各自的檔案中定義 bp
