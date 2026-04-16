-- 線上算命系統 - 資料庫初始化腳本 (SQLite)

-- 1. 使用者表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nickname TEXT NOT NULL,
    birthday TEXT, -- 格式: YYYY-MM-DD
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 籤詩表
CREATE TABLE IF NOT EXISTS fortunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,       -- 如 '觀音靈籤'
    number INTEGER NOT NULL,  -- 籤號
    level TEXT NOT NULL,      -- 如 '大吉'
    poem TEXT NOT NULL,       -- 籤詩本文
    explain TEXT,             -- 解曰
    detail TEXT               -- 詳細各面向建議
);

-- 3. 塔羅牌表
CREATE TABLE IF NOT EXISTS tarot_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,                -- 如 '大阿爾克那'
    image_url TEXT,
    meaning_upright TEXT NOT NULL,
    meaning_reversed TEXT NOT NULL
);

-- 4. 占卜紀錄表
CREATE TABLE IF NOT EXISTS history_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    divination_type TEXT NOT NULL, -- 'fortune', 'tarot', 'daily'
    item_id INTEGER,              -- 關聯 fortunes.id 或 tarot_cards.id
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. 捐獻表
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,               -- 允許 NULL (訪客捐獻)
    amount INTEGER NOT NULL,
    message TEXT,
    is_anonymous BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 索引優化
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_history_user_id ON history_records(user_id);
CREATE INDEX IF NOT EXISTS idx_donations_user_id ON donations(user_id);
