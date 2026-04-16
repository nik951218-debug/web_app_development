import sqlite3
from . import get_db

class User:
    """使用者資料模型，負責與 users 資料表進行互動。"""

    @staticmethod
    def create(username, password_hash, nickname, birthday=None):
        """
        建立新使用者。
        :param username: 登入帳號 (Unique)
        :param password_hash: 加密後的密碼
        :param nickname: 顯示暱稱
        :param birthday: 生日 (YYYY-MM-DD)
        :return: 新建立的使用者 ID
        """
        db = get_db()
        try:
            cursor = db.execute(
                'INSERT INTO users (username, password_hash, nickname, birthday) VALUES (?, ?, ?, ?)',
                (username, password_hash, nickname, birthday)
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得使用者資料。"""
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        return user

    @staticmethod
    def get_by_username(username):
        """根據帳號取得使用者資料 (用於登入驗證)。"""
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        return user

    @staticmethod
    def update_profile(user_id, nickname=None, birthday=None):
        """更新使用者個人資料。"""
        db = get_db()
        try:
            db.execute(
                'UPDATE users SET nickname = COALESCE(?, nickname), birthday = COALESCE(?, birthday) WHERE id = ?',
                (nickname, birthday, user_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除使用者帳號。"""
        db = get_db()
        try:
            db.execute('DELETE FROM users WHERE id = ?', (user_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
