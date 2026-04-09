# 線上算命系統 — 流程圖與資料流文件

本文件描述線上算命系統的使用者操作流程（User Flow）以及核心功能的系統序列圖（Sequence Diagram），幫助開發團隊明確每一項功能的運作步驟與資料傳遞邏輯。

## 1. 使用者流程圖（User Flow）

這張圖展示了使用者從進入網站開始，可以進行的各種操作路徑與頁面跳轉。

```mermaid
flowchart LR
    Start([進入網站]) --> Home[首頁]
    
    Home --> Auth{是否已登入?}
    
    %% 訪客路徑
    Auth -->|否| GuestOptions{瀏覽操作}
    GuestOptions --> Login[登入頁面]
    GuestOptions --> Register[註冊頁面]
    GuestOptions --> DrawFortune[線上抽籤]
    GuestOptions --> Tarot[塔羅牌占卜]
    GuestOptions --> Daily[每日運勢]
    
    %% 會員路徑
    Auth -->|是| UserOptions{會員操作}
    UserOptions --> PerformFortune[進行抽籤/占卜]
    UserOptions --> ViewHistory[我的紀錄]
    UserOptions --> Donate[捐香油錢]
    UserOptions --> Profile[個人資料管理]
    
    %% 算命流程
    DrawFortune --> ShowFortune[顯示籤詩與解籤]
    Tarot --> PickCard[選擇牌陣並翻牌] --> ShowTarot[顯示塔羅牌義]
    Daily --> ShowDaily[查看今日各項指數]
    
    %% 算命包含儲存
    PerformFortune --> ProvideFortune[顯示結果]
    ProvideFortune --> AutoSave[(自動儲存至紀錄)]
    
    %% 儲存後可以到歷史紀錄查看
    AutoSave --> ViewHistory
    
    %% 捐獻流程
    Donate --> ProceedPayment[確認捐獻金額] --> ShowThanks[感謝祈福頁面] --> Ranking[功德榜]
```

---

## 2. 系統序列圖（Sequence Diagram）

以下以系統核心功能 **「已登入使用者進行線上抽籤並保存紀錄」** 為例，說明前端、後端與資料庫之間的資料傳遞流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant Route as Flask Route (Backend)
    participant Model as Database Model
    participant DB as SQLite 資料庫

    User->>Browser: 點擊「開始抽籤」按鈕
    Browser->>Route: POST /fortune/draw
    
    %% 抽取籤詩邏輯
    Route->>Model: 請求隨機抽取一支籤
    Model->>DB: SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1
    DB-->>Model: 回傳籤詩資料 (籤號, 內容, 解曰...)
    Model-->>Route: 籤詩物件
    
    %% 保存紀錄邏輯
    Route->>Model: 要求儲存此抽籤紀錄給當前使用者
    Model->>DB: INSERT INTO history (user_id, fortune_id, date)
    DB-->>Model: 儲存成功
    Model-->>Route: 儲存成功
    
    %% 渲染頁面
    Route->>Browser: render_template('fortune/result.html', data)
    Browser-->>User: 顯示抽籤結果與精美動畫
```

---

## 3. 功能清單與請求對照表

本表格列出系統主要功能對應的 URL 路徑與 HTTP 請求方法（為接下來的路由設計提供基礎）。

| 模組 | 頁面名稱 / 功能 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | 網站首頁 | `/` | `GET` | 系統功能總覽與導覽入口 |
| **帳號管理** | 註冊 | `/register` | `GET`, `POST` | 填寫表單(`GET`)並送出建檔(`POST`) |
| | 登入 | `/login` | `GET`, `POST` | 驗證帳密並建立 Session |
| | 個人資料 | `/profile` | `GET`, `POST` | 查看/修改帳號名稱或密碼 |
| **算命占卜** | 線上抽籤 | `/fortune/draw` | `GET`, `POST` | 進入抽籤頁面(`GET`)與執行搖籤(`POST`) |
| | 籤詩結果 | `/fortune/result/<id>` | `GET` | 顯示特定籤詩的解籤內容 |
| | 塔羅占卜 | `/tarot` | `GET`, `POST` | 選擇牌陣(`GET`)與洗牌翻牌(`POST`) |
| | 塔羅結果 | `/tarot/result/<id>` | `GET` | 顯示翻出的塔羅牌義 |
| | 每日運勢 | `/daily` | `GET` | 根據使用者登入資訊顯示今日運勢 |
| **紀錄** | 歷史紀錄 | `/history` | `GET` | 顯示登入使用者的過往算命與占卜紀錄 |
| **捐獻** | 捐香油錢 | `/donate` | `GET`, `POST` | 填寫金額留言(`GET`)與送出捐獻(`POST`) |
| | 功德榜 | `/donate/ranking` | `GET` | 顯示所有使用者的打賞排行與留言 |
