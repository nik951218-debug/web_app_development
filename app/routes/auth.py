import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User

bp = Blueprint('auth', __name__)

def login_required(view):
    """裝飾器：限制必須登入才能存取的路由。"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("請先登入。")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """每個 Request 前確認登入狀態。"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.get_by_id(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """註冊邏輯。"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nickname = request.form['nickname']
        birthday = request.form.get('birthday')
        error = None

        if not username:
            error = '請輸入帳號。'
        elif not password:
            error = '請輸入密碼。'
        elif not nickname:
            error = '請輸入暱稱。'

        if error is None:
            # 檢查帳號是否已存在
            if User.get_by_username(username):
                error = f"帳號 {username} 已被註冊。"
            else:
                User.create(username, generate_password_hash(password), nickname, birthday)
                flash("註冊成功，請登入。")
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """登入邏輯。"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.get_by_username(username)

        if user is None:
            error = '帳號錯誤。'
        elif not check_password_hash(user['password_hash'], password):
            error = '密碼錯誤。'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash(f"歡迎回來，{user['nickname']}！")
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """登出邏輯。"""
    session.clear()
    flash("您已成功登出。")
    return redirect(url_for('main.index'))
