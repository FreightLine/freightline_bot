from models.truck import Truck

async def save_truck(user_id, truck_name, truck_number, truck_type, tonnage, main_route, back_route):
    truck = Truck(
        user_id=user_id,
        truck_name=truck_name,
        truck_number=truck_number,
        truck_type=truck_type,
        tonnage=tonnage,
        main_route=main_route,
        back_route=back_route,
        status="Свободен"  # Статус по умолчанию
    )
    await truck.save()  # Сохранение данных в БД

async def update_truck_status(user_id, status):
    truck = await Truck.query.where(Truck.user_id == user_id).gino.first()
    if truck:
        truck.status = status
        await truck.update(status=status).apply()  # Обновление статуса
