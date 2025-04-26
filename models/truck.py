from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор для фуры
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID владельца фуры (ссылка на таблицу пользователей)
    vehicle_type = Column(String, nullable=False)  # Тип транспортного средства (например, "Рефрижератор")
    vehicle_number = Column(String, unique=True, nullable=False)  # Номер транспортного средства
    vehicle_load = Column(Float, nullable=False)  # Грузоподъемность (в тоннах)
    main_route = Column(String, nullable=True)  # Основной маршрут
    return_route = Column(String, nullable=True)  # Обратный маршрут
    is_available = Column(Boolean, default=True)  # Статус доступности (свободен/занят)

    # Связь с таблицей пользователей
    owner = relationship("User", back_populates="trucks")