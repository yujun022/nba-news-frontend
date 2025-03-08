from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from main import SessionLocal, News  # 從 main.py 匯入資料庫連線 & News 模型

# 定義 URL 和 Header
url = "https://tw-nba.udn.com/nba/index"
headers = {"User-Agent": "Mozilla/5.0"}

# 發送 GET 請求並解析頁面
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 建立資料庫會話
db: Session = SessionLocal()

# 逐一處理抓取到的新聞項目
for news in soup.select(".splide__slide"):
    title = news.find("h1").text.strip()
    link = news.find("a")["href"]

    # 這裡會避免重複資料，只有在資料庫中沒有這個鏈接時才會新增
    existing_news = db.query(News).filter_by(link=link).first()
    if not existing_news:
        # 新增新聞資料
        new_news = News(title=title, link=link)
        db.add(new_news)
        print(f"新增新聞: {title}, {link}")  # 用來檢查新增的新聞

# 提交所有變更並關閉資料庫會話
db.commit()
db.close()

print("爬蟲資料抓取並寫入資料庫完成！")
