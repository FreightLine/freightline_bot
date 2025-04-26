# services/cargo_service.py
from models import Cargo  # или другой источник данных

async def get_cargo_by_id(cargo_id):
    # Логика получения груза из базы данных или другого источника
    cargo = await Cargo.query.get(cargo_id)
    return cargo

async def _show_cargo_details(cargo_id):
    cargo = await get_cargo_by_id(cargo_id)
    return cargo
