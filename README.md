# nba-news-frontend

# 設定說明

## 1. 環境需求

-	Python 3.8+
-	MySQL 資料庫
-	Node.js (用於前端開發)
## 2 . 安裝依賴套件
```bash
pip install -r requirements.txt
```
## 3. 設定環境變數
請在專案根目錄建立 ```bash .env``` 檔案，內容如下：
```bash
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/nba_news
```
## 4. 運行專案

```uvicorn main:app --reload```

前端請使用 Live Server 或其他 HTTP 伺服器來開啟 index.html。
# API 文件
## 1. 獲取新聞列表
### GET /news
```
{
    "id": 1,
    "title": "NBA 最新消息",
    "link": "https://example.com/news/1"
}
```
## 2. 獲取新聞詳情
### GET /news/{news_id}
```
{
  "id": 1,
  "title": "NBA 最新消息",
  "link": "https://example.com/news/1"
}
```
## 3. 新增新聞
### POST /news
```
{
  "title": "NBA 最新消息",
  "link": "https://example.com/news/1"
}
```
# 測試說明
## 測試爬蟲腳本
### 可執行以下命令來測試爬取新聞是否成功：
```python scraper.py```

## 測試 API
### 使用 ```curl``` 或 Postman 測試 API，例如：
```curl -X GET http://127.0.0.1:8000/news```

# 遷移命令
本專案使用 Alembic 進行資料庫遷移。
## 1. 產生遷移文件
```alembic revision --autogenerate -m "initial migration"```

## 2. 執行資料庫遷移
```alembic upgrade head```

# 設計決策與假設
-	爬取的新聞來源為```https://tw-nba.udn.com/nba/index```
-	透過 ```BeautifulSoup``` 解析 HTML 來獲取新聞標題與連結
-	新聞標題與連結存入 MySQL，並透過 FastAPI 提供 API
-	允許 CORS 請求，以支援前端 AJAX 呼叫

