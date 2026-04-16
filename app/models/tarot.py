from . import get_db

class TarotCard:
    """塔羅牌資料模型，負責與 tarot_cards 資料表進行互動。"""

    @staticmethod
    def get_all():
        """取得所有塔羅牌資料。"""
        db = get_db()
        return db.execute('SELECT * FROM tarot_cards').fetchall()

    @staticmethod
    def get_by_id(card_id):
        """根據 ID 取得特定塔羅牌。"""
        db = get_db()
        return db.execute('SELECT * FROM tarot_cards WHERE id = ?', (card_id,)).fetchone()

    @staticmethod
    def draw_cards(count=1):
        """
        隨機抽取 N 張不重複的塔羅牌。
        :param count: 抽取的張數 (預設為 1)
        :return: 塔羅牌物件列表
        """
        db = get_db()
        return db.execute(
            'SELECT * FROM tarot_cards ORDER BY RANDOM() LIMIT ?', (count,)
        ).fetchall()
