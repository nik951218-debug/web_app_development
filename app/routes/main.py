from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from ..models.donation import Donation

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """首頁。"""
    return render_template('index.html')

@bp.route('/donate', methods=('GET', 'POST'))
def donate():
    """捐獻功能。"""
    if request.method == 'POST':
        amount = request.form.get('amount', type=int)
        message = request.form.get('message')
        is_anonymous = 'is_anonymous' in request.form
        user_id = g.user['id'] if g.user else None

        if not amount or amount <= 0:
            flash("請輸入有效金額。")
        else:
            Donation.create(user_id, amount, message, is_anonymous)
            flash("感謝您的慷慨捐獻，您的功德已被紀錄！")
            return redirect(url_for('main.index'))

    return render_template('donate/index.html')

@bp.route('/donate/ranking')
def ranking():
    """功德榜。"""
    leaderboard = Donation.get_leaderboard()
    return render_template('donate/ranking.html', leaderboard=leaderboard)
