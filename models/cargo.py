from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор груза
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID владельца груза (ссылка на таблицу пользователей)
    description = Column(String, nullable=False)  # Описание груза (например, тип, вес, размеры)
    truck_type = Column(String, nullable=False)  # Тип фуры, необходимой для перевозки
    payment_terms = Column(String, nullable=False)  # Условия оплаты (например, предоплата)
    route = Column(String, nullable=False)  # Маршрут груза (например, Москва → Казань)
    weight = Column(Float, nullable=True)  # Вес груза (в тоннах)
    volume = Column(Float, nullable=True)  # Объем груза (в кубических метрах)

    # Связь с таблицей пользователей
    owner = relationship("User", back_populates="cargo")