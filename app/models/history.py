from . import get_db

class HistoryRecord:
    """占卜紀錄資料模型，負責與 history_records 資料表進行互動。"""

    @staticmethod
    def create(user_id, divination_type, item_id=None, note=None):
        """
        新增一筆占卜紀錄。
        :param user_id: 使用者 ID
        :param divination_type: 占卜類型 ('fortune', 'tarot', 'daily')
        :param item_id: 關聯的案號 (籤詩 ID 或塔羅牌 ID)
        :param note: 使用者備註
        :return: 新紀錄的 ID
        """
        db = get_db()
        try:
            cursor = db.execute(
                'INSERT INTO history_records (user_id, divination_type, item_id, note) VALUES (?, ?, ?, ?)',
                (user_id, divination_type, item_id, note)
            )
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating history record: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """取得特定使用者的所有算命紀錄。"""
        db = get_db()
        # 這裡未來可以視需求 join fortunes 或 tarot_cards 取得詳細內容
        return db.execute(
            'SELECT * FROM history_records WHERE user_id = ? ORDER BY created_at DESC', (user_id,)
        ).fetchall()

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆紀錄。"""
        db = get_db()
        return db.execute('SELECT * FROM history_records WHERE id = ?', (record_id,)).fetchone()

    @staticmethod
    def delete(record_id):
        """刪除單筆紀錄。"""
        db = get_db()
        try:
            db.execute('DELETE FROM history_records WHERE id = ?', (record_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting history record: {e}")
            return False
