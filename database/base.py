from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Получение URL базы данных из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция инициализации базы данных
async def init_db():
    import models  # Импорт моделей для создания таблиц
    Base.metadata.create_all(bind=engine)