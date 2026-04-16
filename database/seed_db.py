import sqlite3
import os
from flask import Flask

def seed_data():
    """注入初步的測試資料進入資料庫。"""
    # 這裡我們手動指定資料庫路徑，通常位於 instance/database.db
    db_path = os.path.join('instance', 'database.db')
    
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} does not exist. Please init_db first.")
        return

    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    
    try:
        # 1. 注入籤詩 (Fortunes)
        fortunes = [
            ('觀音靈籤', 1, '大吉', '天開地闢結良緣，日照月臨顯自尊。', '事事如意，求謀皆遂。', '工作：升遷有望\n感情：百年好合\n財運：大發利市'),
            ('觀音靈籤', 2, '中平', '欲求勝事總成虛，百計營求不自由。', '守舊待時，莫強求。', '工作：保守為宜\n感情：波折難免\n健康：多加留意'),
            ('月老籤', 1, '大吉', '關關雎鳩，在河之洲。窈窕淑女，君子好逑。', '緣分已至，宜主動出擊。', '感情：姻緣天成\n建議：敞開心扉'),
            ('財神籤', 8, '吉', '開市大吉發財源，財帛源源滾進門。', '利潤豐厚，宜擴大經營。', '財運：偏財運旺\n投資：可適度嘗試')
        ]
        db.executemany(
            'INSERT INTO fortunes (type, number, level, poem, explain, detail) VALUES (?, ?, ?, ?, ?, ?)',
            fortunes
        )

        # 2. 注入塔羅牌 (Tarot Cards)
        tarot_cards = [
            ('愚者 (The Fool)', '大阿爾克那', 'static/img/tarot/00.jpg', 
             '象徵新的開始、冒險、自發性與無限可能。', 
             '暗示魯莽、冒險過度、或是對現實的逃避。'),
            ('魔術師 (The Magician)', '大阿爾克那', 'static/img/tarot/01.jpg', 
             '象徵意志力、創造力與行動，代表您已具備成功的導具。', 
             '代表能力的濫用、欺騙、或是計畫未經思考。'),
            ('女祭司 (The High Priestess)', '大阿爾克那', 'static/img/tarot/02.jpg', 
             '象徵直覺、潛意識與神祕學。宜向內心尋求答案。', 
             '代表隱瞞真相、情緒不穩、或是直覺的喪失。'),
            ('戀人 (The Lovers)', '大阿爾克那', 'static/img/tarot/06.jpg', 
             '象徵合諧、夥伴關係、價值觀的契合。', 
             '代表不平衡、失和、或是錯誤的決定。')
        ]
        db.executemany(
            'INSERT INTO tarot_cards (name, type, image_url, meaning_upright, meaning_reversed) VALUES (?, ?, ?, ?, ?)',
            tarot_cards
        )

        db.commit()
        print("Success: Sample data seeded successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
