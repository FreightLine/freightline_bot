from sqlalchemy import Column, Integer, String, Boolean
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор пользователя
    telegram_id = Column(String, unique=True, nullable=False)  # Telegram ID пользователя
    full_name = Column(String, nullable=True)  # Полное имя пользователя
    role = Column(String, nullable=False)  # Роль пользователя (грузоотправитель, перевозчик, администратор)
    is_active = Column(Boolean, default=True)  # Статус активности пользователя
    created_at = Column(String, nullable=False)  # Дата создания пользователя