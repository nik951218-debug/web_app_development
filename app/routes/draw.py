from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from ..models.fortune import Fortune
from ..models.history import HistoryRecord

bp = Blueprint('draw', __name__, url_prefix='/fortune')

@bp.route('/draw', methods=('GET', 'POST'))
def draw_fortune():
    """抽籤功能頁面。"""
    if request.method == 'POST':
        fortune_type = request.form.get('fortune_type', '觀音靈籤')
        
        # 隨機抽取一支籤
        fortune = Fortune.get_random(fortune_type)
        
        if not fortune:
            flash("目前沒有可用的籤詩。")
            return redirect(url_for('draw.draw_fortune'))
        
        # 如果已登入，儲存至歷史紀錄
        record_id = None
        if g.user:
            record_id = HistoryRecord.create(
                user_id=g.user['id'], 
                divination_type='fortune', 
                item_id=fortune['id'],
                note=request.form.get('question')
            )
        
        # 導向結果頁 (如果有紀錄就傳紀錄 ID，否則傳籤詩 ID)
        # 這裡為了簡化，我們先傳籤詩 ID
        return redirect(url_for('draw.result', fortune_id=fortune['id']))

    return render_template('fortune/draw.html')

@bp.route('/result/<int:fortune_id>')
def result(fortune_id):
    """顯示籤詩結果。"""
    fortune = Fortune.get_by_id(fortune_id)
    if not fortune:
        flash("找不到該籤詩。")
        return redirect(url_for('draw.draw_fortune'))
    
    return render_template('fortune/result.html', fortune=fortune)
