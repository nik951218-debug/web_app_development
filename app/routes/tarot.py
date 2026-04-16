import random
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from ..models.tarot import TarotCard
from ..models.history import HistoryRecord

bp = Blueprint('tarot', __name__, url_prefix='/tarot')

@bp.route('/')
def tarot_home():
    """塔羅牌入口與牌陣選擇。"""
    return render_template('fortune/tarot.html')

@bp.route('/draw', methods=('POST',))
def draw():
    """執行塔羅翻牌。"""
    count = request.form.get('count', type=int, default=1)
    question = request.form.get('question')
    
    # 抽取卡牌
    cards_rows = TarotCard.draw_cards(count)
    if not cards_rows:
        flash("資料庫中尚未建立塔羅牌資料。")
        return redirect(url_for('tarot.tarot_home'))
    
    # 隨機決定正逆位
    cards = []
    for row in cards_rows:
        card = dict(row)
        card['is_reversed'] = random.choice([True, False])
        cards.append(card)
    
    # 如果已登入，儲存紀錄 (這裡示範儲存第一張牌的 ID)
    if g.user and cards:
        HistoryRecord.create(
            user_id=g.user['id'],
            divination_type='tarot',
            item_id=cards[0]['id'],
            note=f"問題: {question} | 抽取張數: {count}"
        )
    
    return render_template('fortune/tarot_result.html', cards=cards, count=count)
