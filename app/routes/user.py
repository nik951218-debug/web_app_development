import random
from datetime import datetime
from flask import Blueprint, render_template, g, flash, redirect, url_for
from .auth import login_required
from ..models.history import HistoryRecord

bp = Blueprint('user', __name__)

@bp.route('/profile')
@login_required
def profile():
    """個人資料頁面。"""
    return render_template('user/profile.html', user=g.user)

@bp.route('/history')
@login_required
def history():
    """歷史紀錄列表。"""
    records = HistoryRecord.get_by_user(g.user['id'])
    return render_template('fortune/history.html', records=records)

@bp.route('/daily')
def daily():
    """每日運勢 (簡單算法展示)。"""
    # 這裡的邏輯可以根據使用者的生日與當天日期進行運算
    # 目前先提供一個包含隨機成分的偽邏輯示範
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 偽造數據
    indices = {
        'overall': random.randint(3, 5),
        'work': random.randint(2, 5),
        'love': random.randint(1, 5),
        'wealth': random.randint(2, 5)
    }
    
    motto = random.choice([
        "心誠則靈，凡事莫強求。",
        "今日宜行善，必有後福。",
        "沈穩應對，轉機就在眼前。",
        "保持微笑，好運自然報到。"
    ])
    
    return render_template('fortune/daily.html', indices=indices, motto=motto, date=today)
