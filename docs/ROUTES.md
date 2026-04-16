# 線上算命系統 — 路由設計文件 (Routes Design)

本文件規劃了系統的所有路由、對應的 HTTP 方法、Controller 邏輯以及使用的 Jinja2 模板。

## 1. 路由總覽表

| 模組 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Main** | 網站首頁 | GET | `/` | `index.html` | 系統入口與功能導航 |
| **Auth** | 註冊頁面 | GET | `/register` | `auth/register.html` | 顯示註冊表單 |
| | 執行註冊 | POST | `/register` | — | 建立帳號並重導向至登入 |
| | 登入頁面 | GET | `/login` | `auth/login.html` | 顯示登入表單 |
| | 執行登入 | POST | `/login` | — | 驗證身分並建立 Session |
| | 登出 | GET | `/logout` | — | 清除 Session 並回到首頁 |
| **Draw** | 線上抽籤 | GET | `/fortune/draw` | `fortune/draw.html` | 選擇籤種與顯示動畫 |
| | 執行搖籤 | POST | `/fortune/draw` | — | 隨機抽取籤詩並存入紀錄 |
| | 籤詩結果 | GET | `/fortune/result/<id>` | `fortune/result.html` | 顯示特定 ID 的解籤內容 |
| **Tarot** | 塔羅首頁 | GET | `/tarot` | `fortune/tarot.html` | 塔羅牌陣選擇 |
| | 執行翻牌 | POST | `/tarot/draw` | — | 抽取卡牌、計算正逆位並存紀錄 |
| | 塔羅結果 | GET | `/tarot/result/<id>` | `fortune/tarot_result.html` | 顯示翻出的牌義 |
| **User** | 個人中心 | GET | `/profile` | `user/profile.html` | 查看基本資料與統計 |
| | 歷史紀錄 | GET | `/history` | `fortune/history.html` | 顯示過往算命紀錄列表 |
| | 運勢詳情 | GET | `/history/<id>` | — | 查看單筆歷史紀錄明細 |
| | 每日運勢 | GET | `/daily` | `fortune/daily.html` | 根據生日計算今日運勢 |
| **Donate**| 捐香油錢頁 | GET | `/donate` | `donate/index.html` | 顯示捐款與留言表單 |
| | 執行捐款 | POST | `/donate` | — | 存入捐款紀錄並重導向感謝頁 |
| | 功德榜 | GET | `/donate/ranking`| `donate/ranking.html`| 顯示捐款排行與留言 |

---

## 2. 路由詳細說明

### 2.1 Auth 模組 (`app/routes/auth.py`)

- **POST /register**:
    - 輸入：`username`, `password`, `nickname`, `birthday`
    - 邏輯：檢查帳號是否重複 → Hash 密碼 → 呼叫 `User.create`
    - 輸出：成功重導向至 `/login`；失敗 Flash 錯誤。

- **POST /login**:
    - 輸入：`username`, `password`
    - 邏輯：呼叫 `User.get_by_username` → 用 `check_password_hash` 比對
    - 輸出：成功存入 `session['user_id']` 並重導向首頁。

---

### 2.2 Draw 模組 (`app/routes/draw.py`)

- **POST /fortune/draw**:
    - 輸入：`fortune_type` (from form)
    - 邏輯：呼叫 `Fortune.get_random` → 若已登入則呼叫 `HistoryRecord.create` 儲存
    - 輸出：重導向至 `/fortune/result/<new_history_id>` 或直接顯示。

---

### 2.3 User 模組 (`app/routes/user.py`)

- **GET /history**:
    - 邏輯：檢查 Session → 呼叫 `HistoryRecord.get_by_user`
    - 輸出：渲染 `fortune/history.html` 並傳入列表資料。

---

## 3. Jinja2 模板結構

所有模板皆繼承 `base.html`：
- `base.html`: 包含 Navbar (動態顯示登入/登出), Footer, Flash Messages 顯示區塊。
- 模組化資料夾放置於 `app/templates/` 中，如 `auth/`, `fortune/`, `donate/`。
