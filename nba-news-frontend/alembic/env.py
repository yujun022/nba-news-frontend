import os
from dotenv import load_dotenv
from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from main import Base  # 確保從 main.py 匯入 Base

# 讀取 .env 檔案
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 設定 Alembic
config = context.config
target_metadata = Base.metadata

# 讓 Alembic 使用正確的資料庫連線字串
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 設定日誌
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """以 '離線模式' 執行遷移"""
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """以 '線上模式' 執行遷移"""
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
