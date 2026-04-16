from . import get_db

class Donation:
    """捐獻資料模型，負責與 donations 資料表進行互動。"""

    @staticmethod
    def create(user_id=None, amount=0, message=None, is_anonymous=False):
        """
        建立一筆捐獻紀錄。
        :param user_id: 使用者 ID (可為空)
        :param amount: 捐獻金額
        :param message: 祈福留言
        :param is_anonymous: 是否匿名
        :return: 捐獻紀錄 ID
        """
        db = get_db()
        try:
            cursor = db.execute(
                '''INSERT INTO donations (user_id, amount, message, is_anonymous) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, amount, message, 1 if is_anonymous else 0)
            )
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating donation: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有捐獻紀錄。"""
        db = get_db()
        return db.execute('SELECT * FROM donations ORDER BY created_at DESC').fetchall()

    @staticmethod
    def get_by_id(donation_id):
        """根據 ID 取得單筆捐獻紀錄。"""
        db = get_db()
        return db.execute('SELECT * FROM donations WHERE id = ?', (donation_id,)).fetchone()

    @staticmethod
    def get_leaderboard(limit=10):
        """
        取得功德榜 (依捐獻總金額排序)。
        :param limit: 顯示幾名
        :return: 功德榜資料 (暱稱、總金額、留言數等)
        """
        db = get_db()
        # 這裡示範一個簡單的 SQL：聚合每個使用者的金額
        # 匿名者可能需要特殊處理，這裡我們先簡單列出具名使用者的排行
        return db.execute(
            '''SELECT u.nickname, SUM(d.amount) as total_amount, MAX(d.created_at) as last_donation
               FROM donations d
               LEFT JOIN users u ON d.user_id = u.id
               WHERE d.is_anonymous = 0 AND d.user_id IS NOT NULL
               GROUP BY d.user_id
               ORDER BY total_amount DESC
               LIMIT ?''',
            (limit,)
        ).fetchall()

    @staticmethod
    def delete(donation_id):
        """刪除單筆紀錄。"""
        db = get_db()
        try:
            db.execute('DELETE FROM donations WHERE id = ?', (donation_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting donation: {e}")
            return False
