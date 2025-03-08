from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# 載入 .env 文件中的環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 讀取環境變數中的 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/nba_news")

# 設置同步資料庫引擎
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 定義資料表
class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False, unique=True)

# 定義 Lifespan 事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("應用程式啟動，建立資料表...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("應用程式關閉")

# FastAPI 應用
app = FastAPI(lifespan=lifespan)

# 設定 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可根據需求修改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 取得資料庫 Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 新聞列表 API 端點
@app.get("/news")
async def get_news(db: Session = Depends(get_db)):
    news_list = db.query(News).all()
    return news_list  # FastAPI 會自動處理為 JSON 格式

# 單條新聞詳情 API 端點
@app.get("/news/{news_id}")
async def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    news_item = db.query(News).filter(News.id == news_id).first()
    if news_item is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news_item  # FastAPI 會自動處理為 JSON 格式

# 定義新增新聞的請求模型
class NewsCreate(BaseModel):
    title: str
    link: str

@app.post("/news")
async def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    # 檢查是否已經有相同的新聞存在
    existing_news = db.query(News).filter_by(link=news.link).first()
    if existing_news:
        raise HTTPException(status_code=400, detail="News already exists")
    
    # 如果沒有重複，新增新聞
    new_news = News(title=news.title, link=news.link)
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news  # 返回新創建的新聞
