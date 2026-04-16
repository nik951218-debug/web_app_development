from . import get_db

class Fortune:
    """籤詩資料模型，負責與 fortunes 資料表進行互動。"""

    @staticmethod
    def get_all(fortune_type=None):
        """取得所有籤詩，可依種類篩選。"""
        db = get_db()
        if fortune_type:
            return db.execute('SELECT * FROM fortunes WHERE type = ?', (fortune_type,)).fetchall()
        return db.execute('SELECT * FROM fortunes').fetchall()

    @staticmethod
    def get_by_id(fortune_id):
        """根據 ID 取得特定籤詩。"""
        db = get_db()
        return db.execute('SELECT * FROM fortunes WHERE id = ?', (fortune_id,)).fetchone()

    @staticmethod
    def get_random(fortune_type=None):
        """
        隨機抽取一支籤詩。
        :param fortune_type: 籤詩種類 (例如: '觀音靈籤')
        :return: 隨機的籤詩物件
        """
        db = get_db()
        query = 'SELECT * FROM fortunes'
        params = ()
        if fortune_type:
            query += ' WHERE type = ?'
            params = (fortune_type,)
        
        query += ' ORDER BY RANDOM() LIMIT 1'
        return db.execute(query, params).fetchone()

    @staticmethod
    def update(fortune_id, level=None, poem=None, explain=None, detail=None):
        """更新籤詩內容 (管理用途)。"""
        db = get_db()
        try:
            db.execute(
                '''UPDATE fortunes SET 
                   level = COALESCE(?, level), 
                   poem = COALESCE(?, poem), 
                   explain = COALESCE(?, explain), 
                   detail = COALESCE(?, detail) 
                   WHERE id = ?''',
                (level, poem, explain, detail, fortune_id)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating fortune: {e}")
            return False
