import json
import os
from core import asset_manager
from entities.enemy import Enemy

_enemies_database = {}

def init():
    global _enemies_database
    path = os.path.join(asset_manager.ROOT_DIR, 'assets', 'data', 'enemies.json')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            _enemies_database = json.load(file)
        print(f"Загружено {len(_enemies_database)} врагов из базы.")
    except Exception as e:
        print(f"Ошибка загрузки enemies.json: {e}")

def create_enemy(enemy_id: str) -> Enemy | None:
    if enemy_id not in _enemies_database:
        print(f"Враг '{enemy_id}' не найден!")
        return None
        
    data = _enemies_database[enemy_id].copy()
    
    return Enemy(enemy_id=enemy_id, **data)