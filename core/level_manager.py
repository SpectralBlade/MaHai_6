import os, json
from core import asset_manager, enemy_manager
from core.level import Level

_levels_database = {}

def init():
    global _levels_database
    path = os.path.join(asset_manager.ROOT_DIR, 'assets', 'data', 'stages.json')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            _levels_database = json.load(file)
        print(f"[УСПЕХ] Подгружено {len(_levels_database)} доступных уровней.")
    except Exception as e:
        print(f"[ОШИБКА] Ошибка чтения stages.json: {e}")

def create_level(level_id: str) -> Level | None:
    if level_id not in _levels_database:
        print(f"[ПРЕДУПРЕЖДЕНИЕ] Уровень '{level_id}' не найден!")
        return None
        
    level_data = _levels_database[level_id]

    parsed_waves = []
    
    for phase in level_data['phases']:
        current_wave = []
        enemy_pool = phase['enemy_pool']
        
        for enemy_id, amount in enemy_pool.items():
            for _ in range(amount):
                enemy = enemy_manager.create_enemy(enemy_id)
                if enemy:
                    current_wave.append(enemy)
                    
        parsed_waves.append(current_wave)

    return Level(
        level_id=level_id,
        name=level_data['name'],
        waves=parsed_waves,
        xp_modifier=level_data.get('heroes_xp_modifier', 1.0),
        rewards=level_data.get('physical_awards', {}),
        special_conditions=level_data.get('special_conditions', {})
    )